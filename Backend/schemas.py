from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from Backend.config import MAX_CODE_LENGTH
SupportedLanguage = Literal["python", "javascript"]
ExplanationLevel = Literal["beginner", "intermediate", "advanced"]
Severity = Literal["critical", "high", "medium", "low", "none"]
class AnalysisRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)
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
    severity: Severity = "none"
    confidence: int = Field(default=50, ge=0, le=100)
    verification_steps: list[str] = Field(default_factory=list)
    suggested_fixes: list[SuggestedFix] = Field(default_factory=list)
    tests: list[TestSuggestion] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
