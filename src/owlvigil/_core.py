from __future__ import annotations

import asyncio
import os
import random
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable, Dict, Iterator, Mapping, Optional

import httpx

from ._version import VERSION


CredentialProvider = Callable[[], str]


@dataclass(frozen=True)
class ResponseMeta:
    status_code: int
    request_id: str
    headers: Mapping[str, str]


@dataclass(frozen=True)
class ApiResponse:
    data: Any
    meta: ResponseMeta


@dataclass(frozen=True)
class RequestOptions:
    workspace_id: Optional[int] = None
    idempotency_key: Optional[str] = None
    timeout: Optional[float] = None
    max_retries: Optional[int] = None
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SseEvent:
    event: str
    data: str
    id: str


class OwlVigilError(Exception):
    pass


class OwlVigilApiError(OwlVigilError):
    def __init__(self, status_code: int, request_id: str, code: str, message: str) -> None:
        self.status_code = status_code
        self.request_id = request_id
        self.code = code
        details = [f"status={status_code}"]
        if code:
            details.append(f"code={code}")
        if request_id:
            details.append(f"request_id={request_id}")
        if message:
            details.append(f"message={message}")
        super().__init__("owlvigil: " + " ".join(details))


class SyncTransport:
    def __init__(
        self,
        base_url: str,
        credential: CredentialProvider,
        timeout: float,
        max_retries: int,
        client: Optional[httpx.Client] = None,
        unwrap_envelope: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.credential = credential
        self.timeout = timeout
        self.max_retries = max_retries
        self._owns_client = client is None
        self.client = client or httpx.Client(timeout=timeout)
        self.unwrap_envelope = unwrap_envelope

    def request(self, method: str, path: str, body: Any = None, options: Optional[RequestOptions] = None) -> ApiResponse:
        opts = options or RequestOptions()
        retries = self.max_retries if opts.max_retries is None else opts.max_retries
        for attempt in range(retries + 1):
            try:
                response = self.client.request(
                    method,
                    self.base_url + (path if path.startswith("/") else "/" + path),
                    params={"workspace_id": opts.workspace_id} if opts.workspace_id is not None else None,
                    json=body,
                    headers=self._headers(opts),
                    timeout=opts.timeout or self.timeout,
                )
                if self._retryable(method, response.status_code, opts) and attempt < retries:
                    self._sleep(attempt, response.headers.get("retry-after"))
                    continue
                return _decode(response, self.unwrap_envelope)
            except httpx.TransportError as error:
                if attempt >= retries or not self._retryable(method, -1, opts):
                    raise OwlVigilError("owlvigil: request failed") from error
                self._sleep(attempt, None)
        raise AssertionError("unreachable")

    def stream(self, path: str, body: Any, options: Optional[RequestOptions] = None) -> Iterator[SseEvent]:
        opts = options or RequestOptions()
        with self.client.stream(
            "POST",
            self.base_url + path,
            json=body,
            headers={**self._headers(opts), "accept": "text/event-stream"},
            timeout=opts.timeout or self.timeout,
        ) as response:
            if not response.is_success:
                response.read()
                raise _api_error(response)
            yield from _parse_sse_lines(response.iter_lines())

    def _headers(self, options: RequestOptions) -> Dict[str, str]:
        credential = self.credential()
        if not credential.strip():
            raise OwlVigilError("OwlVigil credential is required")
        headers = {
            "authorization": "Bearer " + credential,
            "accept": "application/json",
            "user-agent": "owlvigil-python/" + VERSION,
        }
        headers.update(_safe_headers(options.headers))
        if options.idempotency_key:
            headers["idempotency-key"] = options.idempotency_key
        return headers

    @staticmethod
    def _retryable(method: str, status: int, options: RequestOptions) -> bool:
        idempotent = method.upper() in {"GET", "HEAD", "OPTIONS"} or bool(options.idempotency_key)
        return idempotent and status in {-1, 408, 429, 502, 503, 504}

    @staticmethod
    def _sleep(attempt: int, retry_after: Optional[str]) -> None:
        time.sleep(_retry_delay(attempt, retry_after))

    def close(self) -> None:
        if self._owns_client:
            self.client.close()


class AsyncTransport:
    def __init__(
        self,
        base_url: str,
        credential: CredentialProvider,
        timeout: float,
        max_retries: int,
        client: Optional[httpx.AsyncClient] = None,
        unwrap_envelope: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.credential = credential
        self.timeout = timeout
        self.max_retries = max_retries
        self._owns_client = client is None
        self.client = client or httpx.AsyncClient(timeout=timeout)
        self.unwrap_envelope = unwrap_envelope

    async def request(self, method: str, path: str, body: Any = None, options: Optional[RequestOptions] = None) -> ApiResponse:
        opts = options or RequestOptions()
        retries = self.max_retries if opts.max_retries is None else opts.max_retries
        for attempt in range(retries + 1):
            try:
                response = await self.client.request(
                    method,
                    self.base_url + (path if path.startswith("/") else "/" + path),
                    params={"workspace_id": opts.workspace_id} if opts.workspace_id is not None else None,
                    json=body,
                    headers=self._headers(opts),
                    timeout=opts.timeout or self.timeout,
                )
                if SyncTransport._retryable(method, response.status_code, opts) and attempt < retries:
                    await self._sleep(attempt, response.headers.get("retry-after"))
                    continue
                return _decode(response, self.unwrap_envelope)
            except httpx.TransportError as error:
                if attempt >= retries or not SyncTransport._retryable(method, -1, opts):
                    raise OwlVigilError("owlvigil: request failed") from error
                await self._sleep(attempt, None)
        raise AssertionError("unreachable")

    async def stream(self, path: str, body: Any, options: Optional[RequestOptions] = None) -> AsyncIterator[SseEvent]:
        opts = options or RequestOptions()
        async with self.client.stream(
            "POST",
            self.base_url + path,
            json=body,
            headers={**self._headers(opts), "accept": "text/event-stream"},
            timeout=opts.timeout or self.timeout,
        ) as response:
            if not response.is_success:
                await response.aread()
                raise _api_error(response)
            event = ""
            event_id = ""
            data = []
            async for line in response.aiter_lines():
                if not line:
                    if data:
                        yield SseEvent(event, "\n".join(data), event_id)
                    event, data = "", []
                    continue
                event, event_id, data = _consume_sse_line(line, event, event_id, data)
            if data:
                yield SseEvent(event, "\n".join(data), event_id)

    def _headers(self, options: RequestOptions) -> Dict[str, str]:
        credential = self.credential()
        if not credential.strip():
            raise OwlVigilError("OwlVigil credential is required")
        headers = {"authorization": "Bearer " + credential, "accept": "application/json", "user-agent": "owlvigil-python/" + VERSION}
        headers.update(_safe_headers(options.headers))
        if options.idempotency_key:
            headers["idempotency-key"] = options.idempotency_key
        return headers

    @staticmethod
    async def _sleep(attempt: int, retry_after: Optional[str]) -> None:
        await asyncio.sleep(_retry_delay(attempt, retry_after))

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()


def env_provider(value: Optional[str], name: str) -> CredentialProvider:
    return lambda: value if value is not None else os.getenv(name, "")


def _decode(response: httpx.Response, unwrap_envelope: bool = False) -> ApiResponse:
    if not response.is_success:
        raise _api_error(response)
    try:
        data = response.json() if response.content else {}
    except ValueError as error:
        request_id = _request_id(response)
        suffix = f" request_id={request_id}" if request_id else ""
        raise OwlVigilError(f"owlvigil: invalid JSON response status={response.status_code}{suffix}") from error
    request_id = _request_id(response)
    if unwrap_envelope and isinstance(data, dict) and "data" in data:
        request_id = request_id or str(data.get("request_id", ""))
        data = data["data"]
    return ApiResponse(data, ResponseMeta(response.status_code, request_id, dict(response.headers)))


def _api_error(response: httpx.Response) -> OwlVigilApiError:
    code = ""
    message = response.reason_phrase
    body_request_id = ""
    try:
        payload = response.json()
        error = payload.get("error", payload) if isinstance(payload, dict) else {}
        code = str(error.get("code", ""))
        message = str(error.get("message", message))
        if isinstance(payload, dict):
            body_request_id = str(payload.get("request_id", ""))
    except Exception:
        pass
    return OwlVigilApiError(response.status_code, _request_id(response) or body_request_id, code, message)


def _request_id(response: httpx.Response) -> str:
    return response.headers.get("x-request-id", response.headers.get("request-id", ""))


def _parse_sse_lines(lines: Iterator[str]) -> Iterator[SseEvent]:
    event = ""
    event_id = ""
    data = []
    for line in lines:
        if not line:
            if data:
                yield SseEvent(event, "\n".join(data), event_id)
            event, data = "", []
            continue
        event, event_id, data = _consume_sse_line(line, event, event_id, data)
    if data:
        yield SseEvent(event, "\n".join(data), event_id)


def _consume_sse_line(line: str, event: str, event_id: str, data: list) -> tuple:
    if line.startswith(":"):
        return event, event_id, data
    field, separator, value = line.partition(":")
    if separator and value.startswith(" "):
        value = value[1:]
    if field == "event":
        event = value
    elif field == "id" and "\0" not in value:
        event_id = value
    elif field == "data":
        data.append(value)
    return event, event_id, data


def _safe_headers(headers: Mapping[str, str]) -> Dict[str, str]:
    reserved = {"authorization", "host", "content-length", "content-type", "idempotency-key"}
    result = {}
    for name, value in headers.items():
        if name.lower() in reserved:
            raise OwlVigilError(f"Header {name} is managed by the SDK")
        result[name] = value
    return result


def _retry_delay(attempt: int, retry_after: Optional[str]) -> float:
    ceiling: Optional[float] = None
    if retry_after:
        try:
            ceiling = float(retry_after)
        except ValueError:
            try:
                parsed = parsedate_to_datetime(retry_after)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                ceiling = (parsed - datetime.now(timezone.utc)).total_seconds()
            except (TypeError, ValueError, OverflowError):
                pass
    if ceiling is None:
        ceiling = min(2.0, 0.2 * (2**attempt))
    ceiling = min(30.0, max(0.0, ceiling))
    return random.uniform(ceiling / 2, ceiling) if ceiling > 0 else 0.0
