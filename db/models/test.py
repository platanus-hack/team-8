# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship

# Libraries Imports
import enum

# Local Imports
from .base import Base, students_tests


# Define the enumeration
class TestStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Define the enumeration
class TestTopics(enum.Enum):
    SCIENCE = "SCIENCE"
    MATHEMATICS = "MATHEMATICS"
    LANGUAGE = "LANGUAGE"
    HISTORY = "HISTORY"

class Test(Base):
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    topic =  Column(Enum(TestTopics), nullable=False)
    max_score =  Column(Integer, nullable=False)
    student_score =  Column(Integer)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status =  Column(Enum(TestStatus), nullable=False)
    

    student_id = Column(Integer, ForeignKey("students.id"))
    students = relationship("Student", secondary=students_tests, back_populates="tests")    
