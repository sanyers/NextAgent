"""LLM 连接器工厂和注册机制"""
import logging
from typing import Any

from src.core.config import settings
from src.services.llm.base import LLMConnector
from src.services.llm.ollama import OllamaConnector

logger = logging.getLogger(__name__)


class LLMConnectorFactory:
    """LLM 连接器工厂类，负责创建和管理连接器实例"""

    _connectors: dict[str, LLMConnector] = {}
    _connector_configs: dict[str, dict[str, Any]] = {}

    @classmethod
    def register_connector(
        cls, provider: str, connector_class: type[LLMConnector], config: dict[str, Any]
    ) -> None:
        """
        注册连接器

        Args:
            provider: 提供方名称，如 "ollama"
            connector_class: 连接器类
            config: 连接器配置
        """
        cls._connector_configs[provider] = {
            "class": connector_class,
            "config": config,
        }
        logger.info(f"已注册 LLM 连接器: {provider}")

    @classmethod
    def get_connector(cls, provider: str) -> LLMConnector:
        """
        获取连接器实例（单例模式）

        Args:
            provider: 提供方名称

        Returns:
            连接器实例

        Raises:
            ValueError: 如果提供方未注册
        """
        if provider not in cls._connector_configs:
            raise ValueError(f"未注册的连接器提供方: {provider}")

        # 如果已创建实例，直接返回
        if provider in cls._connectors:
            return cls._connectors[provider]

        # 创建新实例
        connector_info = cls._connector_configs[provider]
        connector_class = connector_info["class"]
        config = connector_info["config"]

        connector = connector_class(config)
        cls._connectors[provider] = connector
        logger.info(f"已创建连接器实例: {provider}")

        return connector

    @classmethod
    def list_providers(cls) -> list[str]:
        """
        列出所有已注册的提供方

        Returns:
            提供方名称列表
        """
        return list(cls._connector_configs.keys())

    @classmethod
    async def close_all(cls) -> None:
        """关闭所有连接器，释放资源"""
        for provider, connector in cls._connectors.items():
            if hasattr(connector, "close"):
                try:
                    await connector.close()
                except Exception as e:
                    logger.error(f"关闭连接器 {provider} 时出错: {e}")
        cls._connectors.clear()


def get_connector(provider: str) -> LLMConnector:
    """
    便捷函数：获取连接器实例

    Args:
        provider: 提供方名称

    Returns:
        连接器实例
    """
    return LLMConnectorFactory.get_connector(provider)


def initialize_connectors() -> None:
    """初始化所有连接器（从配置中读取）"""
    # 注册 Ollama 连接器
    ollama_config = {
        "base_url": settings.ollama_base_url,
        "timeout": settings.ollama_timeout,
    }
    LLMConnectorFactory.register_connector("ollama", OllamaConnector, ollama_config)

    logger.info("LLM 连接器初始化完成")


# 在模块导入时自动初始化
initialize_connectors()

