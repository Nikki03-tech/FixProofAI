import {
  AlertTriangle,
  CheckCircle2,
  Lightbulb,
  SearchCheck,
  ShieldAlert,
} from "lucide-react";
import type { AnalysisResponse } from "../types";

interface AnalysisPanelProps {
  result: AnalysisResponse;
}

export default function AnalysisPanel({ result }: AnalysisPanelProps) {
  return (
    <section className="panel analysis-panel">
      <div className="panel-heading">
        <div className="panel-heading-icon result-icon">
          <SearchCheck size={20} />
        </div>
        <div>
          <h2>Analysis overview</h2>
          <p>AI-generated findings for your review.</p>
        </div>
        <span className={`result-badge ${result.success ? "success" : "warning"}`}>
          {result.success ? (
            <CheckCircle2 size={14} />
          ) : (
            <AlertTriangle size={14} />
          )}
          {result.success ? "Analysis ready" : "Partial result"}
        </span>
      </div>

      <div className="summary-card">
        <h3>Summary</h3>
        <p>{result.summary}</p>
      </div>

      <div className="analysis-section">
        <h3>
          <AlertTriangle size={17} />
          Potential issues
          <span className="section-count">{result.issues.length}</span>
        </h3>
        {result.issues.length ? (
          <ul className="issue-list">
            {result.issues.map((issue, index) => (
              <li key={`${index}-${issue}`}>
                <span className="issue-marker">{index + 1}</span>
                <span>{issue}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty-message">
            No specific issues were identified. This does not guarantee the
            code is bug-free.
          </p>
        )}
      </div>

      <div className="analysis-section root-cause-section">
        <h3>
          <Lightbulb size={17} />
          Likely root cause
        </h3>
        <p>{result.root_cause}</p>
      </div>

      {result.limitations.length > 0 && (
        <div className="limitations-card">
          <h3>
            <ShieldAlert size={17} />
            Limitations to keep in mind
          </h3>
          <ul>
            {result.limitations.map((item, index) => (
              <li key={`${index}-${item}`}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      <p className="verification-note">
        AI-generated suggestions may be incorrect. Review changes and run
        appropriate tests before using them.
      </p>
    </section>
  );
}
