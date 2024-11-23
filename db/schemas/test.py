from pydantic import BaseModel
from enum import Enum
from datetime import date

from student import StudentBase

from typing import List


class StudentNested(StudentBase):
    pass


class TestStatusEnum(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Define the enumeration
class TestTopicsEnum(str, Enum):
    SCIENCE = "SCIENCE"
    MATHEMATICS = "MATHEMATICS"
    LANGUAGE = "LANGUAGE"
    HISTORY = "HISTORY"


class TestBase(BaseModel):
    title: str
    topic: TestTopicsEnum
    status: TestStatusEnum
    max_score = int
    student_score = int
    start_date = date
    end_date = date
    status: TestStatusEnum

    class Config:
        orm_mode = True

class TestCreate(TestBase):
    student_ids: List[int]

class TestRead(TestBase):
    student_ids: List[StudentNested]