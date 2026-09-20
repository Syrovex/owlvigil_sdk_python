# OwlVigil Python SDK

Sync and native async Python 3.9+ clients for the OwlVigil AI Gateway,
Management API, streaming, and webhook verification.

## Installation

```bash
pip install owlvigil
```

For a source checkout or unreleased change, install with `pip install .`.

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

Use `environment="staging"` or `environment="local"` for the same endpoint
routing convention as the Go SDK. `OWLVIGIL_ENV` is used when the option is
omitted. Explicit base URLs remain available for reverse proxies and test
servers.

## Supported preview surface

- Gateway models, Chat Completions, Responses, Embeddings, and Anthropic Messages
- Sync and async SSE streaming for Chat Completions and Responses
- Workspace listing, usage summary, and request-log lookup
- The complete generated 144-operation Management OpenAPI catalog, available
  through `open_api()` and generated snake_case methods
- OAuth 2.0 authorization-code, refresh-token, client-credentials, revocation,
  and user-info flows
- Webhook HMAC signing and verification

## Development

```bash
python -m pip install -e '.[test,release]'
pytest
python -m build
python -m twine check dist/*
```

Regenerate the checked-in Management catalog and Python types with:

```bash
python scripts/generate_all.py
```

Live tests are opt-in and read-only.

## Documentation

- Developer guide: [here](https://github.com/Syrovex/owlvigil_sdk_python/blob/main/docs/DEVELOPER_GUIDE.en-US.md)
- [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md),
  [SUPPORT.md](SUPPORT.md), and [CHANGELOG.md](CHANGELOG.md)

Licensed under the [MIT License](LICENSE).
