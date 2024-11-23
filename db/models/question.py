from sqlalchemy import Column, Integer, String, Enum
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
    title = Column(String, nullable=False)
    type = Column(Enum(QuestionTypes), nullable=False)
    guideline_answer = Column(String, nullable=False)  # Corrected to `String`
    student_score = Column(Integer)

    # Foreign key linking to `students_answers`
    student_answers = relationship("StudentAnswer", back_populates="question")  # Removed incorrect ForeignKey
