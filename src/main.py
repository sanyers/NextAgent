import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.api.v1 import router as v1_router
from src.core.config import settings
from src.services.llm import LLMConnectorFactory
from src.services.model_registry import sync_models_from_connectors

logger = logging.getLogger(__name__)

title = "NextAgent"
version = "0.0.1"
description = "自主Agent API"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期管理
    启动时执行初始化，关闭时执行清理
    """
    # 启动时执行
    logger.info("应用启动中...")
    try:
        await sync_models_from_connectors()
        logger.info("模型列表同步完成")
    except Exception as e:
        logger.warning(f"模型列表同步失败: {e}")

    yield

    # 关闭时执行
    logger.info("应用关闭中...")
    await LLMConnectorFactory.close_all()
    logger.info("连接器已关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title=title,
    description=description,
    version=version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(settings.static_assets_dir).resolve()
index_file = static_dir / "index.html"
serve_frontend = index_file.is_file()


def _safe_static_file(sub_path: str) -> Optional[Path]:
    """防止目录遍历，返回静态资源文件路径"""
    target = (static_dir / sub_path).resolve()
    try:
        target.relative_to(static_dir)
    except ValueError:
        return None
    return target if target.is_file() else None


# 注册API路由
app.include_router(v1_router)


if serve_frontend:

    @app.get("/", include_in_schema=False)
    async def serve_frontend_root():
        """返回Vue构建后的首页"""
        return FileResponse(index_file)

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend_path(full_path: str):
        """支持Vue Router history模式的静态资源访问"""
        file_path = _safe_static_file(full_path)
        if file_path:
            return FileResponse(file_path)
        return FileResponse(index_file)

else:

    @app.get("/", tags=["根路径"])
    async def root():
        """根路径接口"""
        return {
            "description": description,
            "version": version,
            "docs": "/docs",
            "redoc": "/redoc",
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.server_port, reload=True)

