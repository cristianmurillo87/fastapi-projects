from typing import Annotated

from app.config.databases.postgres import get_db
from app.models.questions import Choices, QuestionBase, Questions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = Choices(**dict(choice), question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Questions).all()


@router.get("/questions/{question_id}", status_code=status.HTTP_200_OK)
async def read_question(question_id: int, db: db_dependency):
    result = db.query(Questions).filter(Questions.id == question_id).first()
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Question with id {question_id} not found."
        )
    return result


@router.get("/choices/{question_id}", status_code=status.HTTP_200_OK)
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(Choices).filter(Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No choices for question with id {question_id} could be found.",
        )
    return result
