"""Offline tests for the confirmed live XposedOrNot scan path.

Every test injects a fake opener; none makes a network request.
"""

from __future__ import annotations

import http.client
import json
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request

import pytest

from personal_watchdog import cli, profiles

EMAIL = "live-user" + "@example.invalid"
REF = "profile-001"
JSON = [("Content-Type", "application/json")]


def _success(names: list[str], *, email: str = EMAIL) -> bytes:
    return json.dumps(
        {"breaches": [names], "email": email, "status": "success"},
        separators=(",", ":"),
    ).encode()


class _Response:
    def __init__(
        self, status: int, body: bytes, headers: list[tuple[str, str]] | None = None
    ):
        self.status = status
        self.headers = Message()
        for name, value in JSON if headers is None else headers:
            self.headers.add_header(name, value)
        self._body = body

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._body)
        chunk, self._body = self._body[:size], self._body[size:]
        return chunk

    def close(self) -> None:
        pass


class _Opener:
    def __init__(self, outcome: object):
        self.outcome = outcome
        self.requests: list[Request] = []

    def open(self, request: Request, timeout: float) -> object:
        self.requests.append(request)
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


def _state(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> Path:
    state_dir = tmp_path / "state"
    assert cli.main(["init", "--state-dir", str(state_dir)]) == 0
    profiles.add_profile(state_dir, kind="email", value=EMAIL, purpose="live-test")
    capsys.readouterr()
    return state_dir


def _live(state_dir: Path, outcome: object, *extra: str) -> tuple[int, _Opener]:
    opener = _Opener(outcome)
    arguments = [
        "scan",
        "--adapter",
        "xposedornot",
        "--subject-ref",
        REF,
        "--state-dir",
        str(state_dir),
        *(extra or ("--confirm-live", REF)),
    ]
    return cli.main(arguments, opener=opener), opener


def _history(state_dir: Path) -> str:
    return (state_dir / "history.json").read_text(encoding="utf-8")


def test_completed_live_scan_sends_one_request_and_stores_no_address(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    code, opener = _live(state_dir, _Response(200, _success(["Example Breach"])))
    captured = capsys.readouterr()

    assert code == 0
    assert len(opener.requests) == 1
    request = opener.requests[0]
    assert request.full_url == (
        "https://api.xposedornot.com/v1/check-email/"
        "live-user%40example.invalid?include_details=false"
    )
    assert request.get_method() == "GET"
    assert request.data is None
    assert dict(request.header_items()) == {
        "Accept": "application/json",
        "User-agent": "Personal-Watchdog/0.1",
    }

    assert captured.out.splitlines() == [
        "LIVE_REQUEST destination=api.xposedornot.com "
        "source_id=xposedornot.free.check-email subject_ref=profile-001 "
        "sends=email-address requests=1",
        "TRANSPORT http_status=200 disposition=ready reason=ready",
        "SCAN scan_id=scan-001 subject_ref=profile-001 outcome=completed "
        "adapter=xposedornot",
        "SOURCE source_id=xposedornot.free.check-email status=completed "
        'reason_codes=[] finding_keys=["breach:Example Breach"]',
        "BASELINE_CREATED source_id=xposedornot.free.check-email",
    ]
    stored = _history(state_dir)
    for text in (captured.out, captured.err, stored):
        assert EMAIL not in text
        assert "live-user" not in text
    record = json.loads(stored)["scans"][0]
    assert record["adapter"] == "xposedornot"
    assert record["fixture"] is None
    assert record["scan"]["source_checks"][0]["subject_ref"] == REF


def test_new_and_disappeared_breaches_are_reported_between_live_scans(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    _live(state_dir, _Response(200, _success(["Alpha"])))
    capsys.readouterr()

    _live(state_dir, _Response(200, _success(["Alpha", "Beta"])))
    output = capsys.readouterr().out
    assert "COMPARISON kind=new" in output
    assert "EXPOSURE_EVENT kind=exposure-new" in output
    assert "finding_key=breach:Beta" in output

    _live(state_dir, _Response(200, _success(["Beta"])))
    output = capsys.readouterr().out
    assert "COMPARISON kind=disappeared" in output
    assert "finding_key=breach:Alpha" in output


@pytest.mark.parametrize(
    ("outcome", "status", "guard"),
    [
        (
            URLError("refused https://api.xposedornot.com/v1/check-email/" + EMAIL),
            "failed",
            "guarding_failed",
        ),
        (TimeoutError("timed out"), "failed", "guarding_failed"),
        (http.client.RemoteDisconnected("closed"), "failed", "guarding_failed"),
        (http.client.BadStatusLine("garbage"), "failed", "guarding_failed"),
        (
            HTTPError("https://invalid.invalid", 404, "Not Found", Message(), None),
            "failed",
            "guarding_failed",
        ),
        (
            HTTPError("https://invalid.invalid", 429, "Too Many", Message(), None),
            "failed",
            "guarding_failed",
        ),
        (_Response(503, b""), "failed", "guarding_failed"),
        (
            _Response(200, b'{"Error":"Not found","email":null}'),
            "unverifiable",
            "guarding_unverifiable",
        ),
        (
            _Response(200, _success(["Alpha"], email="other" + "@example.invalid")),
            "unverifiable",
            "guarding_unverifiable",
        ),
        (
            _Response(200, b'{"breaches":[[]],"email":"x","status":"success"}'),
            "unverifiable",
            "guarding_unverifiable",
        ),
        (
            _Response(
                200, _success(["Alpha"]), headers=[("Content-Type", "text/html")]
            ),
            "unverifiable",
            "guarding_unverifiable",
        ),
        (_Response(200, b"x" * 20_000), "incomplete", "guarding_"),
    ],
)
def test_non_completed_live_check_is_recorded_and_never_clean(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    outcome: object,
    status: str,
    guard: str,
) -> None:
    state_dir = _state(tmp_path, capsys)
    _live(state_dir, _Response(200, _success(["Alpha"])))
    capsys.readouterr()

    code, opener = _live(state_dir, outcome)
    captured = capsys.readouterr()

    assert code == 0
    assert len(opener.requests) == 1
    assert "status=completed" not in captured.out
    if status != "incomplete":
        assert f"status={status}" in captured.out
    assert f"GUARDING_EVENT kind={guard}" in captured.out
    assert "COMPARISON kind=not_comparable" in captured.out
    assert "disappeared" not in captured.out
    assert "EXPOSURE_EVENT" not in captured.out
    assert "NOTE this check did not complete; it is not a clean result" in captured.out
    stored = _history(state_dir)
    for text in (captured.out, captured.err, stored):
        assert EMAIL not in text
        assert "api.xposedornot.com/v1" not in text
    assert len(json.loads(stored)["scans"]) == 2


def test_failed_scan_between_completed_scans_keeps_the_comparison_point(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    _live(state_dir, _Response(200, _success(["Alpha"])))
    _live(state_dir, URLError("down"))
    capsys.readouterr()

    _live(state_dir, _Response(200, _success(["Alpha", "Beta"])))
    output = capsys.readouterr().out
    assert "BASELINE_CREATED" not in output
    assert "EXPOSURE_EVENT kind=exposure-new" in output
    assert "finding_key=breach:Beta" in output


def test_unreadable_response_metadata_is_recorded_as_unverifiable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    response = _Response(200, _success(["Alpha"]))
    response.headers = None  # type: ignore[assignment]
    code, _ = _live(state_dir, response)
    output = capsys.readouterr().out
    assert code == 0
    assert "status=unverifiable" in output
    assert "reason=unreadable_response_metadata" in output
    assert "NOTE this check did not complete" in output
    assert len(json.loads(_history(state_dir))["scans"]) == 1


def test_other_subjects_and_sources_are_never_the_baseline(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    base = ["scan", "--adapter", "fixture", "--state-dir", str(state_dir)]
    assert cli.main([*base, "--fixture", "baseline"]) == 0
    assert cli.main([*base, "--fixture", "baseline", "--subject-ref", REF]) == 0
    capsys.readouterr()

    _live(state_dir, _Response(200, _success(["Alpha"])))
    output = capsys.readouterr().out
    assert "BASELINE_CREATED source_id=xposedornot.free.check-email" in output
    assert "not_comparable" not in output

    assert cli.main([*base, "--fixture", "changed"]) == 0
    output = capsys.readouterr().out
    assert "subject_ref=fixture-subject-01" in output
    assert "COMPARISON kind=changed" in output


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        (("--fixture", "baseline", "--confirm-live", REF), "--fixture cannot be used"),
        (("--confirm-live", "profile-002"), "confirm with --confirm-live"),
        (("--confirm-live", "PROFILE-001"), "confirm with --confirm-live"),
    ],
)
def test_live_scan_without_exact_confirmation_sends_nothing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    extra: tuple[str, ...],
    message: str,
) -> None:
    state_dir = _state(tmp_path, capsys)
    before = _history(state_dir)
    code, opener = _live(state_dir, _Response(200, _success(["Alpha"])), *extra)
    captured = capsys.readouterr()
    assert code == 2
    assert message in captured.err
    assert captured.out == ""
    assert opener.requests == []
    assert _history(state_dir) == before


def test_live_scan_requires_confirmation_and_subject_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    opener = _Opener(_Response(200, _success(["Alpha"])))
    base = ["scan", "--adapter", "xposedornot", "--state-dir", str(state_dir)]

    assert cli.main([*base, "--subject-ref", REF], opener=opener) == 2
    assert "api.xposedornot.com; confirm with" in capsys.readouterr().err
    assert cli.main(base, opener=opener) == 2
    assert "requires --subject-ref" in capsys.readouterr().err
    assert (
        cli.main(
            ["scan", "--adapter", "fixture", "--confirm-live", REF, "--state-dir"]
            + [str(state_dir)],
            opener=opener,
        )
        == 2
    )
    assert "applies only to a live adapter" in capsys.readouterr().err
    assert opener.requests == []


def test_live_scan_refuses_username_and_disabled_profiles(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    profiles.add_profile(
        state_dir, kind="username", value="live-user-name", purpose="live-test"
    )
    opener = _Opener(_Response(200, _success(["Alpha"])))
    base = ["scan", "--adapter", "xposedornot", "--state-dir", str(state_dir)]

    arguments = [*base, "--subject-ref", "profile-002", "--confirm-live", "profile-002"]
    assert cli.main(arguments, opener=opener) == 2
    assert "requires an email profile" in capsys.readouterr().err

    profiles.disable_profile(state_dir, REF)
    arguments = [*base, "--subject-ref", REF, "--confirm-live", REF]
    assert cli.main(arguments, opener=opener) == 2
    assert "profile is disabled" in capsys.readouterr().err

    assert opener.requests == []
    assert json.loads(_history(state_dir))["scans"] == []


def test_report_and_history_name_the_live_adapter(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_dir = _state(tmp_path, capsys)
    _live(state_dir, _Response(200, _success(["Alpha"])))
    capsys.readouterr()
    assert cli.main(["report", "--latest", "--state-dir", str(state_dir)]) == 0
    assert "adapter=xposedornot" in capsys.readouterr().out
    assert cli.main(["history", "--state-dir", str(state_dir)]) == 0
    output = capsys.readouterr().out
    assert "SCAN scan_id=scan-001 adapter=xposedornot status=completed" in output
    assert EMAIL not in output


@pytest.mark.parametrize(
    ("outcome", "line"),
    [
        (
            URLError("down"),
            "TRANSPORT http_status=none disposition=failed reason=pre_status_failure",
        ),
        (
            HTTPError("https://invalid.invalid", 429, "Too Many", Message(), None),
            "TRANSPORT http_status=429 disposition=failed reason=http_failure",
        ),
        (
            _Response(200, b'{"Error":"Not found","email":null}'),
            "TRANSPORT http_status=200 disposition=ready reason=ready",
        ),
    ],
)
def test_transport_line_explains_the_outcome_without_identifiers(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], outcome: object, line: str
) -> None:
    state_dir = _state(tmp_path, capsys)
    _live(state_dir, outcome)
    output = capsys.readouterr().out
    assert line in output.splitlines()
    assert "TRANSPORT" not in _history(state_dir)
