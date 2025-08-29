from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description='Question id')
    is_agree: bool = Field(..., description='Agree/Disagree')


class StaticResponse(BaseModel):
    question_id: int
    agree_count: int = Field(..., ge=0, description='Agree Count')
    disagree_count: int = Field(..., ge=0, description='Disagree Count')