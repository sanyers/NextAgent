"""
NextAgent FastAPI应用入口
"""

import sys
from pathlib import Path

# 将项目根目录添加到Python路径，以支持绝对导入
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import router as v1_router

title = "NextAgent"
version = "0.0.1"
# 创建FastAPI应用实例
app = FastAPI(
    title=title,
    description="自主Agent API",
    version=version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(v1_router)


@app.get("/", tags=["根路径"])
async def root():
    """根路径接口"""
    return {
        "message": "Welcome to NextAgent API",
        "version": version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
