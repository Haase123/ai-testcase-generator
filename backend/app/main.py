from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.api.routes_export import router as export_router
from app.api.routes_generate import router as generate_router
from app.api.routes_history import router as history_router
from app.api.routes_status import router as status_router

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="AI Test Case Generator")

app.include_router(status_router)
app.include_router(generate_router)
app.include_router(export_router)
app.include_router(history_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Test Case Generator is running"}
