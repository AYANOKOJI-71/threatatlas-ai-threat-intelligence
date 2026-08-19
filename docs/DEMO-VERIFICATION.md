# ThreatAtlas Demonstration Verification

## Environment

| Component | Verified setting |
|---|---|
| API | Local FastAPI process on `127.0.0.1:4910` |
| Web console | Local Vite process on port `5201` with same-origin API proxy |
| Data mode | Three bundled deterministic, synthetic fixtures; no live feed, client record, remote enrichment, or target interaction |
| Visual review | Analyst console opened through the temporary preview endpoint and rendered successfully against the local API |

## Verified analyst workflow

| Step | Result |
|---|---|
| Queue loading | The interface rendered a three-case local analyst queue with two critical-review items, one routine-review item, and a visible zero-network-interactions guardrail. |
| High-priority triage | The synthetic remote-access/outbound-transfer fixture rendered a **100/100 Critical review** result from two unique observables, three evidence fragments, high source confidence, and two ATT&CK-informed hypotheses. |
| Explainability | The Triage view displayed each bounded scoring factor: source confidence (+30), observable categories (+18), defensive themes (+34), corroborating evidence (+12), and ATT&CK-informed hypotheses (+6). |
| ATT&CK context | The console displayed T1021 Remote Services and T1567 Exfiltration Over Web Service as **hypotheses to validate**, explicitly labelled “not attribution.” |
| Evidence review | The Evidence view displayed deduplicated observables and all three supplied synthetic evidence fragments with their source type and UTC timestamp. |
| Safety boundary | The dashboard and sidebar visibly stated that only local synthetic fixtures or explicitly supplied sanitized JSON are supported; outbound calls and remote actions were both shown as zero. |

## Visual checks

The desktop layout retained clear hierarchy, readable contrast, and a deliberate dark analyst-workspace presentation. The selected-case state, priority colour treatment, score orb, evidence table, and source labels were visually readable. The responsive styles include tablet and mobile breakpoints; browser verification covered the desktop workflow.

## Additional verified panels

| Panel | Result |
|---|---|
| Client-ready brief | The Brief view rendered the executive summary, observable list, validation actions, limitations, and copy control. It clearly described the output as a triage aid rather than confirmation of malicious activity or attribution. |
| Local JSON intake | The Local intake view rendered a prefilled synthetic example and prominently stated that supplied content must be synthetic or authorized and sanitized. The panel states that records are not saved and that no external system is contacted. |
| End-to-end local analysis | Submitting the prefilled synthetic record returned a **71/100 High review** result with two unique observables, one evidence fragment, medium source confidence, and two clearly labelled ATT&CK-informed hypotheses: T1566 Phishing and T1021 Remote Services. The returned narrative and score-factor evidence remained visible, including the “not attribution” and local-analysis-boundary labels. |

## Release note

All core analyst-workflow panels, including local JSON submission, have been visually verified. The final pre-publication check remains the full automated quality gate and release-tree review.
