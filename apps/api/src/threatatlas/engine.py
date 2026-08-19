from __future__ import annotations

import ipaddress
import re
from collections import Counter
from datetime import UTC, datetime

from threatatlas.contracts import (
    CaseInput,
    CaseReport,
    CaseSummary,
    ConfidenceBand,
    IndicatorInput,
    IntelligenceBrief,
    NormalizedIndicator,
    PriorityFactor,
    TechniqueSuggestion,
)

TECHNIQUE_CATALOG = (
    {
        "terms": ("phishing", "invoice", "credential"),
        "technique_id": "T1566",
        "name": "Phishing",
        "tactic": "Initial Access",
        "rationale": "The supplied narrative references a synthetic lure or credential collection theme.",
    },
    {
        "terms": ("powershell", "script", "command"),
        "technique_id": "T1059",
        "name": "Command and Scripting Interpreter",
        "tactic": "Execution",
        "rationale": "The supplied narrative references scripted command execution and needs analyst validation.",
    },
    {
        "terms": ("remote service", "vpn", "remote access", "sign-in"),
        "technique_id": "T1021",
        "name": "Remote Services",
        "tactic": "Lateral Movement",
        "rationale": "The supplied narrative references remote-access activity and needs authorized log review.",
    },
    {
        "terms": ("exfiltration", "upload", "web service", "archive"),
        "technique_id": "T1567",
        "name": "Exfiltration Over Web Service",
        "tactic": "Exfiltration",
        "rationale": "The supplied narrative references a potential outbound transfer theme and needs validation.",
    },
)

TYPE_POINTS = {"domain": 7, "ipv4": 8, "email": 5, "sha256": 10}
TAG_POINTS = {
    "credential-access": 20,
    "data-exfiltration": 20,
    "phishing": 12,
    "ransomware": 20,
    "suspicious-auth": 14,
}
CONFIDENCE_POINTS = {"low": 10, "medium": 20, "high": 30}


def _normalized_value(indicator: IndicatorInput) -> str:
    value = indicator.value.strip()
    if indicator.kind in {"domain", "email", "sha256"}:
        return value.lower()
    return value


def _validate_indicator(indicator: IndicatorInput) -> None:
    value = _normalized_value(indicator)
    if indicator.kind == "ipv4":
        ipaddress.IPv4Address(value)
    elif indicator.kind == "domain":
        if not re.fullmatch(r"[a-z0-9.-]+", value) or "." not in value:
            raise ValueError(f"Indicator {indicator.indicator_id} is not a supported domain value.")
    elif indicator.kind == "email":
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError(f"Indicator {indicator.indicator_id} is not a supported email value.")
    elif indicator.kind == "sha256" and not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError(f"Indicator {indicator.indicator_id} must be a lowercase or uppercase SHA-256 value.")


def normalize_indicators(indicators: list[IndicatorInput]) -> tuple[list[NormalizedIndicator], int]:
    grouped: dict[tuple[str, str], list[IndicatorInput]] = {}
    for indicator in indicators:
        _validate_indicator(indicator)
        key = (indicator.kind, _normalized_value(indicator))
        grouped.setdefault(key, []).append(indicator)

    normalized = []
    duplicate_count = 0
    for (_, value), grouped_indicators in grouped.items():
        first = grouped_indicators[0]
        duplicate_count += len(grouped_indicators) - 1
        merged_tags = sorted({tag for item in grouped_indicators for tag in item.tags})
        confidence = _highest_confidence(item.confidence for item in grouped_indicators)
        normalized.append(
            NormalizedIndicator(
                indicator_id=first.indicator_id,
                kind=first.kind,
                value=value,
                confidence=confidence,
                tags=merged_tags,
                duplicate_count=len(grouped_indicators) - 1,
            )
        )
    return sorted(normalized, key=lambda item: (item.kind, item.value)), duplicate_count


def _highest_confidence(confidences: object) -> ConfidenceBand:
    ordered = {"low": 1, "medium": 2, "high": 3}
    values = list(confidences)
    return max(values, key=lambda confidence: ordered[confidence])


def suggest_techniques(case: CaseInput) -> list[TechniqueSuggestion]:
    corpus = " ".join([case.narrative, *case.tags, *(tag for item in case.indicators for tag in item.tags)]).lower()
    suggestions = []
    for technique in TECHNIQUE_CATALOG:
        matches = [term for term in technique["terms"] if re.search(rf"\b{re.escape(term)}\b", corpus)]
        if matches:
            confidence: ConfidenceBand = "high" if len(matches) >= 2 else "medium"
            suggestions.append(
                TechniqueSuggestion(
                    technique_id=technique["technique_id"],
                    name=technique["name"],
                    tactic=technique["tactic"],
                    confidence=confidence,
                    rationale=technique["rationale"],
                )
            )
    return suggestions


