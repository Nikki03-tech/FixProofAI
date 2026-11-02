from fastapi.testclient import TestClient

from Backend.main import app

client = TestClient(app)


def test_language_mismatch_is_reported_and_analysis_uses_detected_language(monkeypatch):
    import Backend.main as main_module
    from Backend.schemas import AnalysisResponse

    observed = {}

    def fake_analyze_code(**kwargs):
        observed["language"] = kwargs["language"]
        return AnalysisResponse(
            success=True, summary="Python analysis", root_cause="Python source."
        )

    monkeypatch.setattr(main_module, "analyze_code", fake_analyze_code)
    with main_module._rate_limit_lock:
        main_module._rate_limit_buckets.clear()

    response = client.post("/api/analyze", json={
        "code": "def greet(name):\n    print('hello', name)",
        "language": "javascript",
    })

    assert response.status_code == 200
    body = response.json()
    assert observed["language"] == "python"
    assert body["selected_language"] == "javascript"
    assert body["detected_language"] == "python"
    assert body["language_mismatch"] is True
