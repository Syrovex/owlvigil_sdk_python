import hashlib
import hmac

import pytest

from owlvigil import OwlVigilError, sign_webhook, verify_webhook


PAYLOAD = b'{"type":"invoice.paid"}'
SECRET = "whsec_test"
TIMESTAMP = 1_700_000_000


def _sign(payload: bytes, timestamp: int, secret: str) -> str:
    digest = hmac.new(secret.encode(), str(timestamp).encode() + b"." + payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def test_verify_accepts_a_valid_signature():
    header = _sign(PAYLOAD, TIMESTAMP, SECRET)
    verify_webhook(PAYLOAD, header, SECRET, now=TIMESTAMP)


def test_sign_and_verify_round_trip():
    header = sign_webhook(PAYLOAD, TIMESTAMP, SECRET)
    assert header == _sign(PAYLOAD, TIMESTAMP, SECRET)
    verify_webhook(PAYLOAD, header, SECRET, now=TIMESTAMP)


def test_verify_rejects_missing_signature_header():
    with pytest.raises(OwlVigilError, match="signature is required"):
        verify_webhook(PAYLOAD, "", SECRET, now=TIMESTAMP)


@pytest.mark.parametrize("secret", ["", "   "])
def test_verify_rejects_blank_secret(secret):
    header = _sign(PAYLOAD, TIMESTAMP, "whsec_test")
    with pytest.raises(OwlVigilError, match="secret is required"):
        verify_webhook(PAYLOAD, header, secret, now=TIMESTAMP)


@pytest.mark.parametrize(
    "header",
    ["v1=deadbeef", "t=1700000000", "t=not-a-number,v1=deadbeef", ""],
)
def test_verify_rejects_malformed_signature_header(header):
    if header == "":
        pytest.skip("covered by missing-header test")
    with pytest.raises(OwlVigilError, match="[Ii]nvalid webhook signature"):
        verify_webhook(PAYLOAD, header, SECRET, now=TIMESTAMP)


def test_verify_ignores_unknown_segments_and_whitespace():
    digest = hmac.new(SECRET.encode(), str(TIMESTAMP).encode() + b"." + PAYLOAD, hashlib.sha256).hexdigest()
    header = f" t={TIMESTAMP}, foo=bar, v1={digest} "
    verify_webhook(PAYLOAD, header.strip(), SECRET, now=TIMESTAMP)


def test_verify_ignores_segment_without_equals_sign():
    digest = hmac.new(SECRET.encode(), str(TIMESTAMP).encode() + b"." + PAYLOAD, hashlib.sha256).hexdigest()
    header = f"t={TIMESTAMP},malformed-segment,v1={digest}"
    verify_webhook(PAYLOAD, header, SECRET, now=TIMESTAMP)


def test_verify_rejects_stale_timestamp_just_outside_tolerance():
    header = _sign(PAYLOAD, TIMESTAMP, SECRET)
    with pytest.raises(OwlVigilError, match="Stale webhook timestamp"):
        verify_webhook(PAYLOAD, header, SECRET, tolerance=300, now=TIMESTAMP + 301)


def test_verify_accepts_timestamp_exactly_at_tolerance_boundary():
    header = _sign(PAYLOAD, TIMESTAMP, SECRET)
    verify_webhook(PAYLOAD, header, SECRET, tolerance=300, now=TIMESTAMP + 300)


def test_verify_rejects_tampered_payload():
    header = _sign(PAYLOAD, TIMESTAMP, SECRET)
    with pytest.raises(OwlVigilError, match="Invalid webhook signature"):
        verify_webhook(b'{"type":"tampered"}', header, SECRET, now=TIMESTAMP)


def test_verify_rejects_wrong_secret():
    header = _sign(PAYLOAD, TIMESTAMP, SECRET)
    with pytest.raises(OwlVigilError, match="Invalid webhook signature"):
        verify_webhook(PAYLOAD, header, "whsec_other", now=TIMESTAMP)
