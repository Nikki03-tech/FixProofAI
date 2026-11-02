from Backend.schemas import AnalysisResponse, SuggestedFix, TestSuggestion
from Backend.services.report_service import generate_markdown_report


def test_report_contains_severity_confidence_and_verification():
    result = AnalysisResponse(
        success=True,
        summary="Possible undefined variable.",
        issues=["Variable is not defined."],
        root_cause="A misspelled identifier is referenced.",
        severity="high",
        confidence=91,
        verification_steps=["Run with a normal list.", "Try an empty list."],
        suggested_fixes=[SuggestedFix(
            title="Correct the name", explanation="Use the parameter.",
            code="return len(numbers)"
        )],
        tests=[TestSuggestion(
            description="Checks a list", test_code="assert len([1]) == 1"
        )],
    )
    report = generate_markdown_report(result, "python", "beginner")
    assert "**Severity:** High" in report
    assert "**AI confidence:** 91%" in report
    assert "- [ ] Run with a normal list." in report
    assert "## Suggested tests" in report
