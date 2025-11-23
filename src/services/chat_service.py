"""聊天服务，负责调用 LLM 连接器生成回复"""
import logging
from collections.abc import AsyncGenerator
from typing import Any

from src.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from src.services.llm import get_connector
from src.services.model_registry import lookup_model

logger = logging.getLogger(__name__)


async def generate_reply(payload: ChatCompletionRequest) -> ChatCompletionResponse:
    """
    根据请求生成 LLM 回复。

    Args:
        payload: 聊天补全请求

    Returns:
        聊天补全响应

    Raises:
        ValueError: 如果模型未找到或连接器不可用
    """
    # 查找模型信息
    try:
        model_info = lookup_model(payload.model)
        provider = model_info.provider
    except Exception as e:
        logger.error(f"查找模型失败: {e}")
        raise ValueError(f"模型 {payload.model} 不存在或未注册")

    # 获取对应的连接器
    try:
        connector = get_connector(provider)
    except ValueError as e:
        logger.error(f"获取连接器失败: {e}")
        raise ValueError(f"无法获取提供方 {provider} 的连接器")

    # 检查连接器健康状态
    is_healthy = await connector.health_check()
    if not is_healthy:
        logger.warning(f"连接器 {provider} 健康检查失败，尝试继续使用")

    # 非流式调用
    return await connector.chat_completion(payload)


async def generate_reply_stream(
    payload: ChatCompletionRequest,
) -> AsyncGenerator[str, None]:
    """
    根据请求生成 LLM 回复（流式）。

    Args:
        payload: 聊天补全请求

    Yields:
        流式返回的文本片段

    Raises:
        ValueError: 如果模型未找到或连接器不可用
    """
    # 查找模型信息
    try:
        model_info = lookup_model(payload.model)
        provider = model_info.provider
    except Exception as e:
        logger.error(f"查找模型失败: {e}")
        raise ValueError(f"模型 {payload.model} 不存在或未注册")

    # 获取对应的连接器
    try:
        connector = get_connector(provider)
    except ValueError as e:
        logger.error(f"获取连接器失败: {e}")
        raise ValueError(f"无法获取提供方 {provider} 的连接器")

    # 检查连接器健康状态
    is_healthy = await connector.health_check()
    if not is_healthy:
        logger.warning(f"连接器 {provider} 健康检查失败，尝试继续使用")

    # 流式调用
    async for chunk in connector.chat_completion_stream(payload):
        yield chunk


