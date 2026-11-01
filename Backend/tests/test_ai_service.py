import pytest

from Backend.services import ai_service


def test_analyze_code_requires_gemini_api_key(monkeypatch):
    monkeypatch.setattr(ai_service, "GEMINI_API_KEY", "")

    with pytest.raises(ai_service.AIServiceError, match="GEMINI_API_KEY"):
        ai_service.analyze_code(
            code="print('hello')",
            language="python",
        )
