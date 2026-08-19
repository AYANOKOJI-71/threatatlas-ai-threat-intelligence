# ThreatAtlas Data Model

## STIX-inspired local record contract

ThreatAtlas uses a deliberately small JSON contract inspired by common CTI exchange concepts. It does **not** claim full STIX conformance and does not communicate with TAXII/AIS services. A case has a provenance label, narrative, indicators, supporting evidence fragments, and optional technique candidates.

| Entity | Required fields | Why it exists |
|---|---|---|
| `CaseRecord` | `caseId`, `title`, `sourceLabel`, `narrative`, `confidence`, `indicators` | Bounded analyst review unit. |
| `Indicator` | `indicatorId`, `kind`, `value`, `confidence`, `tags` | A safe observable used for correlation and review. Fixture values use reserved documentation domains or RFC 5737 addresses. |
| `Evidence` | `evidenceId`, `summary`, `sourceType`, `observedAt` | Human-readable rationale supporting a review priority. |
| `TechniqueSuggestion` | `techniqueId`, `name`, `tactic`, `rationale`, `confidence` | A defensive ATT&CK-informed hypothesis that a human must validate. |
| `IntelligenceBrief` | `executiveSummary`, `priority`, `keyObservables`, `recommendedValidationActions`, `limitations` | Client-ready defensive output based strictly on the submitted case. |

## Mapping catalogue

The deterministic demonstration includes a compact, static technique catalogue. It maps narrative themes to technique candidates such as phishing, command and scripting interpreter, external remote services, and exfiltration over a web service. The mapping is a controlled vocabulary for analyst navigation—not evidence that a technique occurred.

## Priority factors

| Factor | Effect | Explanation shown to analyst |
|---|---|---|
| Record confidence | Adds weight for higher-confidence supplied reports | Displays the source-provided confidence band. |
| Indicator type | Raises review priority for high-value observable categories | Lists the categories that contributed. |
| Corroboration | Adds weight when multiple unique observables support the same case | Shows deduplicated evidence count. |
| Severity tags | Adds bounded weight for tags such as `credential-access` or `data-exfiltration` | Shows exact matching tags. |
| ATT&CK suggestion | Adds limited context weight only | Labels the output as a hypothesis to validate. |

The final score is capped at 100 and accompanied by its factors. It is not a probability of compromise or a substitute for incident-scoping decisions.
