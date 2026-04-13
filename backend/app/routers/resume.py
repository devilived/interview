"""
简历面试 API 路由模块
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db, Question, init_db
from ..models import QuestionResponse, ResumeGenerateRequest
from ..chains import generate_resume_questions
from ..vector_db import add_question, delete_question

router = APIRouter(prefix="/api/resume", tags=["resume"])

init_db()


@router.post("/generate", response_model=List[QuestionResponse])
def generate_resume_questions_api(
    req: ResumeGenerateRequest, db: Session = Depends(get_db)
):
    """
    根据项目描述生成面试问题

    Args:
        req: 包含项目描述和生成数量的请求
        db: 数据库会话

    Returns:
        生成的问题列表
    """
    resume_id = str(uuid.uuid4())

    new_questions = generate_resume_questions(req.project_description, req.count)

    result = []
    for q in new_questions:
        db_question = Question(
            category="Resume",
            question=q["question"],
            answer=q["answer"],
            source="resume",
            resume_id=resume_id,
            is_favorited=0,
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        result.append(
            QuestionResponse(
                id=db_question.id,
                category=db_question.category,
                question=db_question.question,
                answer=db_question.answer,
                source=db_question.source,
                is_favorited=db_question.is_favorited,
            )
        )

    return result


@router.post("/{resume_id}/followup", response_model=List[QuestionResponse])
def generate_followup_questions(
    resume_id: str, req: ResumeGenerateRequest, db: Session = Depends(get_db)
):
    """
    生成追问问题 (深挖或扩展)

    Args:
        resume_id: 简历ID
        req: 包含项目描述和生成数量的请求
        db: 数据库会话

    Returns:
        生成的问题列表
    """
    previous_questions = (
        db.query(Question)
        .filter(Question.resume_id == resume_id)
        .all()
    )

    history = [
        {"question": q.question, "answer": q.answer}
        for q in previous_questions
    ]

    new_questions = generate_resume_questions(
        req.project_description, req.count, history
    )

    result = []
    for q in new_questions:
        db_question = Question(
            category="Resume",
            question=q["question"],
            answer=q["answer"],
            source="resume",
            resume_id=resume_id,
            is_favorited=0,
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        result.append(
            QuestionResponse(
                id=db_question.id,
                category=db_question.category,
                question=db_question.question,
                answer=db_question.answer,
                source=db_question.source,
                is_favorited=db_question.is_favorited,
            )
        )

    return result


@router.post("/{question_id}/favorite")
def favorite_resume_question(question_id: int, db: Session = Depends(get_db)):
    """
    收藏简历面试问题

    Args:
        question_id: 问题ID
        db: 数据库会话

    Returns:
        操作结果
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question.is_favorited = 1
    db.commit()

    add_question(
        question.id,
        question.question,
        question.answer or "",
        question.category,
        question.source,
    )

    return {"status": "success", "message": "Question favorited"}


@router.delete("/{question_id}")
def delete_resume_question(question_id: int, db: Session = Depends(get_db)):
    """
    删除简历面试问题

    Args:
        question_id: 问题ID
        db: 数据库会话

    Returns:
        操作结果
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    delete_question(question_id)

    return {"status": "success", "message": "Question deleted"}
