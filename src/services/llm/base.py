"""LLM 连接器抽象基类"""
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from src.schemas.chat import ChatCompletionRequest, ChatCompletionResponse


class LLMConnector(ABC):
    """LLM 连接器抽象基类，定义所有 LLM 连接器必须实现的接口"""

    def __init__(self, config: dict[str, Any]) -> None:
        """
        初始化连接器

        Args:
            config: 连接器配置字典
        """
        self.config = config

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        获取提供方名称

        Returns:
            提供方名称，如 "ollama", "openai" 等
        """
        pass

    @abstractmethod
    async def chat_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """
        执行聊天补全（非流式）

        Args:
            request: 聊天补全请求

        Returns:
            聊天补全响应
        """
        pass

    @abstractmethod
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, None]:
        """
        执行聊天补全（流式）

        Args:
            request: 聊天补全请求

        Yields:
            流式返回的文本片段
        """
        pass

    @abstractmethod
    async def list_models(self) -> list[dict[str, Any]]:
        """
        列出可用的模型列表

        Returns:
            模型信息列表
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        检查连接器健康状态

        Returns:
            是否健康可用
        """
        pass

