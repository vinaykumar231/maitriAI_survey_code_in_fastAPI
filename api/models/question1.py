from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Question1(Base):
    __tablename__ = 'questions1'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(255), index=True)
    option1_text = Column(String(255))
   
    option2_text = Column(String(255))
    
    option3_text = Column(String(255))

    option1_selected_count = Column(Integer, default=0)
    option2_selected_count = Column(Integer, default=0)
    option3_selected_count = Column(Integer, default=0)