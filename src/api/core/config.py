from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 服务端口
    server_port: int = Field(default=8100, alias="SERVER_PORT")
    # 密钥
    secret_key: str = Field(default="change_me_please", alias="SECRET_KEY")

    # SQLite 配置
    sqlite_db_path: str = Field(default="./data/data.db", alias="SQLITE_DB_PATH")

    model_config = {
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
