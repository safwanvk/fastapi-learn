from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, session_local
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/", response_model=QuestionBase)
def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    choices_out = []
    for choice in question.choices:
        db_choice = models.Choice(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        choices_out.append({
            "choice_text": db_choice.choice_text,
            "is_correct": db_choice.is_correct
        })
        db.add(db_choice)

    db.commit()
    return {
        "question_text": db_question.question_text,
        "choices": choices_out
    }

@app.get("/questions/{question_id}", response_model=QuestionBase)
def read_question(question_id: int, db: db_dependency):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    choices = db.query(models.Choice).filter(models.Choice.question_id == question_id).all()
    choices_out = [{"choice_text": choice.choice_text, "is_correct": choice.is_correct} for choice in choices]

    return {
        "question_text": db_question.question_text,
        "choices": choices_out
    }