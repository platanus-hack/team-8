# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Libraries Imports

# Local Imports
from .base import Base, students_tests

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)

    # Define the relationship to access tests from a student instance
    tests = relationship("Test", secondary=students_tests, back_populates="students")