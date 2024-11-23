# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports


class Question(BaseModel):
    title : str
    type : int
    guideline_answer : str
    student_score : int
    max_score : int

    student_answer_id : int