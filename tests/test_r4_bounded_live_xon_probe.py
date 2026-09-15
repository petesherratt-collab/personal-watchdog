"""Offline tests for the one-shot bounded R4 probe."""

from __future__ import annotations

import json
from email.message import Message
from urllib.error import URLError
from urllib.request import Request

from personal_watchdog import r4_bounded_live_xon_probe as probe
from personal_watchdog.r1 import SourceStatus
from personal_watchdog.r4_bounded_live_xon_probe import (
    PROBE_SUBJECT,
    PROBE_TIMEOUT_SECONDS,
    capture_attempt,
    run_probe,
)
from personal_watchdog.xposedornot_check_email_adapter import (
    MAX_XON_BODY_BYTES,
    normalize_check_email,
)


def _body(*, subject: str = PROBE_SUBJECT, names: list[str] | None = None) -> bytes:
    return json.dumps(
        {
            "breaches": [names or ["Example Breach"]],
            "email": subject,
            "status": "success",
        },
        separators=(",", ":"),
    ).encode()


class _Response:
    def __init__(self, status: int, body: bytes, *, headers: list[tuple[str, str]]):
        self.status = status
        self.headers = Message()
        for name, value in headers:
            self.headers.add_header(name, value)
        self._body = body
        self.closed = False

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._body)
        chunk, self._body = self._body[:size], self._body[size:]
        return chunk

    def close(self) -> None:
        self.closed = True


class _Opener:
    def __init__(self, response: _Response):
        self.response = response
        self.request: Request | None = None
        self.timeout: float | None = None

    def open(self, request: Request, timeout: float) -> _Response:
        self.request = request
        self.timeout = timeout
        return self.response


def test_completed_live_shape_uses_exact_request_and_existing_r3() -> None:
    opener = _Opener(
        _Response(
            200,
            _body(),
            headers=[("Content-Type", "application/json"), ("Server", "test")],
        )
    )

    attempt = capture_attempt(opener)
    check = normalize_check_email(attempt)

    assert opener.request is not None
    assert opener.request.full_url == (
        "https://api.xposedornot.com/v1/check-email/"
        "r4-probe-01%40example.invalid?include_details=false"
    )
    assert opener.request.get_header("Accept") == "application/json"
    assert opener.request.get_header("User-agent") == "Personal-Watchdog-R4/1"
    assert opener.timeout == PROBE_TIMEOUT_SECONDS
    assert attempt.http_status == 200
    assert attempt.body_state == "complete"
    assert check.status is SourceStatus.COMPLETED
    assert [item.finding_key for item in check.observations] == [
        "breach:Example Breach"
    ]


def test_http_failure_is_failed_and_has_no_observations() -> None:
    attempt = capture_attempt(
        _Opener(
            _Response(
                503,
                b'{"error":"server"}',
                headers=[("Content-Type", "application/json")],
            )
        )
    )
    check = normalize_check_email(attempt)

    assert attempt.body_state == "absent"
    assert check.status is SourceStatus.FAILED
    assert check.reason_codes == ("response_failed",)
    assert not check.observations


def test_pre_status_timeout_inside_url_error_is_a_timeout() -> None:
    class _TimeoutOpener:
        def open(self, request: Request, timeout: float) -> object:
            raise URLError(TimeoutError("timed out"))

    attempt = capture_attempt(_TimeoutOpener())

    assert attempt.http_status is None
    assert attempt.timed_out is True
    assert attempt.transport_failure is None
    assert attempt.failure_phase == "before_status"
    assert normalize_check_email(attempt).status is SourceStatus.FAILED


def test_post_status_timeout_discards_prefix_as_incomplete() -> None:
    class _ReadTimeoutResponse(_Response):
        def read(self, size: int = -1) -> bytes:
            if self._body:
                return super().read(size)
            raise TimeoutError("timed out")

    response = _ReadTimeoutResponse(
        200,
        b'{"breaches":',
        headers=[("Content-Type", "application/json")],
    )
    attempt = capture_attempt(_Opener(response))
    check = normalize_check_email(attempt)

    assert attempt.body_state == "incomplete"
    assert attempt.body_bytes == b'{"breaches":'
    assert attempt.timed_out is True
    assert attempt.failure_phase == "after_status"
    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.reason_codes == ("response_incomplete",)


def test_duplicate_content_type_is_unverifiable() -> None:
    attempt = capture_attempt(
        _Opener(
            _Response(
                200,
                _body(),
                headers=[
                    ("Content-Type", "application/json"),
                    ("content-type", "application/json"),
                ],
            )
        )
    )

    assert normalize_check_email(attempt).status is SourceStatus.UNVERIFIABLE


def test_malformed_200_is_unverifiable_not_empty() -> None:
    attempt = capture_attempt(
        _Opener(
            _Response(
                200,
                b'{"breaches":[],"email":"r4-probe-01@example.invalid","status":"success"}',
                headers=[("Content-Type", "application/json")],
            )
        )
    )
    check = normalize_check_email(attempt)

    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.reason_codes == ("response_unverifiable",)
    assert not check.observations


def test_over_limit_response_is_bounded_and_incomplete() -> None:
    response = _Response(
        200,
        b"x" * (MAX_XON_BODY_BYTES + 1),
        headers=[("Content-Type", "application/json")],
    )

    attempt = capture_attempt(_Opener(response))
    check = normalize_check_email(attempt)

    assert attempt.body_state == "over_limit"
    assert len(attempt.body_bytes) == MAX_XON_BODY_BYTES
    assert check.status is SourceStatus.UNVERIFIABLE
    assert check.reason_codes == ("response_incomplete",)
    assert not check.observations


def test_redirect_response_is_not_retried_and_report_has_no_raw_body_or_url() -> None:
    opener = _Opener(
        _Response(
            302,
            b"redirect-body",
            headers=[("Location", "https://elsewhere.invalid")],
        )
    )
    result = run_probe(opener)

    assert result.attempt.http_status == 302
    assert result.attempt.body_state == "complete"
    assert opener.request is not None
    assert "Authorization" not in str(opener.request.header_items())
    rendered = json.dumps(result.as_dict(), sort_keys=True)
    assert "redirect-body" not in rendered
    assert "api.xposedornot.com/v1/check-email" not in rendered
    assert PROBE_SUBJECT not in rendered
    assert result.as_dict(include_diagnostic_body=True)["diagnostic_body_hex"] == (
        b"redirect-body".hex()
    )


def test_default_redirect_handler_rejects_redirects() -> None:
    handler = probe._NoRedirectHandler()

    assert (
        handler.redirect_request(None, None, 302, "", {}, "https://elsewhere.invalid")
        is None
    )
