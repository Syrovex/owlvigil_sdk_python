# OwlVigil Python SDK

Sync and native async Python 3.9+ clients for the OwlVigil AI Gateway,
Management API, streaming, and webhook verification. Version 0.1.x is a
preview with a focused Management API surface.

## Installation

After version 0.1.0 is published:

```bash
pip install owlvigil
```

Until then, install a trusted source checkout with `pip install .`.

## Quick start

Set `OWLVIGIL_GATEWAY_KEY` and use a provider-facing model name:

```python
from owlvigil import OwlVigil

with OwlVigil() as client:
    response = client.gateway.create_chat_completion({
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": "Hello"}],
    })
    print(response.data["choices"][0]["message"]["content"])
```

`AsyncOwlVigil` provides native async requests and async streaming. Sync and
async clients are context managers and close only HTTP clients they own.

Set `OWLVIGIL_API_KEY` only for Management calls. List workspaces first, then
pass the returned workspace ID to workspace-scoped methods. `RequestOptions`
controls timeout, retry limits, idempotency keys, and safe custom headers.
Retries apply only to idempotent calls or calls with an idempotency key.

## Supported preview surface

- Gateway models, Chat Completions, Responses, Embeddings, and Anthropic Messages
- Sync and async SSE streaming for Chat Completions and Responses
- Workspace listing, usage summary, and request-log lookup
- Webhook HMAC signing and verification

## Development

```bash
python -m pip install -e '.[test]'
pytest
python -m build
```

Live tests are opt-in and read-only. See the [API overview](docs/API.md), [CONTRIBUTING.md](CONTRIBUTING.md),
[SECURITY.md](SECURITY.md), [SUPPORT.md](SUPPORT.md), and
[CHANGELOG.md](CHANGELOG.md). Licensed under the [MIT License](LICENSE).
