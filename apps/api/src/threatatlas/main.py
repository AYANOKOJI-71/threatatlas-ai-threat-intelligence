from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from threatatlas.contracts import AnalyzeRequest, CaseListItem, CaseReport, MetricsSnapshot
from threatatlas.engine import analyze_case
from threatatlas.fixtures import get_case, load_cases

app = FastAPI(
    title="ThreatAtlas",
    version="0.1.0",
    description="Safe, local-only threat intelligence prioritization and ATT&CK-informed analyst review.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5201", "http://127.0.0.1:5201"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def _reports() -> list[CaseReport]:
    reports = [analyze_case(case) for case in load_cases().values()]
    return sorted(reports, key=lambda report: report.summary.risk_score, reverse=True)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "local-synthetic-only"}


@app.get("/api/cases", response_model=list[CaseListItem])
def list_cases() -> list[CaseListItem]:
    return [
        CaseListItem(
            case_id=report.case_id,
            title=report.title,
            source_label=report.source_label,
            tags=report.tags,
            summary=report.summary,
        )
        for report in _reports()
    ]


@app.get("/api/cases/{case_id}", response_model=CaseReport)
def case_detail(case_id: str) -> CaseReport:
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="The requested local case fixture does not exist.")
    return analyze_case(case)


@app.get("/api/cases/{case_id}/brief", response_model=CaseReport)
def case_brief(case_id: str) -> CaseReport:
    return case_detail(case_id)


@app.post("/api/analyze", response_model=CaseReport, status_code=201)
def analyze_local_case(request: AnalyzeRequest) -> CaseReport:
    return analyze_case(request.case)


@app.get("/api/metrics", response_model=MetricsSnapshot)
def metrics() -> MetricsSnapshot:
    return MetricsSnapshot(
        bundled_cases=len(load_cases()),
        analyzed_reports=len(_reports()),
        active_profile="local-review / v0.1",
        safety_mode="synthetic fixtures or explicitly supplied sanitized JSON only",
    )


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    reports = _reports()
    high_priority = sum(report.summary.risk_score >= 50 for report in reports)
    return "\n".join(
        [
            "# HELP threatatlas_bundled_cases Total bundled deterministic local case fixtures.",
            "# TYPE threatatlas_bundled_cases gauge",
            f"threatatlas_bundled_cases {len(load_cases())}",
            "# HELP threatatlas_high_review_cases Cases requiring high or critical analyst review.",
            "# TYPE threatatlas_high_review_cases gauge",
            f"threatatlas_high_review_cases {high_priority}",
            "",
        ]
    )
