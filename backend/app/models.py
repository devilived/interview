"""
Pydantic 数据模型模块 - 定义请求和响应数据结构
"""
from pydantic import BaseModel
from typing import Optional, List


class QuestionResponse(BaseModel):
    """问题响应模型"""
    id: int
    category: str
    question: str
    answer: Optional[str] = None
    source: str
    is_favorited: int


class GenerateRequest(BaseModel):
    """生成问题请求模型"""
    category: str = "Agent"
    count: int = 5


class ResumeGenerateRequest(BaseModel):
    """简历生成问题请求模型"""
    project_description: str
    count: int = 3


class UpdateAnswerRequest(BaseModel):
    """更新答案请求模型"""
    category: str = "Agent"


class FavoriteResponse(BaseModel):
    """收藏操作响应模型"""
    status: str
    message: str


class DeleteResponse(BaseModel):
    """删除操作响应模型"""
    status: str
    message: str


class RegenerateResponse(BaseModel):
    """重新生成答案响应模型"""
    status: str
    answer: str
