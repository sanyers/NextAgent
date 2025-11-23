from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 服务端口
    server_port: int = Field(default=8000, alias="SERVER_PORT")
    # 密钥
    secret_key: str = Field(default="", alias="SECRET_KEY")
    # 静态资源目录（用于前端构建产物）
    static_assets_dir: str = Field(default="./web", alias="STATIC_ASSETS_DIR")

    # SQLite 配置
    sqlite_db_path: str = Field(default="./data/data.db", alias="SQLITE_DB_PATH")

    # Ollama 配置
    ollama_base_url: str = Field(
        default="http://localhost:11434", alias="OLLAMA_BASE_URL"
    )
    ollama_timeout: int = Field(default=60, alias="OLLAMA_TIMEOUT")

    model_config = {
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
