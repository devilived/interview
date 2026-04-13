from pydantic import BaseModel
from typing import Optional


class QuestionCreate(BaseModel):
    category: str
    question: str
    answer: Optional[str] = None
    source: str = "generated"
    resume_id: Optional[str] = None


class QuestionResponse(BaseModel):
    id: int
    category: str
    question: str
    answer: Optional[str]
    source: str
    is_favorited: int

    class Config:
        from_attributes = True


class GenerateRequest(BaseModel):
    category: str
    count: int = 5


class ResumeGenerateRequest(BaseModel):
    project_description: str
    count: int = 3


class UpdateAnswerRequest(BaseModel):
    answer: str
