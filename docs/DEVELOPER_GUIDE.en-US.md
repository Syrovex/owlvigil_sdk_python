# OwlVigil Python SDK Developer Guide

> **Package:** `owlvigil` · **Python:** 3.9+ · **Version:** `0.2.0`

This guide follows the structure of the other OwlVigil SDK developer guides
while using the Python SDK's actual public API. The Python SDK communicates
with OwlVigil over HTTP through [httpx](https://www.python-httpx.org/). It
does not connect to Dashboard databases, Redis, or other server-side
infrastructure.

## 1. Understand the two API surfaces

OwlVigil separates model inference from management operations:

| API surface | Default URL | Credential | Use it for |
| --- | --- | --- | --- |
| Gateway Runtime | `https://gateway.owlvigil.com` | Gateway Key | Models, Chat, Responses, Embeddings, and Anthropic Messages |
| Management API | `https://api.owlvigil.com/v1` | Management API Key | Workspaces, usage, and request logs |

The two credentials are not interchangeable. Use `OWLVIGIL_GATEWAY_KEY` only
with `client.gateway`, and `OWLVIGIL_API_KEY` only with `client.management`.

## 2. Install and make your first request

```bash
pip install owlvigil
```

Keep the Gateway Key in a server-side environment variable:

```bash
export OWLVIGIL_GATEWAY_KEY='your-gateway-key'
```

Minimal synchronous Chat Completions request:

```python
from owlvigil import OwlVigil

with OwlVigil() as client:
    response = client.gateway.create_chat_completion({
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": "Describe OwlVigil in one sentence."}],
        "max_tokens": 64,
    })
    print(response.data["choices"][0]["message"]["content"])
    print("request_id=" + response.meta.request_id)
```

The native async client mirrors the same surface:

```python
import asyncio
from owlvigil import AsyncOwlVigil

async def main() -> None:
    async with AsyncOwlVigil() as client:
        response = await client.gateway.create_chat_completion({
            "model": "deepseek-v4-flash",
            "messages": [{"role": "user", "content": "Hello"}],
        })
        print(response.data["choices"][0]["message"]["content"])

asyncio.run(main())
```

Available model names depend on the Workspace, Providers, routes, and Gateway
Key. Production applications should call `client.gateway.list_models()` first
instead of assuming that the example model is available.

## 3. Client and authentication configuration

### Defaults

`OwlVigil()` / `AsyncOwlVigil()` use:

| Setting | Default |
| --- | --- |
| Gateway Key | `OWLVIGIL_GATEWAY_KEY` |
| Management API Key | `OWLVIGIL_API_KEY` |
| Gateway base URL | `https://gateway.owlvigil.com` |
| Management base URL | `https://api.owlvigil.com/v1` |
| Timeout | 60 seconds |
| Maximum retries | 2 |
| User-Agent | `owlvigil-python/<SDK version>` |

Construction does not immediately require both credentials. Each credential is
read and validated only when its corresponding API surface sends a request. An
application that only uses the Gateway therefore does not need a Management
Key.

### Explicit values and a shared HTTP client

```python
from owlvigil import OwlVigil

client = OwlVigil(
    gateway_key="replace-with-gateway-key",
    api_key="replace-with-management-key",
    timeout=30.0,
    max_retries=1,
)
```

Do not hard-code real credentials. Read them from environment variables or
your server-side secret manager and pass the values in explicitly.

You can also pass `gateway_base_url` and `management_base_url` for staging,
local tests, or private deployments, and an existing `http_client` /
`httpx.Client` (or `httpx.AsyncClient`) to reuse connection pooling across
multiple OwlVigil clients. Do not let ordinary end users control these URLs.

`OwlVigil` and `AsyncOwlVigil` are context managers. `close()` (or exiting the
`with` / `async with` block) only closes the HTTP client when the SDK created
it; a client instance you pass in via `http_client` remains yours to close.

## 4. Gateway model calls

### Discover models

```python
with OwlVigil() as client:
    models = client.gateway.list_models()
    for model in models.data["data"]:
        print(model["id"], "owned_by=" + model.get("owned_by", ""))
```

### Chat Completions

Requests are plain dictionaries, so new provider fields can be used
immediately without waiting for an SDK release:

```python
request = {
    "model": "your-model-id",
    "messages": [
        {"role": "system", "content": "Be concise."},
        {"role": "user", "content": "Explain idempotent requests."},
    ],
    "temperature": 0.2,
    "max_tokens": 256,
}

result = client.gateway.create_chat_completion(request)
choices = result.data["choices"]
if not choices or not choices[0].get("message"):
    raise RuntimeError(f"empty response: request_id={result.meta.request_id}")
```

Use the current Gateway contract for request and response fields. Do not
treat example model names, vector dimensions, or output fields as fixed
values.

### Responses, Embeddings, and Anthropic Messages

These methods accept the same dictionary shape the server contract expects:

```python
response = client.gateway.create_response({"model": "your-model-id", "input": "Summarize this."})
embeddings = client.gateway.create_embeddings({"model": "embedding-model", "input": ["First document", "Second document"]})
anthropic_message = client.gateway.create_anthropic_message({
    "model": "your-model-id",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello"}],
})
```

### SSE streaming

`create_chat_completion_stream` and `create_response_stream` set `stream:
True` on the request and return an iterator (sync) or async iterator (async)
of `SseEvent`. The underlying HTTP stream is opened and closed for you:

```python
for event in client.gateway.create_chat_completion_stream({
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Count from one to three."}],
}):
    print("event=" + event.event, "data=" + event.data)
```

```python
async for event in async_client.gateway.create_chat_completion_stream({
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Count from one to three."}],
}):
    print("event=" + event.event, "data=" + event.data)
```

`event.data` is an undecoded string; parse it according to the current
Gateway contract. A non-2xx response raises `OwlVigilApiError` before any
events are yielded. Output received before a network interruption is partial
output.

## 5. Management and Workspaces

Set the Management API Key in the server environment:

```bash
export OWLVIGIL_API_KEY='your-management-api-key'
```

List accessible Workspaces first, then use the numeric ID returned by the
service:

```python
with OwlVigil() as client:
    page = client.management.list_workspaces()
    for workspace in page.data["items"]:
        print(workspace["id"], workspace["name"])

    if page.data["items"]:
        workspace_id = page.data["items"][0]["id"]
        usage = client.management.get_usage_summary(workspace_id)
        print("requests=" + str(usage.data["requests"]))
```

Do not infer an ID from a slug or assume the first listed Workspace is the
production Workspace. Use a verified tenant mapping or explicit
configuration.

`list_workspaces()` requests 50 items by default. Use
`list_workspaces(cursor, limit)` for pagination; `limit` must be between 1 and
100 (`ValueError` otherwise), and a cursor must be passed back unchanged.
`get_usage_summary(workspace_id)` and `get_request_log(workspace_id,
request_id)` both require a positive `workspace_id`, and `get_request_log`
also requires a non-blank `request_id` — both raise `ValueError` on invalid
input before any request is sent.

Management responses unwrap the OwlVigil `data` envelope automatically:
`response.data` is already the inner payload, and `response.meta.request_id`
falls back to the envelope's `request_id` field when no response header
carries one. Gateway responses are returned as-is, without unwrapping.

## 6. Per-request options, responses, and errors

### RequestOptions

Gateway and Management methods accept an optional `RequestOptions`:

```python
from owlvigil import RequestOptions

options = RequestOptions(
    timeout=20.0,
    max_retries=1,
    idempotency_key="operation-key-v1",
    headers={"X-Correlation-Id": "job-123"},
)
```

The SDK manages `Authorization`, `Host`, `Content-Type`, `Content-Length`, and
`Idempotency-Key`; setting any of these through `headers` raises
`OwlVigilError`. Use an idempotency key only when the server contract
explicitly supports it. A network timeout does not prove that a write was not
processed.

### ApiResponse and request IDs

Successful calls return `ApiResponse`:

```python
response = client.gateway.list_models()
data = response.data
status = response.meta.status_code
request_id = response.meta.request_id
```

An empty response body decodes to `{}`. Store the request ID, method, path,
status, and UTC timestamp for troubleshooting, but never store credentials or
sensitive request and response bodies.

### Exceptions and status codes

```python
from owlvigil import OwlVigilApiError, OwlVigilError

try:
    client.gateway.list_models()
except OwlVigilApiError as error:
    print(f"status={error.status_code} code={error.code} request_id={error.request_id}")
except OwlVigilError:
    ...  # Network, protocol, decoding, or streaming failure.
```

| Status | Recommended action |
| --- | --- |
| 400 / 422 | Fix the request; do not retry |
| 401 | Check credential type, value, status, and expiry |
| 403 | Check scope, Workspace access, and resource permissions |
| 404 | Check the resource ID, path, and Workspace |
| 409 | Read current state before deciding whether to write again |
| 429 | Follow the server's wait guidance and back off |
| 502 / 503 / 504 | Retry only when replay is safe |

The SDK retries only idempotent HTTP methods (GET, HEAD, and OPTIONS), or a
request carrying an idempotency key. It handles 408, 429, 502, 503, 504, and
retryable transport failures, honoring a numeric or HTTP-date `Retry-After`
response header when present and otherwise backing off exponentially
(capped at 30 seconds, with jitter). If the application already has a retry
policy, set per-request `RequestOptions(max_retries=0)` to avoid multiplying
retries.

## 7. Webhook verification

Verify the raw HTTP request bytes before JSON parsing or reserialization:

```python
import os

from owlvigil import verify_webhook

raw_body: bytes = request_body_bytes
signature = f"t={timestamp_header},v1={signature_header}"

verify_webhook(raw_body, signature, os.environ["OWLVIGIL_WEBHOOK_SECRET"])
```

OwlVigil sends the timestamp and signature in the `OW-Webhook-Timestamp` and
`OW-Webhook-Signature` headers. Combine them as `t=<unix-seconds>,v1=<hex-hmac>`
before passing the value to the SDK. The default tolerance is five minutes
and the algorithm is HMAC-SHA256. `verify_webhook` raises `OwlVigilError` for
a missing/blank secret, a malformed signature header, a stale timestamp, or a
signature mismatch.

`sign_webhook(payload, timestamp, secret)` produces the same `t=...,v1=...`
format and is primarily useful for tests that need to construct a valid
signature.

After verification, parse and process the event. Deduplicate by event ID in
durable storage because webhook delivery is at least once.

## 8. Security checklist

- Keep Management API Keys and Gateway Keys separate; use least privilege.
- Store Gateway Key and webhook secrets immediately in a secret manager when
  they are returned by a create or rotate operation.
- Never log Authorization headers, complete credentials, Provider
  credentials, webhook secrets, or sensitive bodies.
- Confirm the environment, Workspace, resource ID, and side effects before
  deletes, payments, rotations, and redeliveries.
- Always consume streaming responses through the provided iterator (it closes
  the underlying HTTP stream for you) and retain request IDs for important
  responses.

## 9. Validation and references

From the Python SDK repository, run:

```bash
python -m pip install -e '.[test]'
pytest
python -m build
```

Live tests are opt-in, read-only, and run only when `OWLVIGIL_LIVE_TEST=1` is
set alongside real credentials.

For HTTP resources, scopes, status codes, and the public response envelope,
see the [OwlVigil Developer Center](https://github.com/Syrovex/owlvigil_openapi/blob/main/docs/owlvigil-developer-center.md)
and the OpenAPI specification.