def _priority(
    case: CaseInput, indicators: list[NormalizedIndicator], suggestions: list[TechniqueSuggestion]
) -> tuple[int, list[PriorityFactor]]:
    factors = [
        PriorityFactor(
            label="Source confidence",
            points=CONFIDENCE_POINTS[case.confidence],
            detail=f"The supplied case confidence is {case.confidence}.",
        )
    ]
    type_points = min(sum(TYPE_POINTS[item.kind] for item in indicators), 30)
    factors.append(
        PriorityFactor(
            label="Observable categories",
            points=type_points,
            detail=f"{len(indicators)} unique indicator(s) contributed bounded category weight.",
        )
    )
    all_tags = set(case.tags) | {tag for item in indicators for tag in item.tags}
    matched_tags = sorted(tag for tag in all_tags if tag in TAG_POINTS)
    tag_points = min(sum(TAG_POINTS[tag] for tag in matched_tags), 35)
    if matched_tags:
        factors.append(
            PriorityFactor(
                label="Defensive review themes",
                points=tag_points,
                detail=f"Matched supplied tag(s): {', '.join(matched_tags)}.",
            )
        )
    evidence_points = min(len(case.evidence) * 4, 16)
    if evidence_points:
        factors.append(
            PriorityFactor(
                label="Corroborating evidence",
                points=evidence_points,
                detail=f"{len(case.evidence)} supplied evidence item(s) support review.",
            )
        )
    suggestion_points = min(len(suggestions) * 3, 12)
    if suggestion_points:
        factors.append(
            PriorityFactor(
                label="ATT&CK-informed hypotheses",
                points=suggestion_points,
                detail=f"{len(suggestions)} suggestion(s) require analyst validation.",
            )
        )
    return min(sum(factor.points for factor in factors), 100), factors


def _priority_label(score: int) -> str:
    if score >= 75:
        return "Critical review"
    if score >= 50:
        return "High review"
    if score >= 25:
        return "Elevated review"
    return "Routine review"


def _brief(
    case: CaseInput, indicators: list[NormalizedIndicator], suggestions: list[TechniqueSuggestion], score: int
) -> IntelligenceBrief:
    observable_preview = [f"{item.kind}: {item.value}" for item in indicators[:5]]
    action = (
        "Validate supplied observables against telemetry you are authorized to review; "
        "do not interact with observed infrastructure."
    )
    actions = [action, "Review the case’s source evidence and confidence with the designated incident owner."]
    if any(suggestion.technique_id == "T1566" for suggestion in suggestions):
        actions.append("Review approved mail-gateway and identity-provider telemetry for the reported lure theme.")
    if any(suggestion.technique_id == "T1021" for suggestion in suggestions):
        actions.append("Review authorized remote-access sign-in telemetry for anomalous access patterns.")
    if any(suggestion.technique_id == "T1567" for suggestion in suggestions):
        actions.append("Review approved proxy or egress telemetry for the reported outbound-transfer theme.")
    return IntelligenceBrief(
        executive_summary=(
            f"{case.title} received a deterministic review priority of {score}/100 from supplied local evidence. "
            "This is an analyst triage aid, not confirmation of malicious activity or attribution."
        ),
        key_observables=observable_preview,
        recommended_validation_actions=actions,
        limitations=[
            "The report evaluates only supplied local content and bundled synthetic fixtures.",
            "ATT&CK mappings are analyst-review suggestions rather than verified technique assertions.",
            "No external enrichment, scanning, probing, or automated response was performed.",
        ],
    )


def analyze_case(case: CaseInput) -> CaseReport:
    indicators, duplicate_count = normalize_indicators(case.indicators)
    suggestions = suggest_techniques(case)
    score, factors = _priority(case, indicators, suggestions)
    confidence = _highest_confidence([case.confidence, *(item.confidence for item in indicators)])
    summary = CaseSummary(
        risk_score=score,
        priority=_priority_label(score),
        confidence=confidence,
        unique_indicator_count=len(indicators),
        evidence_count=len(case.evidence),
        technique_suggestion_count=len(suggestions),
        duplicate_indicator_count=duplicate_count,
    )
    return CaseReport(
        case_id=case.case_id,
        title=case.title,
        source_label=case.source_label,
        narrative=case.narrative,
        tags=case.tags,
        generated_at=datetime.now(UTC),
        indicators=indicators,
        evidence=case.evidence,
        technique_suggestions=suggestions,
        priority_factors=factors,
        summary=summary,
        brief=_brief(case, indicators, suggestions, score),
    )


def summarize_indicator_kinds(indicators: list[NormalizedIndicator]) -> dict[str, int]:
    counts = Counter(item.kind for item in indicators)
    return dict(sorted(counts.items()))
