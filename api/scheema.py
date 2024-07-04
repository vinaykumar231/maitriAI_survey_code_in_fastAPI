from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, List

class QuestionCreate(BaseModel):
    question_text: str
    option1_text: Optional[str] = None
    option2_text: Optional[str] = None
    option3_text: Optional[str] = None
    option1_given_ans: Optional[str] = None
    option2_given_ans: Optional[str] = None
    option3_given_ans: Optional[str] = None

class QuestionCreate(BaseModel):
    question_text: str
    option1_text: str
    option2_text: str
    option3_text: str

class AnswerCreate(BaseModel):
    option_number: int
    given_answer: str

class QuestionWithAnswers(QuestionCreate):
    answers: List[AnswerCreate]


####
class QuestionCreate1(BaseModel):
    question_text: str
    option1_text: str
    option2_text: str
    option3_text: str



class AnswerCreate1(BaseModel):
    selected_option: int