from __future__ import annotations

import os
from typing import Any, AsyncIterator, Dict, Iterator, Optional
from urllib.parse import quote

import httpx

from ._core import (
    ApiResponse,
    AsyncTransport,
    ManagementOperationRequest,
    RequestOptions,
    SseEvent,
    SyncTransport,
    env_provider,
)
from .management_methods import AsyncGeneratedManagementMethods, GeneratedManagementMethods
from .management_operations import MANAGEMENT_OPERATIONS
from .oauth import AsyncOAuth2, OAuth2


class Gateway:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list_models(self, options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("GET", "/v1/models", options=options)

    def create_chat_completion(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("POST", "/v1/chat/completions", request, options)

    def create_chat_completion_stream(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> Iterator[SseEvent]:
        return self._transport.stream("/v1/chat/completions", {**request, "stream": True}, options)

    def create_response(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("POST", "/v1/responses", request, options)

    def create_response_stream(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> Iterator[SseEvent]:
        return self._transport.stream("/v1/responses", {**request, "stream": True}, options)

    def create_embeddings(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("POST", "/v1/embeddings", request, options)

    def create_anthropic_message(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("POST", "/anthropic/v1/messages", request, options)


class Management(GeneratedManagementMethods):
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list_workspaces(self, cursor: str = "", limit: int = 50, options: Optional[RequestOptions] = None) -> ApiResponse:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        params = httpx.QueryParams({"limit": limit, **({"cursor": cursor} if cursor else {})})
        return self._transport.request("GET", "/workspaces?" + str(params), options=options)

    def iter_workspaces(self, page_size: int = 50, options: Optional[RequestOptions] = None) -> Iterator[Any]:
        cursor = ""
        seen_cursors = set()
        while True:
            page = self.list_workspaces(cursor=cursor, limit=page_size, options=options)
            data = page.data if isinstance(page.data, dict) else {"items": page.data}
            yield from data.get("items", [])
            page_info = data.get("page_info", {})
            if not page_info.get("has_more") or not page_info.get("next_cursor"):
                return
            cursor = str(page_info["next_cursor"])
            if cursor in seen_cursors:
                raise ValueError("Management pagination returned a repeated cursor")
            seen_cursors.add(cursor)

    def get_usage_summary(self, workspace_id: int, options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("GET", "/gateway/usage/summary", options=_workspace_options(workspace_id, options))

    def get_request_log(self, workspace_id: int, request_id: str, options: Optional[RequestOptions] = None) -> ApiResponse:
        if not request_id.strip():
            raise ValueError("request_id is required")
        return self._transport.request("GET", "/gateway/request-logs/" + quote(request_id, safe=""), options=_workspace_options(workspace_id, options))

    def open_api(self, operation_id: str, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        operation = MANAGEMENT_OPERATIONS.get(operation_id)
        if operation is None:
            raise ValueError("unknown Management operation: " + operation_id)
        request = request or ManagementOperationRequest()
        path = _resolve_management_path(operation.path, request.path)
        query = httpx.QueryParams(request.query)
        suffix = ("?" + str(query)) if query else ""
        return self._transport.request(operation.method, path + suffix, request.body, request.options)


class AsyncGateway:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list_models(self, options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("GET", "/v1/models", options=options)

    async def create_chat_completion(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("POST", "/v1/chat/completions", request, options)

    def create_chat_completion_stream(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> AsyncIterator[SseEvent]:
        return self._transport.stream("/v1/chat/completions", {**request, "stream": True}, options)

    async def create_response(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("POST", "/v1/responses", request, options)

    def create_response_stream(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> AsyncIterator[SseEvent]:
        return self._transport.stream("/v1/responses", {**request, "stream": True}, options)

    async def create_embeddings(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("POST", "/v1/embeddings", request, options)

    async def create_anthropic_message(self, request: Dict[str, Any], options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("POST", "/anthropic/v1/messages", request, options)


class AsyncManagement(AsyncGeneratedManagementMethods):
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list_workspaces(self, cursor: str = "", limit: int = 50, options: Optional[RequestOptions] = None) -> ApiResponse:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        params = httpx.QueryParams({"limit": limit, **({"cursor": cursor} if cursor else {})})
        return await self._transport.request("GET", "/workspaces?" + str(params), options=options)

    async def iter_workspaces(self, page_size: int = 50, options: Optional[RequestOptions] = None) -> AsyncIterator[Any]:
        cursor = ""
        seen_cursors = set()
        while True:
            page = await self.list_workspaces(cursor=cursor, limit=page_size, options=options)
            data = page.data if isinstance(page.data, dict) else {"items": page.data}
            for workspace in data.get("items", []):
                yield workspace
            page_info = data.get("page_info", {})
            if not page_info.get("has_more") or not page_info.get("next_cursor"):
                return
            cursor = str(page_info["next_cursor"])
            if cursor in seen_cursors:
                raise ValueError("Management pagination returned a repeated cursor")
            seen_cursors.add(cursor)

    async def get_usage_summary(self, workspace_id: int, options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("GET", "/gateway/usage/summary", options=_workspace_options(workspace_id, options))

    async def get_request_log(self, workspace_id: int, request_id: str, options: Optional[RequestOptions] = None) -> ApiResponse:
        if not request_id.strip():
            raise ValueError("request_id is required")
        return await self._transport.request("GET", "/gateway/request-logs/" + quote(request_id, safe=""), options=_workspace_options(workspace_id, options))

    async def open_api(self, operation_id: str, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:
        operation = MANAGEMENT_OPERATIONS.get(operation_id)
        if operation is None:
            raise ValueError("unknown Management operation: " + operation_id)
        request = request or ManagementOperationRequest()
        path = _resolve_management_path(operation.path, request.path)
        query = httpx.QueryParams(request.query)
        suffix = ("?" + str(query)) if query else ""
        return await self._transport.request(operation.method, path + suffix, request.body, request.options)


class OwlVigil:
    def __init__(
        self,
        gateway_key: Optional[str] = None,
        api_key: Optional[str] = None,
        gateway_base_url: str = "https://gateway.owlvigil.com",
        management_base_url: str = "https://api.owlvigil.com/v1",
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: Optional[httpx.Client] = None,
        oauth_base_url: str = "https://open.owlvigil.com",
        environment: Optional[str] = None,
    ) -> None:
        resolved_environment = _resolve_environment(environment or os.getenv("OWLVIGIL_ENV", "production"))
        gateway_base_url = _resolve_environment_url(gateway_base_url, resolved_environment)
        management_base_url = _resolve_environment_url(management_base_url, resolved_environment)
        oauth_base_url = _resolve_environment_url(oauth_base_url, resolved_environment)
        self._gateway_transport = SyncTransport(gateway_base_url, env_provider(gateway_key, "OWLVIGIL_GATEWAY_KEY"), timeout, max_retries, http_client)
        self._management_transport = SyncTransport(management_base_url, env_provider(api_key, "OWLVIGIL_API_KEY"), timeout, max_retries, http_client, unwrap_envelope=True)
        self.gateway = Gateway(self._gateway_transport)
        self.management = Management(self._management_transport)
        self.oauth2 = OAuth2(oauth_base_url, self._gateway_transport.client, timeout)

    def close(self) -> None:
        self._gateway_transport.close()
        self._management_transport.close()

    def __enter__(self) -> "OwlVigil":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


class AsyncOwlVigil:
    def __init__(
        self,
        gateway_key: Optional[str] = None,
        api_key: Optional[str] = None,
        gateway_base_url: str = "https://gateway.owlvigil.com",
        management_base_url: str = "https://api.owlvigil.com/v1",
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: Optional[httpx.AsyncClient] = None,
        oauth_base_url: str = "https://open.owlvigil.com",
        environment: Optional[str] = None,
    ) -> None:
        resolved_environment = _resolve_environment(environment or os.getenv("OWLVIGIL_ENV", "production"))
        gateway_base_url = _resolve_environment_url(gateway_base_url, resolved_environment)
        management_base_url = _resolve_environment_url(management_base_url, resolved_environment)
        oauth_base_url = _resolve_environment_url(oauth_base_url, resolved_environment)
        self._gateway_transport = AsyncTransport(gateway_base_url, env_provider(gateway_key, "OWLVIGIL_GATEWAY_KEY"), timeout, max_retries, http_client)
        self._management_transport = AsyncTransport(management_base_url, env_provider(api_key, "OWLVIGIL_API_KEY"), timeout, max_retries, http_client, unwrap_envelope=True)
        self.gateway = AsyncGateway(self._gateway_transport)
        self.management = AsyncManagement(self._management_transport)
        self.oauth2 = AsyncOAuth2(oauth_base_url, self._gateway_transport.client, timeout)

    async def close(self) -> None:
        await self._gateway_transport.close()
        await self._management_transport.close()

    async def __aenter__(self) -> "AsyncOwlVigil":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()


def _workspace_options(workspace_id: int, options: Optional[RequestOptions]) -> RequestOptions:
    if workspace_id <= 0:
        raise ValueError("workspace_id must be positive")
    source = options or RequestOptions()
    return RequestOptions(workspace_id, source.idempotency_key, source.timeout, source.max_retries, source.headers)


def _resolve_environment(value: str) -> str:
    if value in {"production", "staging", "local"}:
        return value
    raise ValueError("unsupported OwlVigil environment: " + value)


def _resolve_environment_url(base_url: str, environment: str) -> str:
    if environment == "production":
        return base_url
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(base_url)
    if environment == "staging":
        host = parsed.hostname or ""
        if host == "gateway.owlvigil.com":
            host = "staginggateway.owlvigil.com"
        elif host in {"api.owlvigil.com", "open.owlvigil.com"}:
            host = "stagingapi.owlvigil.com"
        netloc = host + ((":" + str(parsed.port)) if parsed.port else "")
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)).rstrip("/")
    host = parsed.hostname or ""
    if host in {"gateway.owlvigil.com", "staginggateway.owlvigil.com"}:
        return "http://localhost:8080"
    if parsed.path.startswith("/v1") or host == "api.owlvigil.com":
        return "http://localhost:8081/v1"
    if host in {"open.owlvigil.com", "stagingapi.owlvigil.com"}:
        return "http://localhost:8081"
    return "http://localhost:8080"


def _resolve_management_path(path: str, parameters: Mapping[str, Any]) -> str:
    import re

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in parameters:
            raise ValueError("missing Management path parameter: " + name)
        return quote(str(parameters[name]), safe="")

    return re.sub(r"\{([^}]+)\}", replace, path)
