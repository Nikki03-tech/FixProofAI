import { ShieldCheck, Sparkles } from "lucide-react";

interface HeaderProps {
  apiStatus: "checking" | "online" | "offline";
}

export default function Header({ apiStatus }: HeaderProps) {
  const statusLabel = {
    checking: "Checking API",
    online: "API online",
    offline: "API unavailable",
  }[apiStatus];

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

      <div
        className={`header-status header-status--${apiStatus}`}
        role="status"
        aria-live="polite"
      >
        <span className="status-dot" />
        <span>{statusLabel}</span>
        <Sparkles size={16} />
      </div>
    </header>
  );
}
