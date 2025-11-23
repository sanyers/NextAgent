from typing import List

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    name: str = Field(..., description="模型唯一名称")
    provider: str = Field(..., description="模型提供方")
    description: str = Field(..., description="模型描述")
    context_length: int = Field(..., ge=512, description="最大上下文长度")
    capabilities: List[str] = Field(default_factory=list, description="能力标签")


