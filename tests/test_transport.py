import asyncio
import time

import httpx
import pytest

from owlvigil import AsyncOwlVigil, OwlVigil, OwlVigilApiError, OwlVigilError, RequestOptions, __version__
from owlvigil._core import _retry_delay


@pytest.fixture(autouse=True)
def _no_real_sleep(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda _seconds: None)

    async def _async_sleep(_seconds):
        return None

    monkeypatch.setattr(asyncio, "sleep", _async_sleep)


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def test_missing_credential_raises_before_sending_request(monkeypatch):
    monkeypatch.delenv("OWLVIGIL_GATEWAY_KEY", raising=False)
    called = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal called
        called = True
        return httpx.Response(200, json={})

    with OwlVigil(http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError, match="credential is required"):
            client.gateway.list_models()
    assert called is False


def test_explicit_key_takes_precedence_over_environment(monkeypatch):
    monkeypatch.setenv("OWLVIGIL_GATEWAY_KEY", "env-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer explicit-key"
        return httpx.Response(200, json={})

    with OwlVigil(gateway_key="explicit-key", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.gateway.list_models()


def test_falls_back_to_environment_variable_when_key_not_provided(monkeypatch):
    monkeypatch.setenv("OWLVIGIL_GATEWAY_KEY", "env-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer env-key"
        return httpx.Response(200, json={})

    with OwlVigil(http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.gateway.list_models()


def test_user_agent_reports_sdk_version():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["user-agent"] == f"owlvigil-python/{__version__}"
        return httpx.Response(200, json={})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.gateway.list_models()


# ---------------------------------------------------------------------------
# Reserved headers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "header_name",
    ["Authorization", "AUTHORIZATION", "Host", "Content-Length", "content-type", "Idempotency-Key"],
)
def test_rejects_reserved_headers_case_insensitively(header_name):
    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})))) as client:
        with pytest.raises(OwlVigilError, match="managed by the SDK"):
            client.gateway.list_models(RequestOptions(headers={header_name: "x"}))


def test_allows_safe_custom_headers():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-correlation-id"] == "job-123"
        return httpx.Response(200, json={})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.gateway.list_models(RequestOptions(headers={"X-Correlation-Id": "job-123"}))


# ---------------------------------------------------------------------------
# Retry behavior (sync)
# ---------------------------------------------------------------------------


def test_retries_idempotent_get_on_retryable_status_then_succeeds():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"ok": True})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        response = client.gateway.list_models()
        assert response.data == {"ok": True}
    assert len(calls) == 2


def test_raises_after_exhausting_retries_on_persistent_retryable_status():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(503, json={"error": {"code": "unavailable"}})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            client.gateway.list_models(RequestOptions(max_retries=1))
        assert caught.value.code == "unavailable"
    assert len(calls) == 2


def test_does_not_retry_non_idempotent_request_without_idempotency_key():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(429, json={"error": {"code": "rate_limited"}})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError):
            client.gateway.create_chat_completion({"model": "m", "messages": []})
    assert len(calls) == 1


def test_retries_non_idempotent_request_carrying_idempotency_key():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"id": "chatcmpl_1"})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        response = client.gateway.create_chat_completion(
            {"model": "m", "messages": []},
            RequestOptions(idempotency_key="op-1"),
        )
        assert response.data["id"] == "chatcmpl_1"
    assert len(calls) == 2


def test_retries_transport_error_then_succeeds():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ConnectError("boom", request=request)
        return httpx.Response(200, json={"ok": True})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        response = client.gateway.list_models()
        assert response.data == {"ok": True}
    assert len(calls) == 2


def test_transport_error_exhausts_retries_and_wraps_cause():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError, match="request failed") as caught:
            client.gateway.list_models(RequestOptions(max_retries=1))
        assert isinstance(caught.value.__cause__, httpx.ConnectError)


def test_transport_error_not_retried_for_non_idempotent_without_idempotency_key():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        raise httpx.ConnectError("boom", request=request)

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError):
            client.gateway.create_chat_completion({"model": "m", "messages": []})
    assert len(calls) == 1


def test_honors_retry_after_header_delay(monkeypatch):
    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    recorded = []
    monkeypatch.setattr(time, "sleep", lambda seconds: recorded.append(seconds))
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503, headers={"retry-after": "2"})
        return httpx.Response(200, json={"ok": True})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        client.gateway.list_models()
    assert recorded == [2.0]


