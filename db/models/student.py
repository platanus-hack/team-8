# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Libraries Imports

# Local Imports
from .base import Base, students_tests

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)

    # Define the relationship to access tests from a student instance
    test_id = Column(Integer, ForeignKey("test.id"))
    tests = relationship("Test", back_populates="tests")