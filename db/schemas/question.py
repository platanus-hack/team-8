# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports


class Question(BaseModel):
    title : str
    type : int
    max_score : int
    guideline_answer: str
    positional_index: int
    
    guideline_id : int