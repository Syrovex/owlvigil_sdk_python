from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, Optional
from urllib.parse import quote

import httpx

from ._core import (
    ApiResponse,
    AsyncTransport,
    RequestOptions,
    SseEvent,
    SyncTransport,
    env_provider,
)


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


class Management:
    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def list_workspaces(self, cursor: str = "", limit: int = 50, options: Optional[RequestOptions] = None) -> ApiResponse:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        params = httpx.QueryParams({"limit": limit, **({"cursor": cursor} if cursor else {})})
        return self._transport.request("GET", "/workspaces?" + str(params), options=options)

    def get_usage_summary(self, workspace_id: int, options: Optional[RequestOptions] = None) -> ApiResponse:
        return self._transport.request("GET", "/gateway/usage/summary", options=_workspace_options(workspace_id, options))

    def get_request_log(self, workspace_id: int, request_id: str, options: Optional[RequestOptions] = None) -> ApiResponse:
        if not request_id.strip():
            raise ValueError("request_id is required")
        return self._transport.request("GET", "/gateway/request-logs/" + quote(request_id, safe=""), options=_workspace_options(workspace_id, options))


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


class AsyncManagement:
    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def list_workspaces(self, cursor: str = "", limit: int = 50, options: Optional[RequestOptions] = None) -> ApiResponse:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        params = httpx.QueryParams({"limit": limit, **({"cursor": cursor} if cursor else {})})
        return await self._transport.request("GET", "/workspaces?" + str(params), options=options)

    async def get_usage_summary(self, workspace_id: int, options: Optional[RequestOptions] = None) -> ApiResponse:
        return await self._transport.request("GET", "/gateway/usage/summary", options=_workspace_options(workspace_id, options))

    async def get_request_log(self, workspace_id: int, request_id: str, options: Optional[RequestOptions] = None) -> ApiResponse:
        if not request_id.strip():
            raise ValueError("request_id is required")
        return await self._transport.request("GET", "/gateway/request-logs/" + quote(request_id, safe=""), options=_workspace_options(workspace_id, options))


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
    ) -> None:
        self._gateway_transport = SyncTransport(gateway_base_url, env_provider(gateway_key, "OWLVIGIL_GATEWAY_KEY"), timeout, max_retries, http_client)
        self._management_transport = SyncTransport(management_base_url, env_provider(api_key, "OWLVIGIL_API_KEY"), timeout, max_retries, http_client, unwrap_envelope=True)
        self.gateway = Gateway(self._gateway_transport)
        self.management = Management(self._management_transport)

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
    ) -> None:
        self._gateway_transport = AsyncTransport(gateway_base_url, env_provider(gateway_key, "OWLVIGIL_GATEWAY_KEY"), timeout, max_retries, http_client)
        self._management_transport = AsyncTransport(management_base_url, env_provider(api_key, "OWLVIGIL_API_KEY"), timeout, max_retries, http_client, unwrap_envelope=True)
        self.gateway = AsyncGateway(self._gateway_transport)
        self.management = AsyncManagement(self._management_transport)

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
