from pydantic import BaseModel, Field, ConfigDict
from app.schemas.category import CategoryResponse


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, description="Category name")

class QuestionCreate(BaseModel):
    question: str = Field(..., min_length=10, max_length=100)
    category_id: int = Field(..., description="Category ID")

class QuestionResponse(BaseModel):
    id: int
    question: str = Field(..., min_length=10, max_length=100)
    category: CategoryResponse = Field(...)

    model_config = ConfigDict(
        from_attributes=True
    )



class MessageResponse(BaseModel):
    message: str