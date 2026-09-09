from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Requirement, TestCase
from app.schemas import RequirementCreate
from app.services.generator import analyze_requirement, generate_test_cases
from app.services.openai_generator import generate_ai_test_cases

router = APIRouter(tags=["Generate"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
def generate(requirement: RequirementCreate, db: Session = Depends(get_db)):
    try:
        ai_result, generator_mode = generate_ai_test_cases(
            requirement.title,
            requirement.description,
        )

        if ai_result:
            analysis = {
                "priority": ai_result["priority"],
                "risk_level": ai_result["risk_level"],
                "quality_score": ai_result["quality_score"],
                "recommended_automation": ai_result["recommended_automation"],
            }
            categorized_cases = ai_result["test_cases"]
        else:
            categorized_cases = generate_test_cases(requirement.description)
            analysis = analyze_requirement(requirement.description)

        flat_text = []
        for category, cases in categorized_cases.items():
            flat_text.append(f"[{category.upper()}]")
            flat_text.extend(cases)

        db_requirement = Requirement(
            title=requirement.title,
            description=requirement.description,
            generated_cases="\n".join(flat_text),
            priority=analysis["priority"],
            risk_level=analysis["risk_level"],
            quality_score=analysis["quality_score"],
            generator_mode=generator_mode,
        )

        db.add(db_requirement)
        db.commit()
        db.refresh(db_requirement)

        test_counter = 1
        for category, cases in categorized_cases.items():
            for case in cases:
                test_case = TestCase(
                    requirement_id=db_requirement.id,
                    test_id=f"TC-{test_counter:03d}",
                    category=category,
                    description=case,
                    priority=analysis["priority"],
                    status="NOT_RUN",
                )
                db.add(test_case)
                test_counter += 1

        db.commit()

        return {
            "id": db_requirement.id,
            "requirement": requirement.title,
            "generator_mode": generator_mode,
            "analysis": analysis,
            "test_cases": categorized_cases,
        }
    except Exception as e:
        db.rollback()
        print(f"Error generating test cases: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating test cases.",
        )
