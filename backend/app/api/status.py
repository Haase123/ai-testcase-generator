from fastapi import APIRouter
from datetime import datetime
from app.database import SessionLocal   
from sqlalchemy import text
from app.services.openai_generator import get_ai_generator_status

router = APIRouter(prefix="/status", tags=["Status"])

def get_database_status():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return "ok"
    except Exception as e:
        print(f"Database health check failed: {e}")
        return "error"

@router.get("")
def get_status():
    return {
        "status": "healthy",
        "service": "AI Test Case Generator",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "ok",
            "database": get_database_status(),
            "ai_generator": get_ai_generator_status(),
            "export": "ok",
        },
    }