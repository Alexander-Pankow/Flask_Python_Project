from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.category import CategoryResponse

class QuestionCreate(BaseModel):
    question: str = Field(..., min_length=10, max_length=100)
    category_id: Optional[int] = Field(None, description="Category ID")

class QuestionResponse(BaseModel):
    id: int
    question: str = Field(..., min_length=10, max_length=100)
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class MessageResponse(BaseModel):
    message: str