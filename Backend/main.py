from collections.abc import Callable
from threading import Lock
from time import monotonic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Backend.config import ANALYZE_RATE_LIMIT_PER_MINUTE, APP_NAME, APP_VERSION, FRONTEND_ORIGIN
from Backend.schemas import AnalysisRequest, AnalysisResponse, HealthResponse
from Backend.services.ai_service import AIServiceError, analyze_code
from Backend.services.language_detection import detect_language
from Backend.services.report_service import generate_markdown_report
MAX_REQUEST_BODY_BYTES = 1_100_000
app = FastAPI(title=APP_NAME, version=APP_VERSION, description="AI-assisted code debugging API. Submitted code is not executed.")
app.add_middleware(CORSMiddleware, allow_origins=[FRONTEND_ORIGIN], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
class ReportRequest(BaseModel):
    request: AnalysisRequest
    result: AnalysisResponse
_rate_limit_lock = Lock()
_rate_limit_buckets: dict[str, tuple[float, int]] = {}
_RATE_LIMIT_WINDOW_SECONDS = 60
def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"
@app.middleware("http")
async def protect_api(request: Request, call_next: Callable):
    if request.method == "POST" and request.url.path in {"/api/analyze", "/api/report"}:
        length = request.headers.get("content-length")
        if length:
            try:
                if int(length) > MAX_REQUEST_BODY_BYTES:
                    return JSONResponse(status_code=413, content={"detail": "Request body is too large."})
            except ValueError:
                return JSONResponse(status_code=400, content={"detail": "Invalid Content-Length header."})
    if request.method == "POST" and request.url.path == "/api/analyze":
        now = monotonic()
        key = _client_key(request)
        with _rate_limit_lock:
            expired = [item for item, (started, _) in _rate_limit_buckets.items() if now - started >= _RATE_LIMIT_WINDOW_SECONDS]
            for item in expired:
                _rate_limit_buckets.pop(item, None)
            started, count = _rate_limit_buckets.get(key, (now, 0))
            if now - started >= _RATE_LIMIT_WINDOW_SECONDS:
                started, count = now, 0
            if count >= ANALYZE_RATE_LIMIT_PER_MINUTE:
                retry_after = max(1, int(_RATE_LIMIT_WINDOW_SECONDS - (now - started)))
                return JSONResponse(status_code=429, content={"detail": "Analysis rate limit reached. Please try again shortly."}, headers={"Retry-After": str(retry_after)})
            _rate_limit_buckets[key] = (started, count + 1)
    return await call_next(request)
@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", app=APP_NAME, version=APP_VERSION)
@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    detected_language = detect_language(request.code)
    if detected_language is not None and detected_language != request.language:
        raise HTTPException(status_code=409, detail={
            "code": "LANGUAGE_MISMATCH",
            "selected_language": request.language,
            "detected_language": detected_language,
            "message": f"You selected {request.language}, but the code looks like {detected_language}. Switch the language and analyze again.",
        })
    try:
        return analyze_code(code=request.code, language=request.language, explanation_level=request.explanation_level, include_tests=request.include_tests)
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
@app.post("/api/report")
def create_report(body: ReportRequest) -> dict[str, str]:
    return {"report": generate_markdown_report(result=body.result, language=body.request.language, explanation_level=body.request.explanation_level)}
