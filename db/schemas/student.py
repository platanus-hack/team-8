# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports

class Student(BaseModel):
    first_names : str
    last_names : str