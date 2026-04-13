from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import uuid

from ..database import get_db, Question
from ..models import QuestionResponse, ResumeGenerateRequest, QuestionCreate
from ..chains import generate_resume_questions
from ..vector_db import add_question, delete_question

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post("/generate", response_model=List[QuestionResponse])
def generate_resume_questions_api(
    req: ResumeGenerateRequest, db: Session = Depends(get_db)
):
    resume_id = str(uuid.uuid4())[:8]

    new_questions = generate_resume_questions(req.project_description, req.count)

    result = []
    for q in new_questions:
        db_question = Question(
            category="resume",
            question=q["question"],
            answer=q["answer"],
            source="generated",
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
def generate_followup(
    resume_id: str, req: ResumeGenerateRequest, db: Session = Depends(get_db)
):
    previous = db.query(Question).filter(Question.resume_id == resume_id).all()
    history = [{"question": q.question, "answer": q.answer} for q in previous]

    new_questions = generate_resume_questions(
        req.project_description, req.count, history
    )

    result = []
    for q in new_questions:
        db_question = Question(
            category="resume",
            question=q["question"],
            answer=q["answer"],
            source="generated",
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


@router.get("/{resume_id}", response_model=List[QuestionResponse])
def get_resume_questions(resume_id: str, limit: int = 3, db: Session = Depends(get_db)):
    questions = (
        db.query(Question)
        .filter(Question.resume_id == resume_id, Question.is_favorited == 1)
        .limit(limit)
        .all()
    )

    return questions
