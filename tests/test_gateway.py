import json

import httpx
import pytest

from owlvigil import AsyncOwlVigil, OwlVigil, OwlVigilApiError


def _client(handler, **kwargs):
    return OwlVigil(
        gateway_key="test_gateway_key",
        gateway_base_url="https://gateway.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        **kwargs,
    )


def _async_client(handler, **kwargs):
    return AsyncOwlVigil(
        gateway_key="test_gateway_key",
        gateway_base_url="https://gateway.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        **kwargs,
    )


def test_create_chat_completion_sends_body_and_does_not_unwrap_envelope():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        assert json.loads(request.content) == {"model": "deepseek-v4-flash", "messages": []}
        return httpx.Response(200, json={"data": "not-an-envelope-for-gateway", "id": "chatcmpl_1"})

    with _client(handler) as client:
        response = client.gateway.create_chat_completion({"model": "deepseek-v4-flash", "messages": []})
        assert response.data == {"data": "not-an-envelope-for-gateway", "id": "chatcmpl_1"}


def test_create_response_posts_to_responses_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/responses"
        return httpx.Response(200, json={"id": "resp_1"})

    with _client(handler) as client:
        response = client.gateway.create_response({"model": "m", "input": "hi"})
        assert response.data["id"] == "resp_1"


def test_create_embeddings_posts_to_embeddings_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/embeddings"
        assert json.loads(request.content)["model"] == "embedding-model"
        return httpx.Response(200, json={"data": [{"embedding": [0.1, 0.2]}]})

    with _client(handler) as client:
        response = client.gateway.create_embeddings({"model": "embedding-model", "input": ["a"]})
        assert response.data["data"][0]["embedding"] == [0.1, 0.2]


def test_create_anthropic_message_posts_to_anthropic_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/anthropic/v1/messages"
        return httpx.Response(200, json={"id": "msg_1", "type": "message"})

    with _client(handler) as client:
        response = client.gateway.create_anthropic_message({"model": "m", "max_tokens": 16, "messages": []})
        assert response.data["type"] == "message"


def test_chat_completion_stream_sets_stream_flag_and_yields_multiple_events():
    def handler(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content)["stream"] is True
        assert request.headers["accept"] == "text/event-stream"
        return httpx.Response(
            200,
            text="event: delta\ndata: one\n\nevent: delta\ndata: two\n\n",
        )

    with _client(handler) as client:
        events = list(client.gateway.create_chat_completion_stream({"model": "m", "messages": []}))
        assert [event.data for event in events] == ["one", "two"]
        assert all(event.event == "delta" for event in events)


def test_stream_ignores_comment_lines_and_flushes_trailing_block_without_terminator():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=":heartbeat\nevent: delta\ndata: only")

    with _client(handler) as client:
        events = list(client.gateway.create_chat_completion_stream({"model": "m", "messages": []}))
        assert [(event.event, event.data) for event in events] == [("delta", "only")]


def test_response_stream_yields_events():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/responses"
        return httpx.Response(200, text="data: chunk\n\n")

    with _client(handler) as client:
        events = list(client.gateway.create_response_stream({"model": "m", "input": "hi"}))
        assert events[0].data == "chunk"


def test_stream_raises_api_error_on_non_success_status():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": {"code": "rate_limited", "message": "slow down"}})

    with _client(handler) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            list(client.gateway.create_chat_completion_stream({"model": "m", "messages": []}))
        assert caught.value.status_code == 429
        assert caught.value.code == "rate_limited"


@pytest.mark.asyncio
async def test_async_create_chat_completion_and_embeddings():
    calls = []

    async def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path == "/v1/chat/completions":
            return httpx.Response(200, json={"id": "chatcmpl_async"})
        return httpx.Response(200, json={"data": [{"embedding": [1.0]}]})

    async with _async_client(handler) as client:
        chat = await client.gateway.create_chat_completion({"model": "m", "messages": []})
        assert chat.data["id"] == "chatcmpl_async"
        embeddings = await client.gateway.create_embeddings({"model": "m", "input": ["a"]})
        assert embeddings.data["data"][0]["embedding"] == [1.0]
    assert calls == ["/v1/chat/completions", "/v1/embeddings"]


@pytest.mark.asyncio
async def test_async_create_response_and_anthropic_message():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/responses":
            return httpx.Response(200, json={"id": "resp_async"})
        return httpx.Response(200, json={"id": "msg_async"})

    async with _async_client(handler) as client:
        response = await client.gateway.create_response({"model": "m", "input": "hi"})
        assert response.data["id"] == "resp_async"
        message = await client.gateway.create_anthropic_message({"model": "m", "max_tokens": 8, "messages": []})
        assert message.data["id"] == "msg_async"


@pytest.mark.asyncio
async def test_async_response_stream_yields_events():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="event: delta\ndata: async-one\n\n")

    async with _async_client(handler) as client:
        events = [event async for event in client.gateway.create_response_stream({"model": "m", "input": "hi"})]
        assert events[0].data == "async-one"
        assert events[0].event == "delta"


@pytest.mark.asyncio
async def test_async_stream_raises_api_error_on_non_success_status():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": {"code": "internal", "message": "boom"}})

    async with _async_client(handler) as client:
        with pytest.raises(OwlVigilApiError) as caught:
            async for _ in client.gateway.create_chat_completion_stream({"model": "m", "messages": []}):
                pass
        assert caught.value.status_code == 500
        assert caught.value.code == "internal"
