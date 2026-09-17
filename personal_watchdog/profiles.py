"""Restricted local profiles for explicitly approved synthetic identifiers."""

from __future__ import annotations

import getpass
import json
import re
import sys
import unicodedata
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

PROFILE_VERSION = "r7-approved-identifiers/1"
PROFILE_FILE = "profiles.json"
MAX_PROFILES = 8
MAX_VALUE_LENGTH = 128
MAX_PURPOSE_LENGTH = 64
SUBJECT_REF_PATTERN = re.compile(r"^r7-subject-[0-9]{3}$", re.ASCII)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+$", re.ASCII)
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", re.ASCII)
ProfileKind = Literal["email", "username"]
PROFILE_KINDS: tuple[ProfileKind, ...] = ("email", "username")


class ProfileError(ValueError):
    """A safe, user-facing profile configuration error."""


def _path(state_dir: Path) -> Path:
    return state_dir / PROFILE_FILE


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _validate_text(value: object, *, field: str, maximum: int) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise ProfileError(f"profile {field} is invalid")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ProfileError(f"profile {field} is invalid")
    if unicodedata.normalize("NFC", value) != value:
        raise ProfileError(f"profile {field} is invalid")
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in value):
        raise ProfileError(f"profile {field} is invalid")
    return value


def validate_value(kind: ProfileKind, value: object) -> str:
    """Validate one explicitly supplied local identifier without claiming ownership."""

    text = _validate_text(value, field="value", maximum=MAX_VALUE_LENGTH)
    if kind == "email":
        if EMAIL_PATTERN.fullmatch(text) is None:
            raise ProfileError("profile email value is invalid")
    elif USERNAME_PATTERN.fullmatch(text) is None:
        raise ProfileError("profile username value is invalid")
    return text


def validate_purpose(value: object) -> str:
    return _validate_text(value, field="purpose", maximum=MAX_PURPOSE_LENGTH)


def _empty() -> dict[str, object]:
    return {
        "profiles_version": PROFILE_VERSION,
        "next_subject_number": 1,
        "profiles": [],
    }


