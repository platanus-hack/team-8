# Pydantic Imports
from pydantic import BaseModel

# Libraries Imports

# Local Imports


class Test(BaseModel):
    title : str
    max_score :  int
    student_score :  int
    
    student_id : int  
