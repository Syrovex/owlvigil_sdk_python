import httpx
import pytest

from owlvigil import AsyncOwlVigil, MANAGEMENT_OPERATIONS, ManagementOperationRequest, OwlVigil
from owlvigil.management_methods import AsyncGeneratedManagementMethods, GeneratedManagementMethods
from owlvigil.management_types import __all__ as MANAGEMENT_TYPES


def _client(handler):
    return OwlVigil(
        api_key="test_api_key",
        management_base_url="https://api.test/v1",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def _async_client(handler):
    return AsyncOwlVigil(
        api_key="test_api_key",
        management_base_url="https://api.test/v1",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def test_list_workspaces_uses_default_limit_and_omits_cursor():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/workspaces"
        assert dict(request.url.params) == {"limit": "50"}
        return httpx.Response(200, json={"items": []})

    with _client(handler) as client:
        client.management.list_workspaces()


def test_list_workspaces_encodes_cursor_and_custom_limit():
    def handler(request: httpx.Request) -> httpx.Response:
        assert dict(request.url.params) == {"limit": "10", "cursor": "page-2"}
        return httpx.Response(200, json={"items": []})

    with _client(handler) as client:
        client.management.list_workspaces(cursor="page-2", limit=10)


@pytest.mark.parametrize("limit", [0, -1, 101, 1000])
def test_list_workspaces_rejects_limit_out_of_range(limit):
    with _client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="limit must be between 1 and 100"):
            client.management.list_workspaces(limit=limit)


@pytest.mark.parametrize("limit", [1, 100])
def test_list_workspaces_accepts_boundary_limits(limit):
    def handler(request: httpx.Request) -> httpx.Response:
        assert dict(request.url.params)["limit"] == str(limit)
        return httpx.Response(200, json={"items": []})

    with _client(handler) as client:
        client.management.list_workspaces(limit=limit)


@pytest.mark.parametrize("workspace_id", [0, -1])
def test_get_usage_summary_requires_positive_workspace_id(workspace_id):
    with _client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="workspace_id must be positive"):
            client.management.get_usage_summary(workspace_id)


def test_get_usage_summary_sets_workspace_id_query_param():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/gateway/usage/summary"
        assert request.url.params["workspace_id"] == "16"
        return httpx.Response(200, json={"requests": 3})

    with _client(handler) as client:
        response = client.management.get_usage_summary(16)
        assert response.data["requests"] == 3


@pytest.mark.parametrize("request_id", ["", "   "])
def test_get_request_log_requires_request_id(request_id):
    with _client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="request_id is required"):
            client.management.get_request_log(1, request_id)


def test_get_request_log_url_encodes_request_id_and_sets_workspace_id():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path == b"/v1/gateway/request-logs/req%2Fwith-slash?workspace_id=5"
        return httpx.Response(200, json={"id": "req/with-slash"})

    with _client(handler) as client:
        client.management.get_request_log(5, "req/with-slash")


def test_open_api_catalog_and_generated_method_send_typed_request_parts():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"data": {"id": 7}})

    assert len(MANAGEMENT_OPERATIONS) == 144
    with _client(handler) as client:
        response = client.management.get_gateway_providers_provider_id(
            ManagementOperationRequest(path={"provider_id": 7}, query={"include_keys": True})
        )
        assert response.data == {"id": 7}
    assert calls[0].url.path == "/v1/gateway/providers/7"
    assert calls[0].url.params["include_keys"] == "true"
    assert len([name for name in dir(GeneratedManagementMethods) if not name.startswith("_")]) == 144
    assert len([name for name in dir(AsyncGeneratedManagementMethods) if not name.startswith("_")]) == 144
    assert len(MANAGEMENT_TYPES) == 168


def test_iter_workspaces_follows_cursor_pages():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("cursor") == "page-2":
            return httpx.Response(200, json={"items": [{"id": 2}], "page_info": {"has_more": False}})
        return httpx.Response(200, json={"items": [{"id": 1}], "page_info": {"has_more": True, "next_cursor": "page-2"}})

    with _client(handler) as client:
        assert [item["id"] for item in client.management.iter_workspaces(page_size=1)] == [1, 2]


def test_management_unwraps_data_envelope_and_falls_back_to_body_request_id():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": {"items": ["ws"]}, "request_id": "req_from_body"})

    with _client(handler) as client:
        response = client.management.list_workspaces()
        assert response.data == {"items": ["ws"]}
        assert response.meta.request_id == "req_from_body"


@pytest.mark.asyncio
async def test_async_list_workspaces_validates_limit():
    async with _async_client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="limit must be between 1 and 100"):
            await client.management.list_workspaces(limit=0)


@pytest.mark.asyncio
async def test_async_get_usage_summary_validates_workspace_id():
    async with _async_client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="workspace_id must be positive"):
            await client.management.get_usage_summary(0)


@pytest.mark.asyncio
async def test_async_get_request_log_encodes_request_id_and_sets_workspace_id():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path == b"/v1/gateway/request-logs/req%20with-space?workspace_id=7"
        return httpx.Response(200, json={"id": "req with-space"})

    async with _async_client(handler) as client:
        await client.management.get_request_log(7, "req with-space")


@pytest.mark.asyncio
async def test_async_management_unwraps_envelope():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": {"requests": 9}})

    async with _async_client(handler) as client:
        response = await client.management.get_usage_summary(1)
        assert response.data == {"requests": 9}


@pytest.mark.asyncio
async def test_async_open_api_generated_method_and_pagination():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/providers/7"):
            return httpx.Response(200, json={"data": {"id": 7}})
        cursor = request.url.params.get("cursor")
        return httpx.Response(200, json={"items": [{"id": 2 if cursor else 1}], "page_info": {"has_more": not bool(cursor), "next_cursor": "page-2" if not cursor else ""}})

    async with _async_client(handler) as client:
        provider = await client.management.get_gateway_providers_provider_id(ManagementOperationRequest(path={"provider_id": 7}))
        assert provider.data == {"id": 7}
        workspaces = [item async for item in client.management.iter_workspaces(page_size=1)]
        assert [item["id"] for item in workspaces] == [1, 2]


@pytest.mark.asyncio
async def test_async_list_workspaces_uses_default_limit_and_omits_cursor():
    def handler(request: httpx.Request) -> httpx.Response:
        assert dict(request.url.params) == {"limit": "50"}
        return httpx.Response(200, json={"items": []})

    async with _async_client(handler) as client:
        await client.management.list_workspaces()


@pytest.mark.parametrize("request_id", ["", "   "])
@pytest.mark.asyncio
async def test_async_get_request_log_requires_request_id(request_id):
    async with _async_client(lambda request: httpx.Response(200, json={})) as client:
        with pytest.raises(ValueError, match="request_id is required"):
            await client.management.get_request_log(1, request_id)
