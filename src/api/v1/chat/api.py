import json
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.core.security import require_token
from src.schemas.chat import ChatCompletionRequest
from src.services import generate_reply, generate_reply_stream
from src.utils.response import success

router = APIRouter(prefix="/chat", tags=["Chat"], dependencies=[Depends(require_token)])


@router.post("/completions", summary="聊天补全接口", response_model=None)
async def create_chat_completion(payload: ChatCompletionRequest) -> dict[str, Any] | StreamingResponse:
    """
    聊天补全接口，支持多种 LLM 提供方（如 Ollama）。
    根据请求中的模型名称自动选择对应的连接器。
    支持流式和非流式两种模式，通过请求中的 stream 参数控制。
    """
    # 如果请求流式输出，返回流式响应
    if payload.stream:
        return StreamingResponse(
            _stream_chat_completion(payload),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    # 非流式响应
    completion = await generate_reply(payload)
    return success(data=completion.model_dump())


async def _stream_chat_completion(payload: ChatCompletionRequest) -> Any:
    """
    流式生成聊天补全响应，使用 Server-Sent Events (SSE) 格式。

    Args:
        payload: 聊天补全请求

    Yields:
        SSE 格式的数据块
    """
    try:
        async for chunk in generate_reply_stream(payload):
            # SSE 格式：data: <content>\n\n
            data = json.dumps({"content": chunk}, ensure_ascii=False)
            yield f"data: {data}\n\n"

        # 发送结束标记
        yield "data: [DONE]\n\n"
    except Exception as e:
        # 发送错误信息
        error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
        yield f"data: {error_data}\n\n"


