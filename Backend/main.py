from collections.abc import Callable
from threading import Lock
from time import monotonic

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Backend.config import (
    ANALYZE_RATE_LIMIT_PER_MINUTE,
    APP_NAME,
    APP_VERSION,
    FRONTEND_ORIGIN,
)
from Backend.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    HealthResponse,
)
from Backend.services.ai_service import AIServiceError, analyze_code
from Backend.services.report_service import generate_markdown_report


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-assisted code debugging API. Submitted code is not executed.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ReportRequest(BaseModel):
    request: AnalysisRequest
    result: AnalysisResponse


# Lightweight per-process fixed-window limiter. This protects a single
# Render instance; use a shared store such as Redis if running multiple
# instances or needing limits that survive restarts.
_rate_limit_lock = Lock()
_rate_limit_buckets: dict[str, tuple[float, int]] = {}
_RATE_LIMIT_WINDOW_SECONDS = 60


def _client_key(request: Request) -> str:
    # Uvicorn's proxy-header handling supplies the client address when
    # running behind Render's trusted proxy.
    return request.client.host if request.client else "unknown"


@app.middleware("http")
async def limit_analysis_requests(
    request: Request,
    call_next: Callable,
):
    if request.method == "POST" and request.url.path == "/api/analyze":
        now = monotonic()
        client_key = _client_key(request)

        with _rate_limit_lock:
            # Remove expired buckets so the dictionary does not grow forever.
            expired = [
                key for key, (started, _) in _rate_limit_buckets.items()
                if now - started >= _RATE_LIMIT_WINDOW_SECONDS
            ]
            for key in expired:
                _rate_limit_buckets.pop(key, None)

            started, count = _rate_limit_buckets.get(client_key, (now, 0))
            if now - started >= _RATE_LIMIT_WINDOW_SECONDS:
                started, count = now, 0

            if count >= ANALYZE_RATE_LIMIT_PER_MINUTE:
                retry_after = max(
                    1, int(_RATE_LIMIT_WINDOW_SECONDS - (now - started))
                )
                return HTTPExceptionResponse(retry_after)

            _rate_limit_buckets[client_key] = (started, count + 1)

    return await call_next(request)


async def HTTPExceptionResponse(retry_after: int):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=429,
        content={"detail": "Analysis rate limit reached. Please try again shortly."},
        headers={"Retry-After": str(retry_after)},
    )


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=APP_NAME,
        version=APP_VERSION,
    )


@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    try:
        return analyze_code(
            code=request.code,
            language=request.language,
            explanation_level=request.explanation_level,
            include_tests=request.include_tests,
        )
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/report")
def create_report(body: ReportRequest) -> dict[str, str]:
    report = generate_markdown_report(
        result=body.result,
        language=body.request.language,
        explanation_level=body.request.explanation_level,
    )
    return {"report": report}
