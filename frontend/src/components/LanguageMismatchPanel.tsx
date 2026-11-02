import { AlertTriangle, ArrowRight } from "lucide-react";
import type { SupportedLanguage } from "../types";
interface LanguageMismatchPanelProps {
  selectedLanguage: SupportedLanguage;
  detectedLanguage: SupportedLanguage;
  message: string;
  onSwitchAndAnalyze: () => void;
}
const nameOf = (language: SupportedLanguage) => language === "python" ? "Python" : "JavaScript";
export default function LanguageMismatchPanel({ selectedLanguage, detectedLanguage, message, onSwitchAndAnalyze }: LanguageMismatchPanelProps) {
  return (
    <section className="panel language-gate-panel" role="alert" aria-live="assertive">
      <div className="language-gate-icon"><AlertTriangle size={25} /></div>
      <span className="eyebrow">ANALYSIS PAUSED</span>
      <h2>Language mismatch detected</h2>
      <p>{message}</p>
      <div className="language-comparison">
        <div><span>Selected language</span><strong>{nameOf(selectedLanguage)}</strong></div>
        <ArrowRight size={18} />
        <div><span>Detected language</span><strong>{nameOf(detectedLanguage)}</strong></div>
      </div>
      <p className="language-gate-note">No AI analysis has been run yet. Switch to the detected language to continue.</p>
      <button className="language-switch-button" type="button" onClick={onSwitchAndAnalyze}>
        Switch to {nameOf(detectedLanguage)} and analyze
      </button>
    </section>
  );
}
