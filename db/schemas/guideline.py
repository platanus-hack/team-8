# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports


class Guideline(BaseModel):
    title : str
    max_score :  int
    topic : str
    s3_link : str
    test_id : int
    question_id : int
