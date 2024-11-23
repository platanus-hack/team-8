# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship

# Libraries Imports
import enum

# Local Imports
from .base import Base, students_tests


class Test(Base):
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    max_score =  Column(Integer)
    student_score =  Column(Integer)
    

    student_id = Column(Integer, ForeignKey("students.id"))
    students = relationship("Student", secondary=students_tests, back_populates="tests")    
