# API overview

`OwlVigil` is the synchronous client and `AsyncOwlVigil` is the native async
client. Both expose `gateway` and `management` and support context-manager
cleanup.

## Gateway

- `list_models`
- `create_chat_completion` and `create_chat_completion_stream`
- `create_response` and `create_response_stream`
- `create_embeddings`
- `create_anthropic_message`

Requests are dictionaries so new provider fields can be used without waiting
for an SDK release. Streaming yields `SseEvent` from a closeable HTTP stream.

## Management

- `list_workspaces`
- `get_usage_summary`
- `get_request_log`

Use the numeric ID returned by `list_workspaces`. Management responses unwrap
the OwlVigil `data` envelope while preserving response metadata.

`RequestOptions` controls timeout, retry limit, idempotency key, workspace ID,
and non-reserved headers. HTTP errors raise `OwlVigilApiError`; transport,
protocol, validation, and webhook failures derive from `OwlVigilError`.

`verify_webhook` and `sign_webhook` operate on original payload bytes. Verify a
request before decoding it or performing business operations.
