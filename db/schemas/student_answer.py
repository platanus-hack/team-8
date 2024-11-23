# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports

class StudentAnswer(BaseModel):
    title : str
    guideline_answer : str
    student_score : int

    question_id : int
