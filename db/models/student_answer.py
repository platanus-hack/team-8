from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class StudentAnswer(Base):
    __tablename__ = "students_answers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    guideline_answer = Column(String, nullable=False)  # Corrected to `String`
    student_score = Column(Integer)

    # Foreign key linking to `questions`
    question_id = Column(Integer, ForeignKey("questions.id"))  # Fixed table and column reference
    question = relationship("Question", back_populates="student_answers")  # Fixed relationship and back_populates name
