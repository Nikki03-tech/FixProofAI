from fastapi.testclient import TestClient
from Backend.main import app
client = TestClient(app)
def _clear_rate_limit_state():
    import Backend.main as main_module
    with main_module._rate_limit_lock:
        main_module._rate_limit_buckets.clear()
def test_language_mismatch_stops_before_gemini_call(monkeypatch):
    import Backend.main as main_module
    _clear_rate_limit_state()
    def gemini_must_not_run(**kwargs):
        raise AssertionError("Gemini must not run until the language is corrected.")
    monkeypatch.setattr(main_module, "analyze_code", gemini_must_not_run)
    response = client.post("/api/analyze", json={"code": "def greet(name):\n    print('hello', name)", "language": "javascript"})
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["code"] == "LANGUAGE_MISMATCH"
    assert detail["selected_language"] == "javascript"
    assert detail["detected_language"] == "python"
def test_corrected_language_allows_analysis(monkeypatch):
    import Backend.main as main_module
    from Backend.schemas import AnalysisResponse
    _clear_rate_limit_state()
    calls = []
    def fake_analyze_code(**kwargs):
        calls.append(kwargs["language"])
        return AnalysisResponse(success=True, summary="Python code analyzed.", root_cause="Sample.")
    monkeypatch.setattr(main_module, "analyze_code", fake_analyze_code)
    response = client.post("/api/analyze", json={"code": "def greet(name):\n    print('hello', name)", "language": "python"})
    assert response.status_code == 200
    assert calls == ["python"]
    assert response.json()["summary"] == "Python code analyzed."
