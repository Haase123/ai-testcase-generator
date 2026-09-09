import csv
import io
import json

from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["Export"])


@router.post("/export/json")
def export_json(data: dict):
    content = json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )

    return Response(
        content=content,
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="test-cases.json"',
        },
    )


@router.post("/export/csv")
def export_csv(data: dict):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Category", "Test Case"])

    test_cases = data.get("test_cases", {})
    for category, cases in test_cases.items():
        for case in cases:
            writer.writerow([category, case])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="test-cases.csv"',
        },
    )
