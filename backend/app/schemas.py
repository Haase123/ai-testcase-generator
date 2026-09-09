from pydantic import BaseModel, Field
from typing import List


class RequirementCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)


class RequirementResponse(RequirementCreate):
    id: int

    model_config = {"from_attributes": True}

class TestCaseResponse(BaseModel):
    test_id: str
    category: str
    description: str
    priority: str
    status: str