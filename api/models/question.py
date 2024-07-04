from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import shutil
import uuid
import os
from database import Base


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True)
    question_text = Column(String(255))
   
    option1_text = Column(String(255))
   
    option2_text = Column(String(255))
    
    option3_text = Column(String(255))

    

    answers = relationship("Answer", back_populates="question")
    
   
    
    
    
   
    