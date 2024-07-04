from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.question import Question
from database import SessionLocal
from database import get_db
from ..scheema import QuestionCreate, QuestionWithAnswers,QuestionCreate1,AnswerCreate1
from datetime import datetime, timedelta
from sqlalchemy import func
from ..models.answer import Answer
from ..models.question1 import Question1
from sqlalchemy import desc

router = APIRouter()

# @router.post("/questions/", response_model=None)
# def create_question(question_data: QuestionWithAnswers, db: Session = Depends(get_db)):
#     db_question = Question(
#         question_text=question_data.question_text,
#         option1_text=question_data.option1_text,
#         option2_text=question_data.option2_text,
#         option3_text=question_data.option3_text
#     )
#     db.add(db_question)
#     db.flush()  # This assigns an ID to db_question

#     for answer in question_data.answers:
#         db_answer = Answer(
#             question_id=db_question.question_id,
#             option_number=answer.option_number,
#             given_answer=answer.given_answer
#         )
#         db.add(db_answer)

#     db.commit()
#     db.refresh(db_question)
#     return db_question

# @router.get("/questions/{question_id}", response_model=None)
# def read_question(question_id: int, db: Session = Depends(get_db)):
#     db_question = db.query(Question).filter(Question.question_id == question_id).first()
#     if db_question is None:
#         raise HTTPException(status_code=404, detail="Question not found")
#     return db_question

# @router.get("/questions/{question_id}/options", response_model=None)
# def get_question_options(question_id: int, db: Session = Depends(get_db)):
#     question = db.query(Question).filter(Question.question_id == question_id).first()
#     if not question:
#         raise HTTPException(status_code=404, detail="Question not found")
#     all_options=[]
#     options = {
#         "option1_text": question.option1_text,
#         "option2_text": question.option2_text,
#         "option3_text": question.option3_text
#     }
#     all_options.append(options)
#     return all_options


# @router.get("/dashboard_counts", response_model=None)
# async def get_dashboard_counts(db: Session = Depends(get_db)):
#     total_questions = db.query(Question).count()
    
#     total_answers = db.query(Answer).count()
    
#     questions_with_answers = db.query(Question.question_id).join(Answer).distinct().count()
    
#     questions_without_answers = total_questions - questions_with_answers
    
#     most_answered_question_id = db.query(Answer.question_id, func.count(Answer.answer_id).label('answer_count')) \
#                                   .group_by(Answer.question_id) \
#                                   .order_by(func.count(Answer.answer_id).desc()) \
#                                   .first()
    
#     most_answered_count = most_answered_question_id[1] if most_answered_question_id else 0

#     # Count answers for each option
#     option1_answers = db.query(Answer).filter(Answer.option_number == 1).count()
#     option2_answers = db.query(Answer).filter(Answer.option_number == 2).count()
#     option3_answers = db.query(Answer).filter(Answer.option_number == 3).count()

#     return {
#         "total_questions": total_questions,
#         "total_answers": total_answers,
#         "questions_with_answers": questions_with_answers,
#         "questions_without_answers": questions_without_answers,
#         "most_answered_count": most_answered_count,
#         "option1_answers": option1_answers,
#         "option2_answers": option2_answers,
#         "option3_answers": option3_answers
#     }

#################################################
def create_question_db(db: Session, question: QuestionCreate1):
    db_question = Question1(**question.dict(),
                                  option1_selected_count=0,
                                  option2_selected_count=0,
                                  option3_selected_count=0)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question_db(db: Session, question_id: int):
    return db.query(Question1).filter(Question1.id == question_id).first()

def answer_question_db(db: Session, question_id: int, answer: AnswerCreate1):
    db_question = get_question_db(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if answer.selected_option not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid option selected")
    
    # Increment the count for the selected option
    if answer.selected_option == 1:
        db_question.option1_selected_count += 1
    elif answer.selected_option == 2:
        db_question.option2_selected_count += 1
    elif answer.selected_option == 3:
        db_question.option3_selected_count += 1
    
    db.commit()
    db.refresh(db_question)
    return db_question

# Route functions
@router.post("/questions/", response_model=None)
def create_question(question: QuestionCreate1, db: Session = Depends(get_db)):
    return create_question_db(db=db, question=question)

@router.post("/questions/{question_id}/answer", response_model=None)
def answer_question(question_id: int, answer: AnswerCreate1, db: Session = Depends(get_db)):
    return answer_question_db(db=db, question_id=question_id, answer=answer)

@router.get("/questions/{question_id}", response_model=None)
def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question_db(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.get("/dashboard", response_model=None)
def get_dashboard(db: Session = Depends(get_db)):
    # Total number of questions
    total_questions = db.query(func.count(Question1.id)).scalar()

    # Total number of answers (sum of all selected counts)
    total_answers = db.query(func.sum(
        Question1.option1_selected_count + 
        Question1.option2_selected_count + 
        Question1.option3_selected_count
    )).scalar()

    # Questions with at least one answer
    questions_with_answers = db.query(func.count(Question1.id)).filter(
        (Question1.option1_selected_count > 0) |
        (Question1.option2_selected_count > 0) |
        (Question1.option3_selected_count > 0)
    ).scalar()

    # Questions without answers
    questions_without_answers = total_questions - questions_with_answers

    # Most answered question
    most_answered_question = db.query(
        Question1.id,
        (Question1.option1_selected_count + 
         Question1.option2_selected_count + 
         Question1.option3_selected_count).label('total_answers')
    ).order_by(desc('total_answers')).first()  # Corrected usage of desc()

    most_answered_count = most_answered_question.total_answers if most_answered_question else 0

    # Total counts for each option
    option1_total = db.query(func.sum(Question1.option1_selected_count)).scalar() or 0
    option2_total = db.query(func.sum(Question1.option2_selected_count)).scalar() or 0
    option3_total = db.query(func.sum(Question1.option3_selected_count)).scalar() or 0

    return {
        "total_questions": total_questions,
        "total_answers": total_answers or 0,  # In case there are no answers yet
        "questions_with_answers": questions_with_answers,
        "questions_without_answers": questions_without_answers,
        "most_answered_count": most_answered_count,
        "option1_total_selections": option1_total,
        "option2_total_selections": option2_total,
        "option3_total_selections": option3_total
    }
