from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import router as v1_router
from src.api.core.config import settings

title = "NextAgent"
version = "0.0.1"
description = "自主Agent API"
# 创建FastAPI应用实例
app = FastAPI(
    title=title,
    description=description,
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
        "description": description,
        "version": version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.server_port, reload=True)
