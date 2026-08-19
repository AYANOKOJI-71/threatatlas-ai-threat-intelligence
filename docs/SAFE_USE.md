# ThreatAtlas Safe Use

## Authorization rule

Use ThreatAtlas only with synthetic records or data that your organization is expressly authorized to process. In a client engagement, confirm scope, data ownership, retention rules, and review authority before entering information into any intelligence workflow.

## Demo-mode guarantees

| Guarantee | Implementation |
|---|---|
| No external collection | The application makes no outbound HTTP calls and loads only repository fixtures or explicitly supplied sanitized JSON. |
| No target interaction | It has no scanners, probes, exploit modules, remote shells, or blocking controls. |
| No executable content | Fixtures contain text and safe observables only; no malware, payloads, or credential material are stored. |
| No automatic sharing | There is no TAXII/AIS client, feed key, certificate handling, or send operation. |
| Human validation | Every prioritization and ATT&CK mapping is displayed as a suggestion supported by visible factors and limitations. |

## Production considerations

CISA describes AIS as a controlled mechanism for sharing machine-readable threat indicators and defensive measures; participation involves documented terms, a STIX/TAXII capability, and onboarding requirements.[1] Any real feed integration should therefore be separately designed with data classification, least-privilege credentials, audit logging, rate limiting, legal review, and a human approval workflow. Those capabilities are explicitly out of scope for the portfolio demonstration.

## Reference

[1] [CISA — Automated Indicator Sharing (AIS)](https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais)
