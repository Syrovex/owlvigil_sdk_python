import httpx
import pytest

from owlvigil import AsyncOwlVigil, OwlVigil, OwlVigilError, OwlVigilOAuthError


def test_oauth_authorization_and_client_credentials_preserve_base_path():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"access_token": "token", "token_type": "Bearer"})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with OwlVigil(oauth_base_url="https://proxy.test/owlvigil", http_client=http_client) as client:
            url = client.oauth2.authorization_url("client", "https://app.test/callback", scopes=["read"], state="state")
            token = client.oauth2.client_credentials("client", "secret")
    assert url.startswith("https://proxy.test/owlvigil/oauth/authorize?")
    assert token["access_token"] == "token"
    assert calls[0].url.path == "/owlvigil/oauth/token"
    assert httpx.QueryParams(calls[0].content.decode())["grant_type"] == "client_credentials"


def test_oauth_wraps_malformed_successful_response():
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200, text="not-json", headers={"x-request-id": "oauth-1"}))) as http_client:
        with OwlVigil(oauth_base_url="https://oauth.test", http_client=http_client) as client:
            with pytest.raises(OwlVigilError, match="invalid OAuth JSON response status=200 request_id=oauth-1"):
                client.oauth2.client_credentials("client", "secret")


def test_oauth_error_preserves_protocol_fields():
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(400, json={"error": "invalid_grant", "error_description": "bad code", "error_uri": "https://docs.test/errors/invalid-grant"}))) as http_client:
        with OwlVigil(oauth_base_url="https://oauth.test", http_client=http_client) as client:
            with pytest.raises(OwlVigilOAuthError) as caught:
                client.oauth2.exchange("client", "code", "https://app.test/callback")
    assert caught.value.error_code == "invalid_grant"
    assert caught.value.description == "bad code"
    assert caught.value.uri.endswith("invalid-grant")


@pytest.mark.asyncio
async def test_async_oauth_refresh_and_user_info():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/userinfo"):
            return httpx.Response(200, json={"sub": "user-1"})
        return httpx.Response(200, json={"access_token": "refreshed"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        async with AsyncOwlVigil(oauth_base_url="https://oauth.test", http_client=http_client) as client:
            token = await client.oauth2.refresh("client", "refresh-token")
            user = await client.oauth2.user_info("access-token")
    assert token["access_token"] == "refreshed"
    assert user["sub"] == "user-1"


def test_environment_routes_like_go_sdk():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        with OwlVigil(environment="staging", gateway_key="key", http_client=http_client) as client:
            client.gateway.list_models()
    assert calls[0].url.host == "staginggateway.owlvigil.com"
    with pytest.raises(ValueError, match="unsupported OwlVigil environment"):
        OwlVigil(environment="preview")
