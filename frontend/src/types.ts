export type SupportedLanguage = "python" | "javascript";

export type ExplanationLevel = "beginner" | "intermediate" | "advanced";

export interface AnalysisRequest {
  code: string;
  language: SupportedLanguage;
  explanation_level: ExplanationLevel;
  include_tests: boolean;
}

export interface SuggestedFix {
  title: string;
  explanation: string;
  code: string;
}

export interface TestSuggestion {
  description: string;
  test_code: string;
}

export interface AnalysisResponse {
  success: boolean;
  summary: string;
  issues: string[];
  root_cause: string;
  suggested_fixes: SuggestedFix[];
  tests: TestSuggestion[];
  limitations: string[];
}

export interface HealthResponse {
  status: string;
  app: string;
  version: string;
}
