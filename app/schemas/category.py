from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, description="Category name")

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True