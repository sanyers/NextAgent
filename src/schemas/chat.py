from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(default="user", description="消息角色")
    content: str = Field(..., min_length=1, max_length=2000, description="消息内容")


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="nextagent-mock", description="期望使用的模型名称")
    messages: List[ChatMessage] = Field(..., min_length=1, description="按顺序排列的历史消息")
    stream: bool = Field(default=False, description="是否以流式方式返回")

    @field_validator("messages")
    @classmethod
    def ensure_messages_not_empty(cls, value: List[ChatMessage]) -> List[ChatMessage]:
        if not value:
            raise ValueError("messages 不能为空")
        return value


class ChatCompletionResponse(BaseModel):
    model: str
    created_at: datetime
    reply: ChatMessage
    total_messages: int


