# Pydantic Imports
from pydantic import BaseModel

# Libraries Imports

# Local Imports


class Test(BaseModel):
    title : str
    student_score :  int
    s3_link: str
    positional_index :  int
    s3_filename: str

    
    guideline_id : int  
    student_id : int  
