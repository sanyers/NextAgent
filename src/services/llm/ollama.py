"""Ollama LLM 连接器实现"""
import logging
from collections.abc import AsyncGenerator
from typing import Any

import httpx

from src.schemas.chat import ChatCompletionRequest, ChatCompletionResponse, ChatMessage
from src.services.llm.base import LLMConnector

logger = logging.getLogger(__name__)


class OllamaConnector(LLMConnector):
    """Ollama 连接器实现"""

    def __init__(self, config: dict[str, Any]) -> None:
        """
        初始化 Ollama 连接器

        Args:
            config: 配置字典，应包含：
                - base_url: Ollama 服务地址，默认 "http://localhost:11434"
                - timeout: 请求超时时间（秒），默认 60
        """
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.timeout = config.get("timeout", 60)
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        """获取或创建 HTTP 客户端"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        """关闭连接器，释放资源"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def get_provider_name(self) -> str:
        """获取提供方名称"""
        return "ollama"

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
        client = self._get_client()

        # 转换消息格式为 Ollama API 格式
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # 构建请求体
        payload = {
            "model": request.model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = await client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

            # 解析响应
            assistant_message = ChatMessage(
                role="assistant",
                content=data.get("message", {}).get("content", ""),
            )

            from datetime import datetime

            return ChatCompletionResponse(
                model=data.get("model", request.model),
                created_at=datetime.utcnow(),
                reply=assistant_message,
                total_messages=len(request.messages) + 1,
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API 请求失败: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Ollama 连接器错误: {str(e)}")
            raise

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
        client = self._get_client()

        # 转换消息格式为 Ollama API 格式
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # 构建请求体
        payload = {
            "model": request.model,
            "messages": messages,
            "stream": True,
        }

        try:
            async with client.stream("POST", "/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        # Ollama 流式响应是每行一个 JSON 对象
                        import json

                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                            # 检查是否完成
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API 流式请求失败: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Ollama 连接器流式错误: {str(e)}")
            raise

    async def list_models(self) -> list[dict[str, Any]]:
        """
        列出可用的模型列表

        Returns:
            模型信息列表
        """
        client = self._get_client()

        try:
            response = await client.get("/api/tags")
            response.raise_for_status()
            data = response.json()

            models = []
            for model_info in data.get("models", []):
                models.append(
                    {
                        "name": model_info.get("name", ""),
                        "provider": "ollama",
                        "description": f"Ollama 模型: {model_info.get('name', '')}",
                        "context_length": model_info.get("size", 0),  # Ollama 可能不提供此信息
                        "capabilities": ["chat"],
                    }
                )
            return models
        except httpx.HTTPStatusError as e:
            logger.error(f"获取 Ollama 模型列表失败: {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"获取 Ollama 模型列表错误: {str(e)}")
            return []

    async def health_check(self) -> bool:
        """
        检查连接器健康状态

        Returns:
            是否健康可用
        """
        client = self._get_client()

        try:
            response = await client.get("/api/tags", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False

