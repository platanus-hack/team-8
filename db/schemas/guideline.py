# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports


class Guideline(BaseModel):
    title : str
    topic : str
    max_score :  int
    s3_link : str
    
    professor_id : int
