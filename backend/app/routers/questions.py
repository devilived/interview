from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from ..database import get_db, Question, init_db
from ..models import (
    QuestionResponse,
    GenerateRequest,
    QuestionCreate,
    UpdateAnswerRequest,
)
from ..chains import generate_questions, regenerate_answer
from ..vector_db import add_question, delete_question, update_question

router = APIRouter(prefix="/api/questions", tags=["questions"])

init_db()


@router.get("", response_model=List[QuestionResponse])
def get_questions(
    category: str = "Agent", limit: int = 5, db: Session = Depends(get_db)
):
    questions = (
        db.query(Question)
        .filter(Question.category == category, Question.is_favorited == 1)
        .order_by(Question.id)
        .limit(limit)
        .all()
    )

    if not questions:
        return []

    random.shuffle(questions)
    return questions[:limit]


@router.post("/generate", response_model=List[QuestionResponse])
def generate_new_questions(req: GenerateRequest, db: Session = Depends(get_db)):
    new_questions = generate_questions(req.category, req.count)

    result = []
    for q in new_questions:
        db_question = Question(
            category=req.category,
            question=q["question"],
            answer=q["answer"],
            source="generated",
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
def favorite_question(question_id: int, db: Session = Depends(get_db)):
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
def delete_question_by_id(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    delete_question(question_id)

    return {"status": "success", "message": "Question deleted"}


@router.put("/{question_id}/regenerate")
def regenerate_question_answer(
    question_id: int, req: UpdateAnswerRequest, db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_answer = regenerate_answer(question.question, question.category)

    question.answer = new_answer
    db.commit()

    update_question(
        question.id, question.question, new_answer, question.category, question.source
    )

    return {"status": "success", "answer": new_answer}
