import { BrainCircuit, LoaderCircle, ShieldCheck } from "lucide-react";

export default function LoadingState() {
  return (
    <div className="loading-card" role="status" aria-live="polite">
      <div className="loading-icon">
        <BrainCircuit size={28} />
        <span className="loading-orbit" />
      </div>

      <div className="loading-copy">
        <h3>Reviewing your code</h3>
        <p>
          Looking for potential issues, tracing likely root causes, and
          preparing suggestions.
        </p>
        <div className="loading-progress">
          <span />
        </div>
        <span className="loading-note">
          <LoaderCircle className="spin-icon" size={14} />
          AI analysis in progress — your code is not being executed
        </span>
      </div>

      <ShieldCheck className="loading-shield" size={22} />
    </div>
  );
}
