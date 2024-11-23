# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship

# Libraries Imports
import enum

# Local Imports
from .base import Base


class Guideline(Base):
    __tablename__ = "guidelines"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    max_score =  Column(Integer)

    test_id = Column(Integer, ForeignKey("tests.id"))
    tests = relationship("Test", back_populates="tests")    
   
    question_id = Column(Integer, ForeignKey("questions.id"))
    questions = relationship("Question", back_populates="questions")    
   
    question_id = Column(Integer, ForeignKey("questions.id"))
    questions = relationship("Question", back_populates="questions")    
