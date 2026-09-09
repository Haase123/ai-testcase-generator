import csv
import io
import json

import pytest
from fastapi.testclient import TestClient

from app.api import routes_generate
from app.main import app
from app.api import routes_status

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AI Test Case Generator is running"


def test_generate_login_cases():
    response = client.post(
        "/generate",
        json={
            "title": "Login",
            "description": "User can log in with email and password",
        },
    )

    assert response.status_code == 200

    data = response.json()

    # Analyse prüfen
    assert "analysis" in data
    assert data["analysis"]["priority"] == "HIGH"
    assert data["analysis"]["risk_level"] == "HIGH"
    assert data["analysis"]["quality_score"] >= 80

    # Testfälle prüfen
    assert "test_cases" in data
    assert "positive" in data["test_cases"]
    assert len(data["test_cases"]["security"]) > 0


def test_list_requirements():
    response = client.get("/requirements")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "No", "description": "This description is long enough."},
        {"title": "Valid title", "description": "Too short"},
    ],
)
def test_generate_rejects_insufficient_requirements(payload):
    response = client.post("/generate", json=payload)

    assert response.status_code == 422


def test_generate_uses_rule_based_fallback(monkeypatch):
    monkeypatch.setattr(
        routes_generate,
        "generate_ai_test_cases",
        lambda title, description: (None, "rule-based"),
    )

    response = client.post(
        "/generate",
        json={
            "title": "Create account",
            "description": "Users can create an account with a valid email address",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["generator_mode"] == "rule-based"
    assert data["test_cases"]["positive"]
    assert data["test_cases"]["security"]


def test_generate_assesses_priority_and_risk():
    response = client.post(
        "/generate",
        json={
            "title": "Process regulated payment",
            "description": (
                "Process payment transactions with PCI compliance and personal data "
                "protection for checkout and refunds"
            ),
        },
    )

    assert response.status_code == 200
    analysis = response.json()["analysis"]
    assert analysis["priority"] == "CRITICAL"
    assert analysis["risk_level"] == "CRITICAL"
    assert analysis["quality_score"] == 100
    assert "End-to-end flow test" in analysis["recommended_automation"]


def test_status_endpoint_reports_healthy_services():
    response = client.get("/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["api"] == "ok"
    assert data["services"]["database"] == "ok"
    assert data["services"]["export"] == "ok"
    assert "timestamp" in data


def test_status_endpoint_reports_database_error(monkeypatch):
    def failing_session_local():
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(routes_status, "SessionLocal", failing_session_local)

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["services"]["database"] == "error"


def test_history_contains_generated_requirement_and_details():
    payload = {
        "title": "History test requirement",
        "description": "List and fetch a requirement from the saved history",
    }
    generated = client.post("/generate", json=payload)
    assert generated.status_code == 200
    requirement_id = generated.json()["id"]

    history = client.get("/requirements")
    assert history.status_code == 200
    history_item = next(item for item in history.json() if item["id"] == requirement_id)
    assert history_item["title"] == payload["title"]
    assert history_item["test_cases"]["positive"]

    details = client.get(f"/requirements/{requirement_id}")
    assert details.status_code == 200
    data = details.json()
    assert data["id"] == requirement_id
    assert data["analysis"]["recommended_automation"] == []
    assert data["test_cases"]["security"]


def test_history_returns_not_found_for_unknown_requirement():
    response = client.get("/requirements/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Requirement not found."


def test_json_export_returns_json_attachment():
    payload = {
        "test_cases": {"positive": ["Accept valid input"], "security": []},
    }

    response = client.post("/export/json", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert "test-cases.json" in response.headers["content-disposition"]
    assert json.loads(response.text) == payload


def test_csv_export_returns_categories_and_cases():
    response = client.post(
        "/export/csv",
        json={
            "test_cases": {
                "positive": ["Accept valid input"],
                "negative": ["Reject invalid input"],
            }
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "test-cases.csv" in response.headers["content-disposition"]

    rows = list(csv.reader(io.StringIO(response.text)))
    assert rows == [
        ["Category", "Test Case"],
        ["positive", "Accept valid input"],
        ["negative", "Reject invalid input"],
    ]