def _read(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProfileError("cannot read local profiles") from error
    if type(value) is not dict:
        raise ProfileError("local profiles are malformed")
    return cast(dict[str, Any], value)


def _write(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        temporary.write_text(
            json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )
        temporary.chmod(0o600)
        temporary.replace(path)
        path.chmod(0o600)
    except OSError as error:
        raise ProfileError("cannot write local profiles") from error
    finally:
        if temporary.exists():
            temporary.unlink()


def ensure_profiles(state_dir: Path) -> None:
    """Create a versioned empty profile file without changing R6 state."""

    state_dir.mkdir(parents=True, exist_ok=True)
    path = _path(state_dir)
    if not path.exists():
        _write(path, _empty())
    elif not path.is_file():
        raise ProfileError("local profiles path is not a file")


def _validate_profile(value: object) -> dict[str, Any]:
    if type(value) is not dict:
        raise ProfileError("local profile is malformed")
    profile = cast(dict[str, Any], value)
    if set(profile) != {
        "subject_ref",
        "kind",
        "value",
        "approved",
        "enabled",
        "purpose",
        "created_at",
    }:
        raise ProfileError("local profile has unsupported fields")
    subject_ref = profile["subject_ref"]
    if (
        type(subject_ref) is not str
        or SUBJECT_REF_PATTERN.fullmatch(subject_ref) is None
    ):
        raise ProfileError("local subject_ref is invalid")
    kind = profile["kind"]
    if kind not in PROFILE_KINDS:
        raise ProfileError("local profile kind is invalid")
    validate_value(cast(ProfileKind, kind), profile["value"])
    if type(profile["approved"]) is not bool or type(profile["enabled"]) is not bool:
        raise ProfileError("local profile approval state is invalid")
    validate_purpose(profile["purpose"])
    _validate_text(profile["created_at"], field="created_at", maximum=64)
    return profile


def load_profiles(state_dir: Path) -> dict[str, Any]:
    path = _path(state_dir)
    if not path.exists():
        raise ProfileError("local profiles are missing")
    if not path.is_file():
        raise ProfileError("local profiles path is not a file")
    value = _read(path)
    if value.get("profiles_version") != PROFILE_VERSION:
        raise ProfileError("unsupported local profiles version")
    profiles = value.get("profiles")
    if type(profiles) is not list or len(profiles) > MAX_PROFILES:
        raise ProfileError("local profiles exceed the fixed limit")
    validated = [_validate_profile(item) for item in cast(list[object], profiles)]
    refs = [cast(str, item["subject_ref"]) for item in validated]
    if len(set(refs)) != len(refs):
        raise ProfileError("local profile references are not unique")
    next_number = value.get("next_subject_number")
    if type(next_number) is not int or not 1 <= next_number <= 999:
        raise ProfileError("local profile sequence is invalid")
    value["profiles"] = validated
    return value


def add_profile(
    state_dir: Path,
    *,
    kind: ProfileKind,
    value: str,
    purpose: str,
) -> dict[str, str | bool]:
    profiles = load_profiles(state_dir)
    if len(profiles["profiles"]) >= MAX_PROFILES:
        raise ProfileError("local profile limit reached")
    validated_value = validate_value(kind, value)
    validated_purpose = validate_purpose(purpose)
    if any(
        profile["kind"] == kind and profile["value"] == validated_value
        for profile in profiles["profiles"]
    ):
        raise ProfileError("local profile already exists")
    number = cast(int, profiles["next_subject_number"])
    subject_ref = f"r7-subject-{number:03d}"
    profile: dict[str, str | bool] = {
        "subject_ref": subject_ref,
        "kind": kind,
        "value": validated_value,
        "approved": True,
        "enabled": True,
        "purpose": validated_purpose,
        "created_at": _now(),
    }
    profiles["profiles"].append(profile)
    profiles["next_subject_number"] = number + 1
    _write(_path(state_dir), profiles)
    return {key: value for key, value in profile.items() if key != "value"}


def redacted_profiles(state_dir: Path) -> list[dict[str, object]]:
    profiles = load_profiles(state_dir)
    return [
        {
            "subject_ref": profile["subject_ref"],
            "kind": profile["kind"],
            "approved": profile["approved"],
            "enabled": profile["enabled"],
            "purpose": profile["purpose"],
            "created_at": profile["created_at"],
        }
        for profile in profiles["profiles"]
    ]


def selected_profile(state_dir: Path, subject_ref: str) -> dict[str, Any]:
    profiles = load_profiles(state_dir)
    for profile in profiles["profiles"]:
        if profile["subject_ref"] == subject_ref:
            if not profile["approved"]:
                raise ProfileError("profile is not approved")
            if not profile["enabled"]:
                raise ProfileError("profile is disabled")
            return cast(dict[str, Any], profile)
    raise ProfileError("profile reference was not found")


def disable_profile(state_dir: Path, subject_ref: str) -> None:
    profiles = load_profiles(state_dir)
    for profile in profiles["profiles"]:
        if profile["subject_ref"] == subject_ref:
            profile["enabled"] = False
            _write(_path(state_dir), profiles)
            return
    raise ProfileError("profile reference was not found")


def enable_profile(state_dir: Path, subject_ref: str, *, approved: bool) -> None:
    if not approved:
        raise ProfileError("profile enable requires explicit --approve")
    profiles = load_profiles(state_dir)
    for profile in profiles["profiles"]:
        if profile["subject_ref"] == subject_ref:
            profile["approved"] = True
            profile["enabled"] = True
            _write(_path(state_dir), profiles)
            return
    raise ProfileError("profile reference was not found")


def delete_profile(state_dir: Path, subject_ref: str) -> None:
    profiles = load_profiles(state_dir)
    for profile in profiles["profiles"]:
        if profile["subject_ref"] == subject_ref:
            if profile["enabled"]:
                raise ProfileError("profile must be disabled before deletion")
            profiles["profiles"] = [
                item
                for item in profiles["profiles"]
                if item["subject_ref"] != subject_ref
            ]
            _write(_path(state_dir), profiles)
            return
    raise ProfileError("profile reference was not found")


def read_value_from_stdin() -> str:
    """Read one value without echoing it in an interactive terminal."""

    if sys.stdin.isatty():
        return getpass.getpass("Identifier (input hidden): ")
    value = sys.stdin.read()
    if value.endswith("\n"):
        value = value[:-1]
    return value


__all__ = [
    "MAX_PROFILES",
    "PROFILE_FILE",
    "PROFILE_KINDS",
    "PROFILE_VERSION",
    "ProfileError",
    "ProfileKind",
    "add_profile",
    "delete_profile",
    "disable_profile",
    "enable_profile",
    "ensure_profiles",
    "load_profiles",
    "read_value_from_stdin",
    "redacted_profiles",
    "selected_profile",
    "validate_purpose",
    "validate_value",
]
