import { useEffect, useMemo, useState } from "react";

import { api, type CaseListItem, type CaseReport } from "./api";

type Panel = "overview" | "evidence" | "brief" | "intake";

const localCaseExample = {
  case_id: "case-local-demo",
  title: "Explicitly supplied synthetic review",
  source_label: "Authorized local demonstration",
  narrative:
    "A synthetic phishing and remote service review record was supplied for local analyst triage. It requires authorized mail and access telemetry validation only.",
  confidence: "medium",
  tags: ["phishing", "suspicious-auth"],
  indicators: [
    {
      indicator_id: "ind-local-domain",
      kind: "domain",
      value: "training-portal.example",
      confidence: "medium",
      tags: ["phishing"]
    },
    {
      indicator_id: "ind-local-ipv4",
      kind: "ipv4",
      value: "203.0.113.18",
      confidence: "medium",
      tags: ["suspicious-auth"]
    }
  ],
  evidence: [
    {
      evidence_id: "ev-local-note",
      summary: "Synthetic analyst note limits this review to local training data and approved telemetry validation.",
      source_type: "training-scenario",
      observed_at: "2026-08-19T10:00:00Z"
    }
  ]
};

function priorityTone(priority: string) {
  if (priority.startsWith("Critical")) return "critical";
  if (priority.startsWith("High")) return "high";
  if (priority.startsWith("Elevated")) return "elevated";
  return "routine";
}

function scoreTone(score: number) {
  if (score >= 75) return "critical";
  if (score >= 50) return "high";
  if (score >= 25) return "elevated";
  return "routine";
}

function formatTimestamp(value: string) {
  return new Intl.DateTimeFormat("en", { dateStyle: "medium", timeStyle: "short", timeZone: "UTC" }).format(
    new Date(value)
  );
}

