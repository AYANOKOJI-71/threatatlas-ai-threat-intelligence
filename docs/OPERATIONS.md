# Local Operations Guide

ThreatAtlas is deliberately packaged as a **local-review demonstration**. It reads only bundled synthetic fixtures or JSON that an analyst explicitly supplies. It does not include live-feed retrieval, cloud storage, credentials, autonomous response, remote scanning, or remote target interaction.

## Local development

| Task | Command | Expected result |
|---|---|---|
| Install dependencies | `make install` | Creates `.venv`, installs API dependencies, and installs the React workspace. |
| Start API | `make api` | Serves `/health`, `/api/cases`, `/api/analyze`, `/api/metrics`, and `/metrics` on port 4910 by default. |
| Start web console | `make web` | Serves the analyst console on port 5201, proxying same-origin requests to the API. |
| Run checks | `make lint && make test && make build` | Runs Ruff, pytest, Vitest, and the production web build. |

Copy `.env.example` to `.env` only to override local ports. The file must never hold production credentials or client-derived information.

## Container demonstration

`docker compose up --build` starts the API and analyst-console development server. The web container proxies its same-origin API routes to the internal API service, while the host exposes ports 5201 and 4910 by default. The included health check calls the bounded `/health` endpoint.

| Service | Host port | Container port | Purpose |
|---|---:|---:|---|
| `api` | 4910 | 8000 | Local deterministic analysis and evidence APIs. |
| `web` | 5201 | 5201 | Analyst console and same-origin proxy. |

## Operational constraints

The priority score is an explainable local triage aid, not a determination of compromise, maliciousness, attribution, or business impact. Analysts must validate observables only against systems and telemetry they are authorized to review. Any real intelligence-feed integration requires legal review, source-specific authorization, data governance, retention controls, authentication, auditing, and a separately reviewed production threat model.
