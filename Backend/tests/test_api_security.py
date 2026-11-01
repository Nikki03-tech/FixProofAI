from fastapi.testclient import TestClient

from Backend.main import app, _rate_limit_buckets, _rate_limit_lock
from Backend.schemas import AnalysisResponse


client = TestClient(app)


def _clear_rate_limits():
    with _rate_limit_lock:
        _rate_limit_buckets.clear()


def _valid_analysis_response():
    return AnalysisResponse(
        success=True,
        summary="A simple test response.",
        root_cause="No issue was found in this mocked response.",
    )


def test_analysis_endpoint_rate_limits_requests(monkeypatch):
    import Backend.main as main_module

    _clear_rate_limits()
    monkeypatch.setattr(main_module, "ANALYZE_RATE_LIMIT_PER_MINUTE", 2)
    monkeypatch.setattr(
        main_module,
        "analyze_code",
        lambda **kwargs: _valid_analysis_response(),
    )

    payload = {"code": "print('hello')", "language": "python"}

    assert client.post("/api/analyze", json=payload).status_code == 200
    assert client.post("/api/analyze", json=payload).status_code == 200

    limited = client.post("/api/analyze", json=payload)
    assert limited.status_code == 429
    assert limited.headers.get("Retry-After")
    assert "rate limit" in limited.json()["detail"].lower()

    _clear_rate_limits()


def test_analysis_rejects_code_over_configured_limit():
    from Backend.config import MAX_CODE_LENGTH

    payload = {
        "code": "x" * (MAX_CODE_LENGTH + 1),
        "language": "python",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422
    assert "code" in response.text.lower()