function App() {
  const [cases, setCases] = useState<CaseListItem[]>([]);
  const [report, setReport] = useState<CaseReport | null>(null);
  const [activePanel, setActivePanel] = useState<Panel>("overview");
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [copyState, setCopyState] = useState("Copy brief");
  const [localJson, setLocalJson] = useState(JSON.stringify(localCaseExample, null, 2));

  useEffect(() => {
    void (async () => {
      try {
        const availableCases = await api.listCases();
        setCases(availableCases);
        if (availableCases[0]) setReport(await api.getCase(availableCases[0].case_id));
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unable to load local case fixtures.");
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  const criticalCount = useMemo(
    () => cases.filter((item) => item.summary.risk_score >= 75).length,
    [cases]
  );

  async function selectCase(caseId: string) {
    setIsLoading(true);
    setError("");
    try {
      setReport(await api.getCase(caseId));
      setActivePanel("overview");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to load the selected case.");
    } finally {
      setIsLoading(false);
    }
  }

  async function analyzeSuppliedCase() {
    setIsAnalyzing(true);
    setError("");
    try {
      const parsed = JSON.parse(localJson) as unknown;
      const analyzed = await api.analyze(parsed);
      setReport(analyzed);
      setActivePanel("overview");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "The supplied local record could not be analyzed.");
    } finally {
      setIsAnalyzing(false);
    }
  }

  async function copyBrief() {
    if (!report) return;
    const content = [
      `THREATATLAS INTELLIGENCE BRIEF — ${report.title}`,
      "",
      report.brief.executive_summary,
      "",
      "Key observables:",
      ...report.brief.key_observables.map((item) => `- ${item}`),
      "",
      "Recommended validation actions:",
      ...report.brief.recommended_validation_actions.map((item) => `- ${item}`),
      "",
      "Limitations:",
      ...report.brief.limitations.map((item) => `- ${item}`)
    ].join("\n");
    try {
      await navigator.clipboard.writeText(content);
      setCopyState("Copied");
      window.setTimeout(() => setCopyState("Copy brief"), 1600);
    } catch {
      setCopyState("Copy unavailable");
      window.setTimeout(() => setCopyState("Copy brief"), 1600);
    }
  }

  if (isLoading && !report) {
    return <div className="boot-screen">Loading local intelligence workspace…</div>;
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="ThreatAtlas navigation">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true"><span>TA</span></div>
          <div>
            <p className="eyebrow">Cyber Invasion Army</p>
            <h1>ThreatAtlas</h1>
            <p className="brand-subtitle">Intelligence workspace</p>
          </div>
        </div>

        <nav className="side-nav" aria-label="Workspace sections">
          <button className="nav-item active"><span>⌂</span> Review queue <b>{cases.length}</b></button>
          <button className="nav-item" onClick={() => setActivePanel("brief")}><span>▣</span> Intelligence briefs</button>
          <button className="nav-item" onClick={() => setActivePanel("intake")}><span>＋</span> Local intake</button>
        </nav>

        <div className="side-rule" />
        <div className="profile-card">
          <div className="profile-head"><span className="presence" /> <span>LOCAL REVIEW PROFILE</span></div>
          <p>Safe synthetic fixtures and explicitly supplied sanitized JSON only.</p>
          <div className="profile-facts"><span>Outbound calls</span><b>0</b><span>Remote actions</span><b>0</b></div>
        </div>
        <p className="sidebar-foot">v0.1 · deterministic demo mode</p>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div className="breadcrumb"><span>Threat intelligence</span><span>/</span><b>Analyst review</b></div>
          <div className="topbar-actions"><span className="safe-pill"><i /> Local-only evidence</span><button className="avatar" aria-label="Analyst profile">SR</button></div>
        </header>

        <div className="content-wrap">
          <section className="intro">
            <div>
              <p className="eyebrow accent">REVIEW PRIORITIZATION</p>
              <h2>Turn authorized evidence into <em>clearer</em> analyst decisions.</h2>
              <p className="intro-copy">Explainable local scoring, safe ATT&CK-informed hypotheses, and client-ready defensive briefs—without a live feed, scanner, or remote action.</p>
            </div>
            <button className="outline-action" onClick={() => setActivePanel("intake")}>Review supplied JSON <span>→</span></button>
          </section>

          {error && <div className="error-banner" role="alert">{error}</div>}

          <section className="metric-grid" aria-label="Workspace metrics">
            <article className="metric-card"><span>Local case fixtures</span><strong>{cases.length}</strong><small>deterministic records</small></article>
            <article className="metric-card"><span>Critical review</span><strong className="critical-text">{criticalCount}</strong><small>analyst queue items</small></article>
            <article className="metric-card"><span>Network interactions</span><strong className="safe-text">0</strong><small>by design</small></article>
            <article className="metric-card workflow-card"><span>Workflow</span><strong>Evidence → review → brief</strong><small>human validation remains required</small></article>
          </section>

          <section className="review-layout">
            <div className="case-column">
              <div className="section-heading"><div><p className="eyebrow">ANALYST QUEUE</p><h3>Local cases</h3></div><span>{cases.length} records</span></div>
              <div className="case-list">
                {cases.map((item) => (
                  <button
                    className={`case-item ${report?.case_id === item.case_id ? "selected" : ""}`}
                    key={item.case_id}
                    onClick={() => void selectCase(item.case_id)}
                  >
                    <div className="case-item-top"><span className={`priority-dot ${priorityTone(item.summary.priority)}`} /><span className="case-score">{item.summary.risk_score}</span><span className={`priority-label ${priorityTone(item.summary.priority)}`}>{item.summary.priority.replace(" review", "")}</span></div>
                    <strong>{item.title}</strong>
                    <p>{item.source_label}</p>
                    <div className="tag-row">{item.tags.length ? item.tags.map((tag) => <span key={tag}>{tag}</span>) : <span>unclassified</span>}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="report-column">
              {report ? (
                <>
                  <div className="report-head">
                    <div><p className="eyebrow">ACTIVE REVIEW</p><h3>{report.title}</h3><p>{report.source_label}</p></div>
                    <div className={`score-orb ${scoreTone(report.summary.risk_score)}`}><span>{report.summary.risk_score}</span><small>/100</small></div>
                  </div>

                  <div className="report-tabs" role="tablist" aria-label="Active case review panels">
                    {(["overview", "evidence", "brief", "intake"] as Panel[]).map((panel) => (
                      <button key={panel} className={activePanel === panel ? "tab active" : "tab"} onClick={() => setActivePanel(panel)}>
                        {panel === "overview" ? "Triage" : panel === "evidence" ? "Evidence" : panel === "brief" ? "Client brief" : "Local intake"}
                      </button>
                    ))}
                  </div>

                  {activePanel === "overview" && <Overview report={report} />}
                  {activePanel === "evidence" && <Evidence report={report} />}
                  {activePanel === "brief" && <Brief report={report} copyState={copyState} onCopy={() => void copyBrief()} />}
                  {activePanel === "intake" && (
                    <Intake json={localJson} onChange={setLocalJson} onAnalyze={() => void analyzeSuppliedCase()} isAnalyzing={isAnalyzing} />
                  )}
                </>
              ) : <div className="empty-state">Choose a local case to begin review.</div>}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

function Overview({ report }: { report: CaseReport }) {
  return (
    <div className="panel-stack">
      <section className="summary-strip">
        <div><span>Review priority</span><strong className={priorityTone(report.summary.priority)}>{report.summary.priority}</strong></div>
        <div><span>Source confidence</span><strong className="titlecase">{report.summary.confidence}</strong></div>
        <div><span>Unique observables</span><strong>{report.summary.unique_indicator_count}</strong></div>
        <div><span>Evidence fragments</span><strong>{report.summary.evidence_count}</strong></div>
      </section>
      <section className="panel-card narrative-card"><p className="eyebrow">CASE NARRATIVE</p><p>{report.narrative}</p></section>
      <div className="two-column">
        <section className="panel-card">
          <div className="card-heading"><div><p className="eyebrow">WHY THIS SCORE</p><h4>Visible priority factors</h4></div><span className="sum-note">bounded to 100</span></div>
          <div className="factor-list">
            {report.priority_factors.map((factor) => (
              <div className="factor-row" key={factor.label}><div><strong>{factor.label}</strong><p>{factor.detail}</p></div><b>+{factor.points}</b></div>
            ))}
          </div>
        </section>
        <section className="panel-card">
          <div className="card-heading"><div><p className="eyebrow">ATT&CK CONTEXT</p><h4>Hypotheses to validate</h4></div><span className="review-badge">not attribution</span></div>
          {report.technique_suggestions.length ? <div className="tech-list">{report.technique_suggestions.map((item) => <div className="tech-row" key={item.technique_id}><span>{item.technique_id}</span><div><strong>{item.name}</strong><p>{item.tactic} · {item.confidence} confidence</p></div></div>)}</div> : <p className="quiet-copy">No catalogue hypothesis was triggered from the supplied local record.</p>}
        </section>
      </div>
      <section className="notice-card"><span>⊙</span><p><b>Analysis boundary.</b> This workspace has evaluated only supplied local evidence. No remote enrichment, scanning, probing, automated response, or attribution occurred.</p></section>
    </div>
  );
}

function Evidence({ report }: { report: CaseReport }) {
  return (
    <div className="panel-stack">
      <section className="panel-card"><div className="card-heading"><div><p className="eyebrow">NORMALIZED OBSERVABLES</p><h4>Deduplicated local indicators</h4></div><span className="sum-note">{report.summary.duplicate_indicator_count} merged duplicate(s)</span></div>
        <div className="table-wrap"><table><thead><tr><th>Type</th><th>Value</th><th>Confidence</th><th>Context</th></tr></thead><tbody>{report.indicators.map((item) => <tr key={item.indicator_id}><td><span className="kind-chip">{item.kind}</span></td><td className="mono">{item.value}</td><td className="titlecase">{item.confidence}</td><td>{item.tags.length ? item.tags.join(", ") : "—"}{item.duplicate_count ? ` · ${item.duplicate_count} duplicate merged` : ""}</td></tr>)}</tbody></table></div>
      </section>
      <section className="panel-card"><div className="card-heading"><div><p className="eyebrow">SUPPLIED EVIDENCE</p><h4>Reviewable rationale</h4></div></div>
        <div className="evidence-list">{report.evidence.length ? report.evidence.map((item) => <article key={item.evidence_id}><div className="evidence-icon">◇</div><div><p>{item.summary}</p><span>{item.source_type.replace("-", " ")} · {formatTimestamp(item.observed_at)} UTC</span></div></article>) : <p className="quiet-copy">No supporting evidence fragments were supplied with this record.</p>}</div>
      </section>
    </div>
  );
}

function Brief({ report, copyState, onCopy }: { report: CaseReport; copyState: string; onCopy: () => void }) {
  return (
    <div className="panel-stack">
      <section className="brief-card"><div className="brief-top"><div><p className="eyebrow">CLIENT-READY INTELLIGENCE BRIEF</p><h4>{report.title}</h4></div><button className="copy-button" onClick={onCopy}>{copyState}</button></div>
        <div className="brief-section"><h5>Executive summary</h5><p>{report.brief.executive_summary}</p></div>
        <div className="brief-grid"><div className="brief-section"><h5>Key observables</h5><ul>{report.brief.key_observables.map((item) => <li key={item}>{item}</li>)}</ul></div><div className="brief-section"><h5>Recommended validation</h5><ol>{report.brief.recommended_validation_actions.map((item) => <li key={item}>{item}</li>)}</ol></div></div>
        <div className="limitations"><h5>Limitations</h5>{report.brief.limitations.map((item) => <p key={item}>— {item}</p>)}</div>
      </section>
    </div>
  );
}

function Intake({ json, onChange, onAnalyze, isAnalyzing }: { json: string; onChange: (value: string) => void; onAnalyze: () => void; isAnalyzing: boolean }) {
  return (
    <div className="panel-stack">
      <section className="intake-head"><div><p className="eyebrow">EXPLICITLY SUPPLIED LOCAL RECORD</p><h4>Analyze sanitized JSON</h4><p>Paste only a synthetic or explicitly authorized, sanitized record. This endpoint runs local validation and deterministic scoring; it does not save the record or contact any external system.</p></div><span className="local-stamp">LOCAL-ONLY</span></section>
      <label className="json-label" htmlFor="local-json">Case JSON</label>
      <textarea id="local-json" className="json-area" value={json} onChange={(event) => onChange(event.target.value)} spellCheck="false" />
      <div className="intake-actions"><p>By submitting, you confirm that the content is synthetic or authorized for local review.</p><button className="primary-action" onClick={onAnalyze} disabled={isAnalyzing}>{isAnalyzing ? "Analyzing local record…" : "Analyze supplied record"} <span>→</span></button></div>
    </div>
  );
}

export default App;
