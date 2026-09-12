# OwlVigil Python SDK Documentation

These guides describe the Python SDK's current public API. The Python source,
checked-in Management contract, and tests are the final authority for method
names and request fields.

## Recommended path

1. [Developer Guide (English)](DEVELOPER_GUIDE.en-US.md): install the package,
   choose the correct credential, call Gateway and Management, and handle
   streaming, OAuth 2.0, webhooks, retries, and errors.
2. [开发者文档（简体中文）](DEVELOPER_GUIDE.zh-CN.md): the same workflow in
   Chinese.
3. [Releasing](RELEASING.md): build, validate, and publish the package.

## Public package surface

| Surface | Python API | Responsibility |
| --- | --- | --- |
| Shared client | `OwlVigil`, `AsyncOwlVigil`, `RequestOptions`, `ApiResponse` | lifecycle, request options, response metadata, retries |
| Gateway | `client.gateway` / `async_client.gateway` | models, Chat Completions, Responses, Embeddings, Anthropic-compatible Messages, SSE |
| Management | `client.management` / `async_client.management` | workspaces and the generated 144-operation Management catalog |
| OAuth 2.0 | `client.oauth2` | authorization URL, authorization-code, refresh-token, client-credentials, revoke, user-info |
| Webhook | `verify_webhook`, `sign_webhook` | inbound HMAC-SHA256 verification and test signatures |

## Source and contract references

- [Python package source](https://github.com/Syrovex/owlvigil_sdk_python/tree/main/src/owlvigil)
- [Management operation catalog](../src/owlvigil/management_operations.py)
- [Management TypedDict definitions](../src/owlvigil/management_types.py)
- [OwlVigil Developer Center](https://github.com/Syrovex/owlvigil_openapi/blob/main/docs/owlvigil-developer-center.md)

When a guide and a generated contract disagree, follow the generated contract
and update the guide in the same change.
