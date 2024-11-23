from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Create the declarative base
Base = declarative_base()

# # Association Table
# students_tests = Table(
#     "students_tests", Base.metadata,
#     Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
#     Column("test_id", Integer, ForeignKey("tests.id"), primary_key=True)
# )
