# Pydantic Imports
from pydantic import BaseModel
# Libraries Imports

# Local Imports


class Professor(BaseModel):
    email : str

    guideline_id : int