from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

IndicatorKind = Literal["domain", "ipv4", "email", "sha256"]
ConfidenceBand = Literal["low", "medium", "high"]


class IndicatorInput(BaseModel):
    indicator_id: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9-]+$")
    kind: IndicatorKind
    value: str = Field(min_length=3, max_length=255)
    confidence: ConfidenceBand
    tags: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, values: list[str]) -> list[str]:
        return sorted({value.strip().lower() for value in values if value.strip()})


class EvidenceInput(BaseModel):
    evidence_id: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9-]+$")
    summary: str = Field(min_length=10, max_length=500)
    source_type: Literal["synthetic-telemetry", "analyst-note", "training-scenario"]
    observed_at: datetime


class CaseInput(BaseModel):
    case_id: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9-]+$")
    title: str = Field(min_length=8, max_length=140)
    source_label: str = Field(min_length=3, max_length=120)
    narrative: str = Field(min_length=30, max_length=4000)
    confidence: ConfidenceBand
    indicators: list[IndicatorInput] = Field(min_length=1, max_length=30)
    evidence: list[EvidenceInput] = Field(default_factory=list, max_length=20)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("tags")
    @classmethod
    def normalize_case_tags(cls, values: list[str]) -> list[str]:
        return sorted({value.strip().lower() for value in values if value.strip()})


class TechniqueSuggestion(BaseModel):
    technique_id: str
    name: str
    tactic: str
    confidence: ConfidenceBand
    rationale: str


class PriorityFactor(BaseModel):
    label: str
    points: int
    detail: str


class NormalizedIndicator(BaseModel):
    indicator_id: str
    kind: IndicatorKind
    value: str
    confidence: ConfidenceBand
    tags: list[str]
    duplicate_count: int = 0


class CaseSummary(BaseModel):
    risk_score: int
    priority: Literal["Critical review", "High review", "Elevated review", "Routine review"]
    confidence: ConfidenceBand
    unique_indicator_count: int
    evidence_count: int
    technique_suggestion_count: int
    duplicate_indicator_count: int


class IntelligenceBrief(BaseModel):
    executive_summary: str
    key_observables: list[str]
    recommended_validation_actions: list[str]
    limitations: list[str]


class CaseReport(BaseModel):
    case_id: str
    title: str
    source_label: str
    narrative: str
    tags: list[str]
    generated_at: datetime
    indicators: list[NormalizedIndicator]
    evidence: list[EvidenceInput]
    technique_suggestions: list[TechniqueSuggestion]
    priority_factors: list[PriorityFactor]
    summary: CaseSummary
    brief: IntelligenceBrief


class CaseListItem(BaseModel):
    case_id: str
    title: str
    source_label: str
    tags: list[str]
    summary: CaseSummary


class AnalyzeRequest(BaseModel):
    case: CaseInput


class MetricsSnapshot(BaseModel):
    bundled_cases: int
    analyzed_reports: int
    active_profile: str
    safety_mode: str
