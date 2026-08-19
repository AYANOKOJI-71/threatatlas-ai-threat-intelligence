from __future__ import annotations

from fastapi.testclient import TestClient
from threatatlas.fixtures import get_case
from threatatlas.main import app

client = TestClient(app)


def test_health_case_list_and_detail_contracts() -> None:
    health = client.get("/health")
    cases = client.get("/api/cases")
    detail = client.get("/api/cases/case-synthetic-phishing")

    assert health.status_code == 200
    assert health.json() == {"status": "ok", "mode": "local-synthetic-only"}
    assert cases.status_code == 200
    assert [item["case_id"] for item in cases.json()] == [
        "case-synthetic-remote-access",
        "case-synthetic-phishing",
        "case-synthetic-routine",
    ]
    assert detail.status_code == 200
    assert detail.json()["summary"]["duplicate_indicator_count"] == 1


def test_unknown_case_returns_bounded_not_found_error() -> None:
    response = client.get("/api/cases/not-a-local-case")

    assert response.status_code == 404
    assert response.json()["detail"] == "The requested local case fixture does not exist."


def test_explicit_sanitized_case_analysis_and_metrics_contracts() -> None:
    case = get_case("case-synthetic-routine")
    analysis = client.post("/api/analyze", json={"case": case.model_dump(mode="json")})
    metrics = client.get("/api/metrics")
    prometheus = client.get("/metrics")

    assert analysis.status_code == 201
    assert analysis.json()["case_id"] == "case-synthetic-routine"
    assert analysis.json()["summary"]["priority"] == "Routine review"
    assert metrics.status_code == 200
    assert metrics.json()["bundled_cases"] == 3
    assert "threatatlas_bundled_cases 3" in prometheus.text
