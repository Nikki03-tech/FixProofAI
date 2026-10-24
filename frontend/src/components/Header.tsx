import { Bug, ShieldCheck, Sparkles } from "lucide-react";

export default function Header() {
  return (
    <header className="site-header">
      <a className="brand" href="/" aria-label="FixProof AI home">
        <span className="brand-icon">
          <ShieldCheck size={25} />
        </span>
        <span className="brand-copy">
          <span className="brand-name">
            FixProof <span>AI</span>
          </span>
          <span className="brand-tagline">Understand. Debug. Improve.</span>
        </span>
      </a>

      <div className="header-status">
        <span className="status-dot" />
        <span>AI debugging assistant</span>
        <Sparkles size={16} />
      </div>
    </header>
  );
}
