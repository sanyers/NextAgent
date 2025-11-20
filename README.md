# NextAgent

自主Agent

## 项目简介

NextAgent 是一个基于 FastAPI 的自主 Agent，提供了完整的 RESTful API 接口。

## 项目结构

```
NextAgent/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── routes.py    # API v1 路由和测试接口
├── requirements.txt         # Python 依赖包
├── README.md               # 项目说明文档
└── LICENSE                 # 许可证文件
```

## 安装依赖

```bash
# 建议使用虚拟环境
conda create -n nextagent python=3.10.16
conda activate nextagent

pip install -r requirements.txt
```

## 运行项目

### 方式一：直接运行

```bash
python src/main.py
```

### 方式二：使用 uvicorn 命令

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问以下地址：

- API 文档（Swagger UI）: http://localhost:8000/docs
- API 文档（ReDoc）: http://localhost:8000/redoc
- 根路径: http://localhost:8000/

## API 接口说明

### 基础接口

- `GET /` - 根路径，返回欢迎信息
- `GET /api/v1/health` - 健康检查接口
- `GET /api/v1/test` - 基础测试接口
- `GET /api/v1/info` - 获取服务信息
- `POST /api/v1/echo` - 回显接口，用于测试数据传输

### 接口示例

#### 1. 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

响应：
```json
{
  "status": "healthy",
  "timestamp": "2025-11-20T19:05:00",
  "version": "0.1.0"
}
```

#### 2. 基础测试

```bash
curl http://localhost:8000/api/v1/test
```

响应：
```json
{
  "message": "API测试成功",
  "data": {
    "service": "NextAgent",
    "endpoint": "/api/v1/test"
  },
  "timestamp": "2025-11-20T19:05:00"
}
```

#### 3. 获取服务信息

```bash
curl http://localhost:8000/api/v1/info
```

#### 4. 回显接口

```bash
curl -X POST http://localhost:8000/api/v1/echo \
  -H "Content-Type: application/json" \
  -d '{"key": "value", "test": "data"}'
```

## 开发说明

### 添加新的 API 接口

在 `src/api/v1/routes.py` 文件中添加新的路由处理函数，例如：

```python
@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "新的接口"}
```

### 添加新的 API 版本

1. 创建新的版本目录，如 `src/api/v2/`
2. 在新目录中创建路由文件
3. 在 `src/main.py` 中注册新版本的路由

## 技术栈

- **FastAPI**: 现代化的 Python Web 框架
- **Uvicorn**: ASGI 服务器
- **Pydantic**: 数据验证和序列化

## 许可证

详见 LICENSE 文件
