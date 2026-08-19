# ThreatAtlas Research Notes

## Design findings

ThreatAtlas will use a **local, STIX-inspired evidence model** for its synthetic demonstration records. MITRE states that Structured Threat Information Expression (STIX) is a language and serialization format for exchanging cyber threat intelligence, that ATT&CK data is available in STIX 2.0 and 2.1, and that it can be accessed through an official TAXII server.[1] The application will not connect to that server or any live feed in demo mode. Instead, the model will retain compatible concepts—indicator, observed data, relationship, confidence, technique mapping, and provenance—using sanitized JSON fixtures.

MITRE further describes the ATT&CK Navigator as a tool for annotating and exploring ATT&CK matrices, including defensive coverage. That supports an analyst-console feature which maps a case’s defensively relevant signals to selected ATT&CK techniques without asserting that the application independently validates malicious activity.[1]

CISA describes Automated Indicator Sharing (AIS) as a service for exchanging machine-readable cyber threat indicators and defensive measures. It notes that operational AIS participation requires an appropriate STIX/TAXII capability, onboarding, an agreement, and a certificate.[2] Accordingly, ThreatAtlas will provide a **future-integration boundary only**: no live feed ingestion, credentials, connection details, or sharing functions will exist in the bundled demonstration.

OASIS describes STIX as a language and serialization format for cyber threat intelligence, with JSON representations and relationships between objects. Its examples distinguish an Indicator as an intelligence assertion from Observed Data as machine-generated raw information, and introduce confidence and relationships in STIX 2.1.[3] ThreatAtlas will preserve that distinction in a compact local schema: supplied indicators and narrative evidence remain separate, while confidence and ATT&CK suggestions are displayed as analyst-review context rather than automatic attribution.

## Product boundary

| Area | Included in the deterministic demonstration | Explicitly excluded |
|---|---|---|
| Input | Bundled synthetic case files and analyst-supplied sanitized text/indicators | Live TAXII/AIS connections, scraping, credentialed feeds, production client data |
| Analysis | Explainable feature scoring, entity normalization, indicator deduplication, ATT&CK technique suggestions, evidence display | Malware execution, exploitation, scanning, enrichment against third-party infrastructure, automated blocking |
| Output | Client-ready defensive intelligence brief, case summary, recommended validation actions | Incident response commands, offensive playbooks, instructions to disrupt third-party systems |
| Storage | In-memory deterministic demo state | Secrets, private client logs, production indicators, personally identifiable information |

## References

[1] [MITRE ATT&CK — ATT&CK Data & Tools](https://attack.mitre.org/resources/attack-data-and-tools/)

[2] [CISA — Automated Indicator Sharing (AIS)](https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais)

[3] [OASIS — Introduction to STIX 2.1](https://oasis-open.github.io/cti-documentation/stix/intro.html)
