export type Confidence = "low" | "medium" | "high";

export interface CaseSummary {
  risk_score: number;
  priority: string;
  confidence: Confidence;
  unique_indicator_count: number;
  evidence_count: number;
  technique_suggestion_count: number;
  duplicate_indicator_count: number;
}

export interface CaseListItem {
  case_id: string;
  title: string;
  source_label: string;
  tags: string[];
  summary: CaseSummary;
}

export interface Indicator {
  indicator_id: string;
  kind: string;
  value: string;
  confidence: Confidence;
  tags: string[];
  duplicate_count: number;
}

export interface Evidence {
  evidence_id: string;
  summary: string;
  source_type: string;
  observed_at: string;
}

export interface TechniqueSuggestion {
  technique_id: string;
  name: string;
  tactic: string;
  confidence: Confidence;
  rationale: string;
}

export interface PriorityFactor {
  label: string;
  points: number;
  detail: string;
}

export interface Brief {
  executive_summary: string;
  key_observables: string[];
  recommended_validation_actions: string[];
  limitations: string[];
}

export interface CaseReport extends CaseListItem {
  narrative: string;
  generated_at: string;
  indicators: Indicator[];
  evidence: Evidence[];
  technique_suggestions: TechniqueSuggestion[];
  priority_factors: PriorityFactor[];
  brief: Brief;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init);
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Request failed with ${response.status}`);
  }
  return (await response.json()) as T;
}

export const api = {
  listCases: () => request<CaseListItem[]>("/api/cases"),
  getCase: (caseId: string) => request<CaseReport>(`/api/cases/${caseId}`),
  analyze: (caseRecord: unknown) =>
    request<CaseReport>("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ case: caseRecord })
    })
};
