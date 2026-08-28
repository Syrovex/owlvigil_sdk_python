import hashlib
import hmac
import re
from pathlib import Path

import httpx
import pytest

from owlvigil import AsyncOwlVigil, OwlVigil, OwlVigilApiError, OwlVigilError, RequestOptions, __version__, verify_webhook


def test_public_version_matches_project_version():
    pyproject = Path(__file__).parents[1].joinpath("pyproject.toml").read_text()
    assert re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE).group(1) == __version__


def test_lists_models_with_gateway_authentication():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test_gateway_key"
        assert request.url.path == "/v1/models"
        return httpx.Response(
            200,
            headers={"x-request-id": "req_models"},
            json={"object": "list", "data": [{"id": "deepseek-v4-flash"}]},
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with OwlVigil(gateway_key="test_gateway_key", gateway_base_url="https://gateway.test", http_client=http_client) as client:
            response = client.gateway.list_models()
            assert response.data["data"][0]["id"] == "deepseek-v4-flash"
            assert response.meta.request_id == "req_models"


@pytest.mark.asyncio
async def test_async_lists_models_without_blocking_wrapper():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"object": "list", "data": [{"id": "deepseek-v4-flash"}]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        async with AsyncOwlVigil(gateway_key="test_gateway_key", gateway_base_url="https://gateway.test", http_client=http_client) as client:
            response = await client.gateway.list_models()
            assert response.data["data"][0]["id"] == "deepseek-v4-flash"


def test_verifies_webhook_signature():
    payload = b'{"type":"test"}'
    timestamp = 1_700_000_000
    signature = hmac.new(b"whsec_test", str(timestamp).encode() + b"." + payload, hashlib.sha256).hexdigest()
    verify_webhook(payload, f"t={timestamp},v1={signature}", "whsec_test", now=timestamp)


def test_preserves_management_error_request_id_from_envelope():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"code": "denied", "message": "no access", "request_id": "req_body"})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with OwlVigil(api_key="test_api_key", management_base_url="https://api.test/v1", http_client=http_client) as client:
            with pytest.raises(OwlVigilApiError) as caught:
                client.management.list_workspaces()
            assert caught.value.request_id == "req_body"


def test_rejects_attempt_to_override_authentication_header():
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))) as http_client:
        with OwlVigil(gateway_key="test_gateway_key", http_client=http_client) as client:
            with pytest.raises(OwlVigilError, match="managed by the SDK"):
                client.gateway.list_models(RequestOptions(headers={"AuThOrIzAtIoN": "Bearer wrong"}))


def test_retains_sse_event_id():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="id: event-1\ndata: one\n\ndata: two\n\n")

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with OwlVigil(gateway_key="test_gateway_key", http_client=http_client) as client:
            events = list(client.gateway.create_chat_completion_stream({"model": "deepseek-v4-flash", "messages": []}))
            assert [event.id for event in events] == ["event-1", "event-1"]
