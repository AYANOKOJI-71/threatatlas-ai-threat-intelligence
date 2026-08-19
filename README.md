# ThreatAtlas — AI-Assisted Threat Intelligence Platform

ThreatAtlas is a **safe, deterministic, local-only analyst workspace** for demonstrating how structured threat records can be normalized, prioritized, connected to ATT&CK-informed hypotheses, and converted into client-ready defensive intelligence briefs. It is designed as an interview-ready project for **Cyber Invasion Army** and operates without a live feed, production data, remote lookup, remote target interaction, or autonomous action.

> **Safety boundary:** ThreatAtlas is a triage and evidence-organization demonstration. It accepts bundled synthetic fixtures or explicitly supplied, authorized, sanitized JSON only. It does not scan, probe, enrich, contact, or modify any external system.

## Why it is interview-ready

| Capability | Demonstrated implementation |
|---|---|
| Explainable prioritization | A bounded 0–100 score exposes the confidence, observable, theme, evidence, and ATT&CK-context factors that produced it. |
| Structured intelligence workflow | Local records use an STIX-inspired vocabulary for cases, indicators, evidence fragments, confidence, and tags. |
| ATT&CK-informed review | A deliberately limited local catalogue proposes hypotheses to validate, clearly labelled as non-attribution. |
| Analyst experience | A React console provides a prioritized queue, triage explanation, deduplicated evidence review, local JSON intake, and client-ready brief. |
| Defensive operations | FastAPI endpoints, a Prometheus-style `/metrics` response, Docker Compose, tests, and GitHub Actions form a complete local delivery workflow. |

## Demonstration scenarios

The repository ships only synthetic documentation-range indicators and training narratives.

| Fixture | Expected priority | What it demonstrates |
|---|---:|---|
| `synthetic-remote-access-review` | 100 / Critical review | Evidence-led review of remote-service and outbound-transfer themes. |
| `synthetic-phishing-review` | 85 / Critical review | Case normalization and duplicate-indicator merging in a phishing-themed training scenario. |
| `synthetic-routine-review` | 17 / Routine review | A low-confidence record that remains bounded and does not fabricate a high-risk conclusion. |

## Architecture

```text
Bundled synthetic JSON / explicitly supplied sanitized JSON
                         |
                         v
      FastAPI validation → normalization → explainable local score
                         |                   |
                         |                   v
                         |         ATT&CK-informed hypotheses
                         v
       evidence report + client-ready defensive brief
                         |
                         v
         React analyst queue, review panels, and local intake
```

The browser uses same-origin API requests; Vite proxies them to the local FastAPI service during development. The platform deliberately has no background workers, live-feed clients, database, credential store, or outbound connector.

## Quick start

```bash
make install
make api      # terminal 1, http://127.0.0.1:4910
make web      # terminal 2, http://127.0.0.1:5201
```

Then open `http://127.0.0.1:5201`, choose a synthetic case, inspect the Triage and Evidence panels, and use **Local intake** to submit the prefilled authorized synthetic record.

For a containerized local demonstration:

```bash
docker compose up --build
```

See [Local Operations](docs/OPERATIONS.md), [Architecture](docs/ARCHITECTURE.md), [Data Model](docs/DATA_MODEL.md), [Safe Use](docs/SAFE_USE.md), and [Demo Verification](docs/DEMO-VERIFICATION.md).

## Quality gate

```bash
make lint
make test
make build
```

The GitHub Actions workflow runs the API lint/test job and the frontend frozen-lockfile install, Vitest, and production-build job on pushes and pull requests.

## Scope and limitations

ThreatAtlas does **not** establish that a system is compromised, determine attribution, generate detections, monitor a production environment, or replace a qualified security analyst. ATT&CK mappings and risk scores are local, explainable review suggestions that require human validation against authorized telemetry.

The project references ATT&CK terminology and STIX-inspired structural ideas for interoperability and analyst communication; the bundled records are not claimed to be official CTI feeds or complete STIX bundles. MITRE publishes ATT&CK data and tools for using the framework, while OASIS maintains STIX documentation and examples for structured cyber-observable and intelligence-exchange vocabulary.[1] [2]

## References

[1]: https://attack.mitre.org/resources/attack-data-and-tools/ "MITRE ATT&CK — ATT&CK Data and Tools"

[2]: https://oasis-open.github.io/cti-documentation/stix/examples.html "OASIS CTI Documentation — STIX Examples"
