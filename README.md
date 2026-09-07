# OwlVigil Python SDK

Sync and native async Python 3.9+ clients for the OwlVigil AI Gateway,
Management API, streaming, and webhook verification.

## Installation

```bash
pip install owlvigil
```

Until the package is published on PyPI, install a trusted source checkout
with `pip install .`.

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

Live tests are opt-in and read-only.

## Documentation

- Developer guides: [English](docs/DEVELOPER_GUIDE.en-US.md) · [简体中文](docs/DEVELOPER_GUIDE.zh-CN.md)
- [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md),
  [SUPPORT.md](SUPPORT.md), and [CHANGELOG.md](CHANGELOG.md)

Licensed under the [MIT License](LICENSE).
