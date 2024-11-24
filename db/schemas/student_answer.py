# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports

class StudentAnswer(BaseModel):
    content : str
    student_score : int
    model_feedback : str
    student_score : int

    question_id : int
    test_id : int
