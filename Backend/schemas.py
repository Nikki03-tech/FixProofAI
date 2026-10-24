from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


SupportedLanguage = Literal["python", "javascript"]
ExplanationLevel = Literal["beginner", "intermediate", "advanced"]


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    code: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="Source code to analyze. The backend will not execute it.",
    )
    language: SupportedLanguage
    explanation_level: ExplanationLevel = "beginner"
    include_tests: bool = True


class SuggestedFix(BaseModel):
    title: str
    explanation: str
    code: str


class TestSuggestion(BaseModel):
    description: str
    test_code: str


class AnalysisResponse(BaseModel):
    success: bool
    summary: str
    issues: list[str] = Field(default_factory=list)
    root_cause: str
    suggested_fixes: list[SuggestedFix] = Field(default_factory=list)
    tests: list[TestSuggestion] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
