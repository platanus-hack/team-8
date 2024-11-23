# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports

class StudentAnswer(BaseModel):
    content : str
    model_score : int
    model_feedback : str
    student_score : int

    question_id : int
    student_id : int
