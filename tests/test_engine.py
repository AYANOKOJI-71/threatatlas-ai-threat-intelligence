from __future__ import annotations

import pytest
from threatatlas.engine import analyze_case
from threatatlas.fixtures import get_case, load_cases


def test_bundled_cases_are_deterministic_and_prioritized() -> None:
    reports = {case_id: analyze_case(case) for case_id, case in load_cases().items()}

    phishing = reports["case-synthetic-phishing"]
    remote_access = reports["case-synthetic-remote-access"]
    routine = reports["case-synthetic-routine"]

    assert phishing.summary.duplicate_indicator_count == 1
    assert phishing.summary.risk_score == 85
    assert phishing.summary.priority == "Critical review"
    assert remote_access.summary.risk_score == 100
    assert remote_access.summary.priority == "Critical review"
    assert routine.summary.risk_score == 17
    assert routine.summary.priority == "Routine review"


def test_report_retains_explainable_hypotheses_and_defensive_limits() -> None:
    report = analyze_case(get_case("case-synthetic-remote-access"))

    assert {item.technique_id for item in report.technique_suggestions} == {"T1021", "T1567"}
    assert any(factor.label == "Defensive review themes" for factor in report.priority_factors)
    assert "No external enrichment" in report.brief.limitations[2]
    assert "do not interact" in report.brief.recommended_validation_actions[0].lower()


def test_invalid_indicator_values_are_rejected_before_reporting() -> None:
    case = get_case("case-synthetic-routine")
    invalid_indicator = case.indicators[0].model_copy(update={"kind": "ipv4", "value": "not-an-ip"})
    invalid_case = case.model_copy(update={"indicators": [invalid_indicator]})

    with pytest.raises(ValueError, match="not-an-ip"):
        analyze_case(invalid_case)
