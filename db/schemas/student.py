from pydantic import BaseModel

from .test import TestBase

from enum import Enum
from typing import List


class TestNested(TestBase):
    pass


class StudentBase(BaseModel):
    id: int
    first_names: str
    last_names: str

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    first_names: str
    last_names: str

class StudentRead(BaseModel):
    tests: List[TestBase]