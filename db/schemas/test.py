# Pydantic Imports
from pydantic import BaseModel

# Libraries Imports

# Local Imports


class Test(BaseModel):
    title : str
    student_score :  int
    s3_link: str
    
    student_id : int  
