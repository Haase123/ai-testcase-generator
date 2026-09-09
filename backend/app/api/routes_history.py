import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Requirement, TestCase

router = APIRouter(tags=["History"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def build_test_case_groups(cases):
    groups = {
        "positive": [],
        "negative": [],
        "edge_cases": [],
        "security": [],
    }

    if isinstance(cases, dict):
        for key, items in cases.items():
            normalized_key = key.strip().lower().replace(" ", "_")
            if normalized_key in groups:
                groups[normalized_key].extend(items or [])
        return groups

    if not cases:
        return groups

    current_key = None
    for line in str(cases).split("\n"):
        cleaned = line.strip()
        if not cleaned:
            continue

        category_match = re.match(r"^\[(.+)\]$", cleaned)
        if category_match:
            normalized_key = category_match.group(1).strip().lower().replace(" ", "_")
            if normalized_key in groups:
                current_key = normalized_key
            else:
                current_key = None
            continue

        if current_key:
            groups[current_key].append(cleaned)
        else:
            groups["positive"].append(cleaned)

    return groups


@router.get("/requirements")
def list_requirements(db: Session = Depends(get_db)):
    requirements = db.query(Requirement).all()

    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "generated_test_cases": (r.generated_cases or "").split("\n") if r.generated_cases else [],
            "test_cases": build_test_case_groups(r.generated_cases),
        }
        for r in requirements
    ]


@router.get("/requirements/{requirement_id}")
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):
    requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found.")

    return {
        "id": requirement.id,
        "title": requirement.title,
        "description": requirement.description,
        "generator_mode": requirement.generator_mode,
        "analysis": {
            "priority": requirement.priority,
            "risk_level": requirement.risk_level,
            "quality_score": requirement.quality_score,
            "recommended_automation": [],
        },
        "generated_test_cases": (requirement.generated_cases or "").split("\n") if requirement.generated_cases else [],
        "test_cases": build_test_case_groups(requirement.generated_cases),
    }


@router.get("/test-cases")
def list_test_cases(db: Session = Depends(get_db)):
    test_cases = db.query(TestCase).all()

    return [
        {
            "id": test_case.id,
            "test_id": test_case.test_id,
            "requirement_id": test_case.requirement_id,
            "category": test_case.category,
            "description": test_case.description,
            "priority": test_case.priority,
            "status": test_case.status,
        }
        for test_case in test_cases
    ]