# ---------------------------------------------------------------------------
# Retry behavior (async)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_retries_idempotent_get_then_succeeds():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"ok": True})

    async with AsyncOwlVigil(gateway_key="k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        response = await client.gateway.list_models()
        assert response.data == {"ok": True}
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_async_does_not_retry_non_idempotent_without_idempotency_key():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(429, json={})

    async with AsyncOwlVigil(gateway_key="k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError):
            await client.gateway.create_chat_completion({"model": "m", "messages": []})
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_async_retries_transport_error_then_succeeds():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ConnectError("boom", request=request)
        return httpx.Response(200, json={"ok": True})

    async with AsyncOwlVigil(gateway_key="k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        response = await client.gateway.list_models()
        assert response.data == {"ok": True}
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_async_transport_error_exhausts_retries_and_wraps_cause():
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    async with AsyncOwlVigil(gateway_key="k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError, match="request failed") as caught:
            await client.gateway.list_models(RequestOptions(max_retries=1))
        assert isinstance(caught.value.__cause__, httpx.ConnectError)


@pytest.mark.asyncio
async def test_async_missing_credential_raises_before_sending_request(monkeypatch):
    monkeypatch.delenv("OWLVIGIL_GATEWAY_KEY", raising=False)
    called = False

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal called
        called = True
        return httpx.Response(200, json={})

    async with AsyncOwlVigil(http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError, match="credential is required"):
            await client.gateway.list_models()
    assert called is False


@pytest.mark.asyncio
async def test_async_retries_non_idempotent_request_carrying_idempotency_key():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503)
        assert request.headers["idempotency-key"] == "op-async-1"
        return httpx.Response(200, json={"id": "chatcmpl_async"})

    async with AsyncOwlVigil(gateway_key="k", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as client:
        response = await client.gateway.create_chat_completion(
            {"model": "m", "messages": []},
            RequestOptions(idempotency_key="op-async-1"),
        )
        assert response.data["id"] == "chatcmpl_async"
    assert len(calls) == 2


# ---------------------------------------------------------------------------
# Decoding and error extraction
# ---------------------------------------------------------------------------


def test_empty_success_body_decodes_to_empty_dict():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"")

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        response = client.gateway.list_models()
        assert response.data == {}


def test_invalid_json_body_raises_with_status_and_request_id():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not-json", headers={"x-request-id": "req_bad"})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilError, match="invalid JSON response status=200 request_id=req_bad"):
            client.gateway.list_models()


def test_error_extracts_nested_error_object():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"error": {"code": "bad_request", "message": "nope"}})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            client.gateway.list_models()
        assert caught.value.code == "bad_request"
        assert "nope" in str(caught.value)


def test_error_falls_back_to_flat_payload_fields():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"code": "denied", "message": "no access"})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            client.gateway.list_models()
        assert caught.value.code == "denied"


def test_error_falls_back_to_reason_phrase_for_non_json_body():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, content=b"internal error")

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            client.gateway.list_models()
        assert caught.value.code == ""
        assert caught.value.status_code == 500


def test_request_id_header_takes_precedence_over_body():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"request_id": "req_body"}, headers={"x-request-id": "req_header"})

    with OwlVigil(gateway_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler))) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            client.gateway.list_models()
        assert caught.value.request_id == "req_header"


# ---------------------------------------------------------------------------
# Client / transport lifecycle
# ---------------------------------------------------------------------------


def test_close_shuts_down_owned_http_client():
    client = OwlVigil(gateway_key="k")
    owned_client = client._gateway_transport.client
    client.close()
    assert owned_client.is_closed is True


def test_close_leaves_externally_supplied_http_client_open():
    external = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})))
    client = OwlVigil(gateway_key="k", http_client=external)
    client.close()
    assert external.is_closed is False
    external.close()


@pytest.mark.asyncio
async def test_async_close_shuts_down_owned_http_client():
    client = AsyncOwlVigil(gateway_key="k")
    owned_client = client._gateway_transport.client
    await client.close()
    assert owned_client.is_closed is True


@pytest.mark.asyncio
async def test_async_close_leaves_externally_supplied_http_client_open():
    external = httpx.AsyncClient(transport=httpx.MockTransport(lambda r: httpx.Response(200, json={})))
    client = AsyncOwlVigil(gateway_key="k", http_client=external)
    await client.close()
    assert external.is_closed is False
    await external.aclose()


# ---------------------------------------------------------------------------
# _retry_delay pure-function bounds
# ---------------------------------------------------------------------------


def test_retry_delay_uses_numeric_retry_after_as_ceiling(monkeypatch):
    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    assert _retry_delay(0, "5") == 5.0


def test_retry_delay_parses_http_date_retry_after(monkeypatch):
    from datetime import datetime, timedelta, timezone

    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    future = datetime.now(timezone.utc) + timedelta(seconds=10)
    from email.utils import format_datetime

    delay = _retry_delay(0, format_datetime(future))
    assert 8.0 <= delay <= 10.5


def test_retry_delay_falls_back_to_exponential_backoff_when_missing(monkeypatch):
    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    assert _retry_delay(0, None) == pytest.approx(0.2)
    assert _retry_delay(1, None) == pytest.approx(0.4)
    assert _retry_delay(2, None) == pytest.approx(0.8)


def test_retry_delay_ignores_unparsable_retry_after(monkeypatch):
    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    assert _retry_delay(0, "not-a-date") == pytest.approx(0.2)


def test_retry_delay_is_clamped_to_thirty_seconds(monkeypatch):
    monkeypatch.setattr("owlvigil._core.random.uniform", lambda lo, hi: hi)
    assert _retry_delay(0, "999") == 30.0
