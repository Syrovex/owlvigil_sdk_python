import hashlib
import hmac
import time
from typing import Optional

from ._core import OwlVigilError


def verify_webhook(payload: bytes, signature_header: str, secret: str, tolerance: int = 300, now: Optional[int] = None) -> None:
    if not signature_header:
        raise OwlVigilError("Webhook signature is required")
    if not secret.strip():
        raise OwlVigilError("Webhook secret is required")
    timestamp = 0
    signature = ""
    for part in signature_header.split(","):
        key, separator, value = part.strip().partition("=")
        if not separator:
            continue
        if key == "t":
            try:
                timestamp = int(value)
            except ValueError as error:
                raise OwlVigilError("Invalid webhook signature") from error
        elif key == "v1":
            signature = value
    if not timestamp or not signature:
        raise OwlVigilError("Invalid webhook signature")
    if abs((now if now is not None else int(time.time())) - timestamp) > tolerance:
        raise OwlVigilError("Stale webhook timestamp")
    expected = hmac.new(secret.encode(), str(timestamp).encode() + b"." + payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise OwlVigilError("Invalid webhook signature")


def sign_webhook(payload: bytes, timestamp: int, secret: str) -> str:
    signature = hmac.new(secret.encode(), str(timestamp).encode() + b"." + payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={signature}"
