# SQLAlchemy Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Libraries Imports

# Local Imports
from .base import Base, students_tests

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)

    guideline_id = Column(Integer, ForeignKey("guideline.id"))
    guidelines = relationship("Guideline", back_populates="guidelines")