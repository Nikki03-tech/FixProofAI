import { Code2, FileCode2, FlaskConical, Sparkles } from "lucide-react";
import type {
  ExplanationLevel,
  SupportedLanguage,
} from "../types";

interface CodeEditorProps {
  code: string;
  onCodeChange: (code: string) => void;
  language: SupportedLanguage;
  onLanguageChange: (language: SupportedLanguage) => void;
  explanationLevel: ExplanationLevel;
  onExplanationLevelChange: (level: ExplanationLevel) => void;
  includeTests: boolean;
  onIncludeTestsChange: (include: boolean) => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

const EXAMPLE_CODE: Record<SupportedLanguage, string> = {
  python: `def calculate_average(numbers):
    total = sum(numbers)
    return total / len(number)

scores = [80, 90, 75]
print(calculate_average(scores))`,
  javascript: `function calculateAverage(numbers) {
  const total = numbers.reduce((sum, n) => sum + n, 0);
  return total / numbers.length;
}

const scores = [80, 90, 75];
console.log(calculateAverage(scores));`,
};

export default function CodeEditor({
  code,
  onCodeChange,
  language,
  onLanguageChange,
  explanationLevel,
  onExplanationLevelChange,
  includeTests,
  onIncludeTestsChange,
  onAnalyze,
  isLoading,
}: CodeEditorProps) {
  return (
    <section className="panel editor-panel">
      <div className="panel-heading">
        <div className="panel-heading-icon">
          <Code2 size={19} />
        </div>
        <div>
          <h2>Inspect your code</h2>
          <p>Share a snippet to uncover potential issues.</p>
        </div>
      </div>

      <div className="editor-toolbar">
        <label className="field-label" htmlFor="language">
          <FileCode2 size={15} />
          Language
        </label>
        <select
          id="language"
          value={language}
          onChange={(event) =>
            onLanguageChange(event.target.value as SupportedLanguage)
          }
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
        </select>

        <button
          className="text-button"
          type="button"
          onClick={() => onCodeChange(EXAMPLE_CODE[language])}
        >
          Load example
        </button>
      </div>

      <label className="sr-only" htmlFor="source-code">
        Source code to analyze
      </label>
      <textarea
        id="source-code"
        className="code-input"
        value={code}
        onChange={(event) => onCodeChange(event.target.value)}
        placeholder="Paste your code here..."
        spellCheck={false}
        autoCapitalize="off"
        autoCorrect="off"
        maxLength={20000}
      />

      <div className="editor-footer">
        <span>{code.length.toLocaleString()} / 20,000 characters</span>
        <span>Code is analyzed, not executed</span>
      </div>

      <div className="editor-options">
        <div className="option-field">
          <label htmlFor="explanation-level">Explanation level</label>
          <select
            id="explanation-level"
            value={explanationLevel}
            onChange={(event) =>
              onExplanationLevelChange(
                event.target.value as ExplanationLevel
              )
            }
          >
            <option value="beginner">Beginner-friendly</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <label className="checkbox-option">
          <input
            type="checkbox"
            checked={includeTests}
            onChange={(event) => onIncludeTestsChange(event.target.checked)}
          />
          <FlaskConical size={16} />
          Include test suggestions
        </label>
      </div>

      <button
        className="primary-button analyze-button"
        type="button"
        onClick={onAnalyze}
        disabled={isLoading || !code.trim()}
      >
        <Sparkles size={18} />
        {isLoading ? "Analyzing code..." : "Analyze my code"}
      </button>
    </section>
  );
}
