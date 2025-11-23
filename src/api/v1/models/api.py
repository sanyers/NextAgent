from typing import Any

from fastapi import APIRouter, Depends

from src.core.security import require_token
from src.services import list_registered_models, lookup_model
from src.services.model_registry import sync_models_from_connectors
from src.utils.response import success

router = APIRouter(prefix="/models", tags=["Models"], dependencies=[Depends(require_token)])


@router.get("/", summary="列出可用模型")
async def list_models() -> dict[str, Any]:
    """返回服务当前注册的所有模型（包括从连接器动态加载的模型）。"""
    return success(data=[model.model_dump() for model in list_registered_models()])


@router.get("/{model_name}", summary="查询模型详情")
async def get_model(model_name: str) -> dict[str, Any]:
    """根据名称获取单个模型的能力描述。"""
    model = lookup_model(model_name)
    return success(data=model.model_dump())


@router.post("/sync", summary="同步模型列表")
async def sync_models() -> dict[str, Any]:
    """从所有已注册的连接器同步模型列表。"""
    await sync_models_from_connectors()
    return success(data={"message": "模型列表已同步"})

