# ThreatAtlas Architecture

## Purpose

ThreatAtlas is an **AI-assisted defensive threat-intelligence workspace** for analysts who need to convert authorized, sanitized case records into prioritised indicators, ATT&CK-informed context, and a concise client-ready brief. The bundled product uses synthetic fixtures and deterministic scoring so that every demonstration is reproducible without credentials, live feeds, or production data.

```text
Bundled synthetic case / analyst-supplied sanitized JSON
                         ↓
               schema and size validation
                         ↓
    normalization → deduplication → evidence extraction
                         ↓
 explainable local prioritization → ATT&CK suggestion catalogue
                         ↓
 case report, review queue, defensive intelligence brief, metrics
```

## Components

| Component | Responsibility | Trust boundary |
|---|---|---|
| React analyst console | Displays cases, evidence, ATT&CK mappings, scoring rationale, and export-ready brief text. | Browser communicates only with the local application API. |
| FastAPI service | Validates bounded input, processes synthetic/sanitized records, and exposes read-only report/brief endpoints. | No shell execution, no remote fetch, no background collection, and no persistence of secrets. |
| Local enrichment engine | Extracts observables, normalizes duplicate indicators, applies documented scoring factors, and produces suggestions from an embedded ATT&CK catalogue. | No malware analysis, network probes, credential use, or claim of independent threat attribution. |
| Fixture catalogue | Stores clearly synthetic STIX-inspired records for reproducible demonstrations. | Repository data excludes client records, live indicators, malware, and personal data. |

## Explainable assistance model

The application does not present opaque verdicts as intelligence fact. It calculates a review priority from transparent factors: indicator type, confidence supplied by the record, corroborating evidence count, severity tags, and recognized ATT&CK-relevant language. It returns the contributing factors alongside the score. Analyst-facing copy labels results as **suggestions to validate**, not confirmed attribution.

MITRE publishes ATT&CK data in STIX representations and describes the official TAXII server for programmatic access.[1] ThreatAtlas uses a compact embedded catalogue for deterministic demonstration only; a future, separately approved adapter could validate and synchronize a versioned ATT&CK source.

## Non-goals

ThreatAtlas does not retrieve, scan, probe, block, exploit, execute, or alter remote systems. It does not automatically contact intelligence feeds, generate offensive instructions, or expose a client-data ingestion endpoint. Production adoption would require legal authorization, data handling controls, privacy review, retained evidence policies, and human analyst review.

## Reference

[1] [MITRE ATT&CK — ATT&CK Data & Tools](https://attack.mitre.org/resources/attack-data-and-tools/)
