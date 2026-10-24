from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Backend.config import (
    APP_NAME,
    APP_VERSION,
    FRONTEND_ORIGIN,
    MAX_CODE_LENGTH,
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


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=APP_NAME,
        version=APP_VERSION,
    )


@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    if len(request.code) > MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"Code exceeds the {MAX_CODE_LENGTH}-character limit.",
        )

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
