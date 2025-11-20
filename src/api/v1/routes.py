"""
API v1 路由和测试接口
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["v1"])


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    timestamp: str
    version: str


class TestResponse(BaseModel):
    """测试接口响应模型"""
    message: str
    data: Dict[str, Any]
    timestamp: str


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health_check():
    """
    健康检查接口
    
    用于检查服务是否正常运行
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="0.1.0"
    )


@router.get("/test", response_model=TestResponse, summary="基础测试接口")
async def test_endpoint():
    """
    基础测试接口
    
    返回测试数据，验证API正常工作
    """
    return TestResponse(
        message="API测试成功",
        data={
            "service": "NextAgent",
            "endpoint": "/api/v1/test"
        },
        timestamp=datetime.now().isoformat()
    )


@router.get("/info", response_model=Dict[str, Any], summary="服务信息")
async def get_info():
    """
    获取服务信息
    
    返回项目的详细信息
    """
    return {
        "name": "NextAgent",
        "description": "自主Agent研究项目",
        "version": "0.1.0",
        "api_version": "v1",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/api/v1/health",
            "test": "/api/v1/test",
            "info": "/api/v1/info",
            "echo": "/api/v1/echo"
        }
    }


@router.post("/echo", response_model=Dict[str, Any], summary="回显接口")
async def echo(data: Dict[str, Any]):
    """
    回显接口
    
    接收POST请求的数据并原样返回，用于测试数据传输
    """
    return {
        "echo": data,
        "timestamp": datetime.now().isoformat(),
        "message": "数据接收成功"
    }

