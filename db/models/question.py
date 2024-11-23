from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import enum

# Define the enumeration
class QuestionTypes(enum.Enum):
    MULTIPLE_CHOICES = "MULTIPLE_CHOICES"
    TRUTH_FALSE = "TRUTH_FALSE"
    DEVELOPMENT = "DEVELOPMENT"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(Enum(QuestionTypes))
    guideline_answer = Column(String)  # Corrected to `String`
    student_score = Column(Integer)
    max_score = Column(Integer)

    # Foreign key linking to `students_answers`
    student_answer_id = Column(Integer, ForeignKey("student_answer.id"))
    students_answers = relationship("StudentAnswer", back_populates="students_answers")