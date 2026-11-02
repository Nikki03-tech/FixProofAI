import json

import httpx
import pytest

from Backend.services import ai_service


def test_analyze_code_requires_gemini_api_key(monkeypatch):
    monkeypatch.setattr(ai_service, "GEMINI_API_KEY", "")
    with pytest.raises(ai_service.AIServiceError, match="GEMINI_API_KEY"):
        ai_service.analyze_code(code="print('hello')", language="python")


def _mock_gemini(monkeypatch, response):
    class FakeClient:
        def __init__(self, timeout):
            self.timeout = timeout
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def post(self, *args, **kwargs):
            return response
    monkeypatch.setattr(ai_service, "GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(ai_service.httpx, "Client", FakeClient)


def test_valid_gemini_response_is_parsed(monkeypatch):
    payload = {
        "success": True, "summary": "Possible name error.",
        "issues": ["Undefined identifier."], "root_cause": "Wrong variable name.",
        "severity": "high", "confidence": 92,
        "verification_steps": ["Run with a three-item list."],
        "suggested_fixes": [], "tests": [], "limitations": ["Static analysis only."]
    }
    response = httpx.Response(200, json={
        "candidates": [{"content": {"parts": [{"text": json.dumps(payload)}]}}]
    })
    _mock_gemini(monkeypatch, response)
    result = ai_service.analyze_code("return len(number)", "python")
    assert result.severity == "high"
    assert result.confidence == 92
    assert result.verification_steps


def test_malformed_gemini_json_is_rejected(monkeypatch):
    response = httpx.Response(200, json={
        "candidates": [{"content": {"parts": [{"text": "{bad json"}]}}]
    })
    _mock_gemini(monkeypatch, response)
    with pytest.raises(ai_service.AIServiceError, match="invalid analysis"):
        ai_service.analyze_code("print(1)", "python")


def test_gemini_http_failure_is_reported(monkeypatch):
    response = httpx.Response(429, json={"error": {"status": "RESOURCE_EXHAUSTED"}})
    _mock_gemini(monkeypatch, response)
    with pytest.raises(ai_service.AIServiceError, match="HTTP 429"):
        ai_service.analyze_code("print(1)", "python")


def test_gemini_timeout_is_reported(monkeypatch):
    class FakeClient:
        def __init__(self, timeout):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def post(self, *args, **kwargs):
            raise httpx.ReadTimeout("timeout")
    monkeypatch.setattr(ai_service, "GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(ai_service.httpx, "Client", FakeClient)
    with pytest.raises(ai_service.AIServiceError, match="timed out"):
        ai_service.analyze_code("print(1)", "python")
