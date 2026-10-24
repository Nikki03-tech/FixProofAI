import { useState } from "react";
import {
  Check,
  Clipboard,
  Download,
  FlaskConical,
  Wrench,
} from "lucide-react";
import type { AnalysisResponse } from "../types";

interface ReportPanelProps {
  result: AnalysisResponse;
  onDownload: () => Promise<string>;
}

export default function ReportPanel({
  result,
  onDownload,
}: ReportPanelProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [downloadError, setDownloadError] = useState("");
  const [downloading, setDownloading] = useState(false);

  async function copyCode(code: string, index: number) {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedIndex(index);
      window.setTimeout(() => setCopiedIndex(null), 1800);
    } catch {
      setDownloadError("Could not copy code. Please select and copy it manually.");
    }
  }

  async function handleDownload() {
    setDownloading(true);
    setDownloadError("");

    try {
      const report = await onDownload();
      const blob = new Blob([report], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "fixproof-ai-report.md";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (error) {
      setDownloadError(
        error instanceof Error ? error.message : "Could not generate the report."
      );
    } finally {
      setDownloading(false);
    }
  }

  return (
    <section className="panel report-panel">
      <div className="panel-heading">
        <div className="panel-heading-icon fixes-icon">
          <Wrench size={19} />
        </div>
        <div>
          <h2>Suggested improvements</h2>
          <p>Review each suggestion before applying it.</p>
        </div>
      </div>

      {result.suggested_fixes.length > 0 ? (
        <div className="fix-list">
          {result.suggested_fixes.map((fix, index) => (
            <article className="fix-card" key={`${index}-${fix.title}`}>
              <div className="fix-title-row">
                <span className="fix-number">{index + 1}</span>
                <h3>{fix.title}</h3>
                <button
                  type="button"
                  className="icon-button"
                  onClick={() => void copyCode(fix.code, index)}
                  aria-label={`Copy code for ${fix.title}`}
                  title="Copy suggested code"
                >
                  {copiedIndex === index ? <Check size={16} /> : <Clipboard size={16} />}
                </button>
              </div>
              <p>{fix.explanation}</p>
              <pre className="code-output">
                <code>{fix.code}</code>
              </pre>
              {copiedIndex === index && (
                <span className="copy-feedback">Code copied</span>
              )}
            </article>
          ))}
        </div>
      ) : (
        <p className="empty-message">No specific fixes were suggested.</p>
      )}

      <div className="analysis-section test-section">
        <h3>
          <FlaskConical size={17} />
          Suggested tests
          <span className="section-count">{result.tests.length}</span>
        </h3>

        {result.tests.length > 0 ? (
          result.tests.map((test, index) => (
            <article className="test-card" key={`${index}-${test.description}`}>
              <h4>{test.description}</h4>
              <pre className="code-output">
                <code>{test.test_code}</code>
              </pre>
            </article>
          ))
        ) : (
          <p className="empty-message">No test suggestions were provided.</p>
        )}
        <p className="verification-note">
          These are suggestions only. Tests have not been run by FixProof AI.
        </p>
      </div>

      <div className="download-row">
        <div>
          <h3>Your debugging report</h3>
          <p>Save the findings and suggestions as a Markdown file.</p>
        </div>
        <button
          type="button"
          className="secondary-button"
          onClick={() => void handleDownload()}
          disabled={downloading}
        >
          <Download size={17} />
          {downloading ? "Preparing..." : "Download report"}
        </button>
      </div>

      {downloadError && (
        <p className="error-message" role="alert">
          {downloadError}
        </p>
      )}
    </section>
  );
}
