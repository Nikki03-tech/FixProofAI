import { AlertTriangle, CheckCircle2, Lightbulb, SearchCheck, ShieldAlert } from "lucide-react";
import type { AnalysisResponse, SupportedLanguage } from "../types";

interface AnalysisPanelProps {
  result: AnalysisResponse;
  onSelectLanguage: (language: SupportedLanguage) => void;
}

const languageName = (language: SupportedLanguage) =>
  language === "python" ? "Python" : "JavaScript";

export default function AnalysisPanel({ result, onSelectLanguage }: AnalysisPanelProps) {
  const hasMismatch = result.language_mismatch && result.detected_language;

  return (
    <section className="panel analysis-panel">
      <div className="panel-heading">
        <div className="panel-heading-icon result-icon"><SearchCheck size={20} /></div>
        <div><h2>Analysis overview</h2><p>AI-generated findings for your review.</p></div>
        <span className={`result-badge ${result.success ? "success" : "warning"}`}>
          {result.success ? <CheckCircle2 size={14} /> : <AlertTriangle size={14} />}
          {result.success ? "Analysis ready" : "Partial result"}
        </span>
      </div>

      {hasMismatch && (
        <div className="language-warning" role="alert">
          <div className="language-warning-copy">
            <strong>Language mismatch detected</strong>
            <p>
              You selected {languageName(result.selected_language ?? "javascript")},
              but your code looks like {languageName(result.detected_language)}.
              The analysis was run as {languageName(result.detected_language)}.
            </p>
          </div>
          <button
            type="button"
            className="language-switch-button"
            onClick={() => onSelectLanguage(result.detected_language!)}
          >
            Switch to {languageName(result.detected_language)}
          </button>
        </div>
      )}

      <div className="summary-card">
        <h3>Summary</h3><p>{result.summary}</p>
        <p><strong>Severity:</strong> {result.severity.toUpperCase()} · <strong>AI confidence:</strong> {result.confidence}%</p>
      </div>
      <div className="analysis-section">
        <h3><AlertTriangle size={17} />Potential issues<span className="section-count">{result.issues.length}</span></h3>
        {result.issues.length ? <ul className="issue-list">{result.issues.map((issue, index) => (
          <li key={`${index}-${issue}`}><span className="issue-marker">{index + 1}</span><span>{issue}</span></li>
        ))}</ul> : <p className="empty-message">No specific issues were identified. This does not guarantee the code is bug-free.</p>}
      </div>
      <div className="analysis-section root-cause-section">
        <h3><Lightbulb size={17} />Likely root cause</h3><p>{result.root_cause}</p>
      </div>
      <div className="analysis-section">
        <h3><CheckCircle2 size={17} />Verification checklist</h3>
        {result.verification_steps.length ? <ul className="issue-list">{result.verification_steps.map((step, index) => (
          <li key={`${index}-${step}`}><span className="issue-marker">✓</span><span>{step}</span></li>
        ))}</ul> : <p className="empty-message">Review the changes and run relevant tests in a safe environment.</p>}
      </div>
      {result.limitations.length > 0 && <div className="limitations-card">
        <h3><ShieldAlert size={17} />Limitations to keep in mind</h3>
        <ul>{result.limitations.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}</ul>
      </div>}
      <p className="verification-note">Confidence is an AI estimate, not a guarantee. Suggestions have not been independently verified.</p>
    </section>
  );
}
