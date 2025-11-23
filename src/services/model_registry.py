"""模型注册表，管理所有可用的模型"""
import logging
from typing import Dict, List

from fastapi import HTTPException, status

from src.schemas.models import ModelInfo
from src.services.llm import LLMConnectorFactory

logger = logging.getLogger(__name__)

# 静态模型列表（用于演示或特殊模型）
_STATIC_MODELS: Dict[str, ModelInfo] = {
    model.name: model
    for model in [
        ModelInfo(
            name="nextagent-mini",
            provider="nextagent-lab",
            description="轻量级推理模型，适合快速响应与demo演示。",
            context_length=4096,
            capabilities=["chat", "reasoning"],
        ),
        ModelInfo(
            name="nextagent-pro",
            provider="nextagent-lab",
            description="增强型模型，支持更长上下文与函数调用能力。",
            context_length=16384,
            capabilities=["chat", "reasoning", "function-calling"],
        ),
    ]
}

# 动态模型缓存（从连接器加载）
_DYNAMIC_MODELS: Dict[str, ModelInfo] = {}


async def sync_models_from_connectors() -> None:
    """从所有已注册的连接器同步模型列表"""
    _DYNAMIC_MODELS.clear()

    for provider in LLMConnectorFactory.list_providers():
        try:
            connector = LLMConnectorFactory.get_connector(provider)
            models_data = await connector.list_models()

            for model_data in models_data:
                model_name = model_data.get("name", "")
                if model_name:
                    model_info = ModelInfo(
                        name=model_name,
                        provider=model_data.get("provider", provider),
                        description=model_data.get("description", f"{provider} 模型"),
                        context_length=model_data.get("context_length", 4096),
                        capabilities=model_data.get("capabilities", ["chat"]),
                    )
                    _DYNAMIC_MODELS[model_name] = model_info

            logger.info(f"从 {provider} 同步了 {len(models_data)} 个模型")
        except Exception as e:
            logger.warning(f"从 {provider} 同步模型失败: {e}")


def list_registered_models() -> List[ModelInfo]:
    """
    列出所有已注册的模型（静态 + 动态）

    Returns:
        模型信息列表
    """
    all_models = {**_STATIC_MODELS, **_DYNAMIC_MODELS}
    return list(all_models.values())


def lookup_model(model_name: str) -> ModelInfo:
    """
    查找模型信息

    Args:
        model_name: 模型名称

    Returns:
        模型信息

    Raises:
        HTTPException: 如果模型不存在
    """
    # 先查找静态模型
    model = _STATIC_MODELS.get(model_name)
    if model:
        return model

    # 再查找动态模型
    model = _DYNAMIC_MODELS.get(model_name)
    if model:
        return model

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"模型 {model_name} 不存在",
    )


