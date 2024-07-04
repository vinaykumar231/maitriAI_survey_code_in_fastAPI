from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .question import Question

class Answer(Base):
    __tablename__ = 'answers'

    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    option_number = Column(Integer)  # 1, 2, or 3
    given_answer = Column(String(255))

    question = relationship("Question", back_populates="answers")

