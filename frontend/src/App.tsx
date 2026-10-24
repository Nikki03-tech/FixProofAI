import { useState } from "react";
import {
  ArrowDown,
  Code2,
  Github,
  RotateCcw,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import Header from "./components/Header";
import CodeEditor from "./components/CodeEditor";
import LoadingState from "./components/LoadingState";
import AnalysisPanel from "./components/AnalysisPanel";
import ReportPanel from "./components/ReportPanel";

import { analyzeCode, downloadReport } from "./services/api";

import type {
  AnalysisRequest,
  AnalysisResponse,
  ExplanationLevel,
  SupportedLanguage,
} from "./types";

const INITIAL_CODE = `def calculate_average(numbers):
    total = sum(numbers)
    return total / len(number)

scores = [80, 90, 75]
print(calculate_average(scores))`;

export default function App() {
  const [code, setCode] = useState(INITIAL_CODE);
  const [language, setLanguage] = useState<SupportedLanguage>("python");
  const [explanationLevel, setExplanationLevel] =
    useState<ExplanationLevel>("beginner");
  const [includeTests, setIncludeTests] = useState(true);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<AnalysisRequest | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (!code.trim()) {
      setError("Please enter some code to analyze.");
      return;
    }

    if (code.length > 20000) {
      setError("Your code exceeds the 20,000-character limit.");
      return;
    }

    const payload: AnalysisRequest = {
      code,
      language,
      explanation_level: explanationLevel,
      include_tests: includeTests,
    };

    setIsLoading(true);
    setError("");
    setResult(null);
    setLastRequest(null);

    try {
      const analysis = await analyzeCode(payload);
      setResult(analysis);
      setLastRequest(payload);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while analyzing your code."
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDownload(): Promise<string> {
    if (!result || !lastRequest) {
      throw new Error("Analyze your code before downloading a report.");
    }

    return downloadReport(lastRequest, result);
  }

  function handleReset() {
    setCode("");
    setResult(null);
    setLastRequest(null);
    setError("");
  }

  return (
    <div className="app-shell">
      <Header />

      <main className="main-content">
        <section className="hero-section">
          <div className="hero-pill">
            <Sparkles size={15} />
            Your AI debugging companion
          </div>

          <h1>
            Debug smarter.
            <br />
            <span>Build with confidence.</span>
          </h1>

          <p className="hero-description">
            Understand tricky bugs, explore likely root causes, and get
            practical code suggestions — all in one place.
          </p>

          <div className="hero-benefits">
            <span>
              <ShieldCheck size={16} />
              Code isn't executed
            </span>
            <span>
              <Code2 size={16} />
              Python &amp; JavaScript
            </span>
            <span>
              <Sparkles size={16} />
              Clear explanations
            </span>
          </div>
        </section>

        <div className="workspace-heading">
          <div>
            <span className="eyebrow">THE WORKSPACE</span>
            <h2>Let's find the problem</h2>
          </div>

          <button
            type="button"
            className="text-button reset-button"
            onClick={handleReset}
          >
            <RotateCcw size={15} />
            Clear workspace
          </button>
        </div>

        <div className="workspace-grid">
          <CodeEditor
            code={code}
            onCodeChange={setCode}
            language={language}
            onLanguageChange={setLanguage}
            explanationLevel={explanationLevel}
            onExplanationLevelChange={setExplanationLevel}
            includeTests={includeTests}
            onIncludeTestsChange={setIncludeTests}
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
          />

          <section className="results-column" aria-live="polite">
            {isLoading ? (
              <LoadingState />
            ) : error ? (
              <div className="panel error-panel" role="alert">
                <div className="error-symbol">!</div>
                <h2>We couldn't complete the analysis</h2>
                <p>{error}</p>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={handleAnalyze}
                >
                  <RotateCcw size={16} />
                  Try again
                </button>
              </div>
            ) : result ? (
              <>
                <AnalysisPanel result={result} />
                <ReportPanel
                  result={result}
                  onDownload={handleDownload}
                />
              </>
            ) : (
              <div className="panel results-placeholder">
                <div className="placeholder-art">
                  <div className="placeholder-circle circle-one" />
                  <div className="placeholder-circle circle-two" />
                  <div className="placeholder-icon">
                    <ShieldCheck size={38} />
                  </div>
                  <span className="floating-code">&lt;/&gt;</span>
                  <span className="floating-sparkle">
                    <Sparkles size={18} />
                  </span>
                </div>

                <span className="eyebrow">READY WHEN YOU ARE</span>
                <h2>Your insights will appear here</h2>
                <p>
                  Add your code on the left and select Analyze my code. We'll
                  organize the findings, root cause, and possible improvements
                  here.
                </p>

                <div className="placeholder-hint">
                  <ArrowDown size={16} />
                  Start with the example code, or paste your own.
                </div>
              </div>
            )}
          </section>
        </div>

        <section className="trust-strip">
          <div className="trust-icon">
            <ShieldCheck size={20} />
          </div>
          <div>
            <strong>Your code stays under your control</strong>
            <p>
              FixProof AI does not execute submitted code. Review AI-generated
              suggestions and test changes before using them.
            </p>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <a className="footer-brand" href="/" aria-label="FixProof AI home">
          <ShieldCheck size={17} />
          FixProof AI
        </a>
        <span>Understand. Debug. Improve.</span>
        <a
          className="footer-link"
          href="https://github.com/Nikki03-tech/FixProofAI"
          target="_blank"
          rel="noreferrer"
        >
          <Github size={16} />
          GitHub
        </a>
      </footer>
    </div>
  );
}
