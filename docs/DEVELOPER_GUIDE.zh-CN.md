# OwlVigil Python SDK 开发者文档

> **包名：** `owlvigil` · **Python：** 3.9+ · **版本：** `0.2.0`

本文按照 OwlVigil 其他 SDK 开发者文档的结构组织，但示例全部使用 Python SDK 当前
公开 API。Python SDK 通过 [httpx](https://www.python-httpx.org/) 访问 OwlVigil，
不连接 Dashboard 数据库、Redis 或其他服务端基础设施。

## 1. 接入前先理解两类 API

OwlVigil 将模型调用和管理操作分成两个 API 面：

| API 面 | 默认地址 | 凭证 | 用途 |
| --- | --- | --- | --- |
| Gateway Runtime | `https://gateway.owlvigil.com` | Gateway Key | 模型列表、Chat、Responses、Embeddings、Anthropic Messages |
| Management API | `https://api.owlvigil.com/v1` | Management API Key | 工作区、用量及请求日志 |

两类 Key 不能互换。环境变量 `OWLVIGIL_GATEWAY_KEY` 只用于
`client.gateway`；`OWLVIGIL_API_KEY` 只用于 `client.management`。

## 2. 安装与第一次调用

```bash
pip install owlvigil
```

把 Gateway Key 放到服务端环境变量，不要写入源码、日志或前端代码：

```bash
export OWLVIGIL_GATEWAY_KEY='your-gateway-key'
```

最小同步 Chat Completions 调用：

```python
from owlvigil import OwlVigil

with OwlVigil() as client:
    response = client.gateway.create_chat_completion({
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": "用一句话介绍 OwlVigil。"}],
        "max_tokens": 64,
    })
    print(response.data["choices"][0]["message"]["content"])
    print("request_id=" + response.meta.request_id)
```

原生异步客户端提供相同的 API 面：

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

模型名取决于当前 Workspace、Provider、路由和 Gateway Key。生产代码应先调用
`client.gateway.list_models()`，不要假设示例模型一定可用。

## 3. 客户端与认证配置

### 默认值

`OwlVigil()` / `AsyncOwlVigil()` 使用以下配置：

| 配置 | 默认值 |
| --- | --- |
| Gateway Key | `OWLVIGIL_GATEWAY_KEY` |
| Management API Key | `OWLVIGIL_API_KEY` |
| Gateway Base URL | `https://gateway.owlvigil.com` |
| Management Base URL | `https://api.owlvigil.com/v1` |
| 超时 | 60 秒 |
| 最大重试次数 | 2 |
| User-Agent | `owlvigil-python/<SDK version>` |

构造客户端时不会立即要求两类 Key；只有对应 API 发起请求时才读取并校验对应凭证。
因此只调用 Gateway 时不需要配置 Management Key。

### 显式配置与共享 HTTP 客户端

```python
from owlvigil import OwlVigil

client = OwlVigil(
    gateway_key="replace-with-gateway-key",
    api_key="replace-with-management-key",
    timeout=30.0,
    max_retries=1,
)
```

不要在代码中硬编码真实凭证；从环境变量或服务端密钥管理服务读取后再显式传入。

也可以传入 `gateway_base_url`、`management_base_url` 用于 staging、本地测试或私有
部署，以及一个已有的 `http_client`（`httpx.Client` 或 `httpx.AsyncClient`），
在多个 OwlVigil 客户端之间复用连接池。不要让普通终端用户控制这些地址。

`OwlVigil` 和 `AsyncOwlVigil` 都是上下文管理器。`close()`（或退出 `with` /
`async with` 代码块）只会关闭 SDK 自己创建的 HTTP 客户端；通过 `http_client`
传入的客户端仍然由调用方负责关闭。

## 4. Gateway 模型调用

### 模型发现

```python
with OwlVigil() as client:
    models = client.gateway.list_models()
    for model in models.data["data"]:
        print(model["id"], "owned_by=" + model.get("owned_by", ""))
```

### Chat Completions

请求体是普通字典，因此可以立即使用新的 Provider 字段，无需等待 SDK 发版：

```python
request = {
    "model": "your-model-id",
    "messages": [
        {"role": "system", "content": "回答要简洁。"},
        {"role": "user", "content": "解释什么是幂等请求。"},
    ],
    "temperature": 0.2,
    "max_tokens": 256,
}

result = client.gateway.create_chat_completion(request)
choices = result.data["choices"]
if not choices or not choices[0].get("message"):
    raise RuntimeError(f"empty response: request_id={result.meta.request_id}")
```

实际字段和返回结构以当前 Gateway API 契约为准；不要把示例中的模型名、向量维度
或输出字段当作固定值。

### Responses、Embeddings 和 Anthropic Messages

这些方法接收服务端契约要求的同一种字典结构：

```python
response = client.gateway.create_response({"model": "your-model-id", "input": "总结一下。"})
embeddings = client.gateway.create_embeddings({"model": "embedding-model", "input": ["第一段文本", "第二段文本"]})
anthropic_message = client.gateway.create_anthropic_message({
    "model": "your-model-id",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello"}],
})
```

### SSE 流式响应

`create_chat_completion_stream` 和 `create_response_stream` 会在请求体中设置
`stream: True`，并返回一个（同步或异步）`SseEvent` 迭代器；底层 HTTP 连接由 SDK
负责打开和关闭：

```python
for event in client.gateway.create_chat_completion_stream({
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "从一数到三。"}],
}):
    print("event=" + event.event, "data=" + event.data)
```

```python
async for event in async_client.gateway.create_chat_completion_stream({
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "从一数到三。"}],
}):
    print("event=" + event.event, "data=" + event.data)
```

`event.data` 是未解码的字符串，需按当前 Gateway 契约自行解析。非 2xx 响应会在
产生任何事件之前抛出 `OwlVigilApiError`。网络中断后已产生的事件只能视为部分
结果。

## 5. Management 与工作区

Management API Key 的环境变量：

```bash
export OWLVIGIL_API_KEY='your-management-api-key'
```

先列出当前凭证可访问的工作区，再使用返回的数字 ID：

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

不要从 slug 猜测 ID，也不要默认把列表第一项当成生产工作区；生产系统应使用已验证
的租户映射或显式配置。

`list_workspaces()` 默认请求 50 条；需要分页时使用
`list_workspaces(cursor, limit)`，其中 `limit` 必须为 1 到 100（否则抛出
`ValueError`），cursor 只能原样传回。`get_usage_summary(workspace_id)` 和
`get_request_log(workspace_id, request_id)` 都要求 `workspace_id` 为正数，
`get_request_log` 还要求 `request_id` 非空——参数不合法时会在发起请求前抛出
`ValueError`。

Management 响应会自动拆开 OwlVigil 的 `data` 信封：`response.data` 已经是内层
数据，且当响应头中没有 request ID 时，`response.meta.request_id` 会回退使用
信封里的 `request_id` 字段。Gateway 响应不做这层拆包，原样返回。

## 6. 单次请求选项、返回值与错误

### RequestOptions

Gateway 和 Management 方法都可以传入可选的 `RequestOptions`：

```python
from owlvigil import RequestOptions

options = RequestOptions(
    timeout=20.0,
    max_retries=1,
    idempotency_key="operation-key-v1",
    headers={"X-Correlation-Id": "job-123"},
)
```

SDK 会管理 `Authorization`、`Host`、`Content-Type`、`Content-Length` 和
`Idempotency-Key`；通过 `headers` 设置其中任意一个都会抛出 `OwlVigilError`。
幂等键只应发送给服务端明确支持的写操作；写请求超时后不能仅凭网络错误判断服务端
未执行。

### ApiResponse 和 Request ID

成功调用返回 `ApiResponse`：

```python
response = client.gateway.list_models()
data = response.data
status = response.meta.status_code
request_id = response.meta.request_id
```

空响应体会被解码为 `{}`。排障时保存 request ID、方法、路径、状态码和 UTC
时间，但不要保存认证头、完整凭证或敏感响应正文。

### 异常类型和状态码

```python
from owlvigil import OwlVigilApiError, OwlVigilError

try:
    client.gateway.list_models()
except OwlVigilApiError as error:
    print(f"status={error.status_code} code={error.code} request_id={error.request_id}")
except OwlVigilError:
    ...  # 网络、协议、解码或流式读取失败。
```

| 状态 | 建议 |
| --- | --- |
| 400 / 422 | 修正参数，不重试 |
| 401 | 检查 Key 类型、值、状态和过期时间 |
| 403 | 检查 scope、Workspace 关系和资源权限 |
| 404 | 检查资源 ID、路径和 Workspace |
| 409 | 先读取当前状态，再决定是否写入 |
| 429 | 遵循服务端等待提示并退避 |
| 502 / 503 / 504 | 仅在请求可安全重放时重试 |

SDK 默认只对 GET、HEAD、OPTIONS 以及带幂等键的请求进行自动重试，并针对
408、429、502、503、504 和可重试的传输错误处理：优先使用响应头 `Retry-After`
（数值秒数或 HTTP 日期），否则按指数退避（上限 30 秒，并带抖动）。业务层已有
重试策略时，可将单次请求设为 `RequestOptions(max_retries=0)`，避免重试叠加。

## 7. Webhook 验签

验签必须使用 HTTP 请求体的原始字节，不要先 JSON decode 再重新序列化：

```python
from owlvigil import verify_webhook

raw_body: bytes = request_body_bytes
signature = f"t={timestamp_header},v1={signature_header}"

verify_webhook(raw_body, signature, os.environ["OWLVIGIL_WEBHOOK_SECRET"])
```

OwlVigil 将时间戳和签名分别放在 `OW-Webhook-Timestamp`、
`OW-Webhook-Signature` Header 中；传给 SDK 前组合为
`t=<unix-seconds>,v1=<hex-hmac>`。默认时间容差为 5 分钟，算法为 HMAC-SHA256。
遇到缺失/空 secret、签名格式错误、时间戳过期或签名不匹配时，`verify_webhook`
都会抛出 `OwlVigilError`。

`sign_webhook(payload, timestamp, secret)` 生成同样的 `t=...,v1=...` 格式，
主要用于测试中构造合法签名。

验签通过后再解析和处理事件，并以事件 ID 做持久化去重，因为 Webhook 是至少
一次投递。

## 8. 安全接入检查

- 两类 API Key 分开保存、分开轮换，最小化 scope 和 Workspace 权限。
- Gateway Key 或 Webhook secret 只在创建/轮换响应中返回一次时立即写入密钥管理
  服务。
- 不记录 Authorization、完整凭证、Provider credential、Webhook secret 或
  敏感正文。
- 创建、删除、支付、轮换和重投前确认环境、Workspace、资源 ID 与副作用。
- 始终通过 SDK 提供的迭代器消费流式响应（它会负责关闭底层 HTTP 连接），并为
  关键响应保存 request ID。

## 9. 本地验证与参考

在 Python SDK 仓库执行：

```bash
python -m pip install -e '.[test]'
pytest
python -m build
```

Live 测试默认关闭，只有设置 `OWLVIGIL_LIVE_TEST=1` 并配置真实凭证时才运行，
且只读不写。

HTTP 资源、scope、状态码与公共 envelope 以
[OwlVigil Developer Center](https://github.com/Syrovex/owlvigil_openapi/blob/main/docs/owlvigil-developer-center.md)
和 OpenAPI 规范为准。
