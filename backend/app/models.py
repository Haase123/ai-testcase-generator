from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    generated_cases = Column(Text, nullable=True)

    priority = Column(String, nullable=True)
    risk_level = Column(String, nullable=True)
    quality_score = Column(Integer, nullable=True)
    generator_mode = Column(String, nullable=True)

    test_cases = relationship(
        "TestCase",
        back_populates="requirement",
        cascade="all, delete-orphan",
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)

    requirement_id = Column(
        Integer,
        ForeignKey("requirements.id"),
        nullable=False,
    )

    test_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, nullable=False, default="MEDIUM")
    status = Column(String, nullable=False, default="NOT_RUN")

    requirement = relationship(
        "Requirement",
        back_populates="test_cases",
    )