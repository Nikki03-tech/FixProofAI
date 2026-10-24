
import json
import logging
import time

import httpx
from pydantic import ValidationError

from Backend.config import GEMINI_API_KEY, GEMINI_MODEL, REQUEST_TIMEOUT
from Backend.schemas import AnalysisResponse
from Backend.services.prompt_service import build_analysis_prompt

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Raised when the AI service cannot produce a valid analysis."""


def analyze_code(
    code: str,
    language: str,
    explanation_level: str = "beginner",
    include_tests: bool = True,
) -> AnalysisResponse:
    api_key = GEMINI_API_KEY.strip()

    if not api_key:
        raise AIServiceError(
            "Gemini is not configured. Add GEMINI_API_KEY "
            "to the backend environment variables."
        )

    prompt = build_analysis_prompt(
        code=code,
        language=language,
        explanation_level=explanation_level,
        include_tests=include_tests,
    )

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    body = {
        "systemInstruction": {
            "parts": [{
                "text": (
                    "You are FixProof AI, an expert code debugging assistant. "
                    "Return only a valid JSON object matching the requested "
                    "schema. Never claim code was executed or tested."
                )
            }]
        },
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
        },
    }

    started = time.monotonic()

    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            response = client.post(url, headers=headers, json=body)

        elapsed = round(time.monotonic() - started, 2)
        logger.info(
            "Gemini model=%s HTTP status=%s elapsed_seconds=%s",
            GEMINI_MODEL, response.status_code, elapsed,
        )

        if response.is_error:
            try:
                error_data = response.json().get("error", {})
                error_code = error_data.get("status", "UNKNOWN")
            except (ValueError, AttributeError):
                error_code = "UNKNOWN"

            logger.error(
                "Gemini API error: http=%s code=%s",
                response.status_code, error_code,
            )
            raise AIServiceError(
                f"Gemini API returned HTTP {response.status_code} "
                f"({error_code}). Check the backend logs for details."
            )

        data = response.json()
        candidates = data.get("candidates", [])

        if not candidates:
            raise AIServiceError(
                "Gemini returned no analysis. Please try again."
            )

        parts = candidates[0].get("content", {}).get("parts", [])
        content = "".join(
            part.get("text", "")
            for part in parts
            if isinstance(part.get("text"), str)
        )

        if not content.strip():
            raise AIServiceError("Gemini returned an empty response.")

        payload = json.loads(content)
        result = AnalysisResponse.model_validate(payload)

        if not include_tests:
            result.tests = []

        logger.info("Gemini analysis succeeded; elapsed_seconds=%s", elapsed)
        return result

    except AIServiceError:
        raise
    except httpx.TimeoutException as exc:
        elapsed = round(time.monotonic() - started, 2)
        logger.error("Gemini request timed out after %s seconds", elapsed)
        raise AIServiceError(
            f"Gemini timed out after {elapsed} seconds. "
            "Please try again with a smaller code sample."
        ) from exc
    except httpx.RequestError as exc:
        logger.error("Gemini connection error: %s", type(exc).__name__)
        raise AIServiceError(
            "Could not connect to Gemini. Please try again."
        ) from exc
    except (
        json.JSONDecodeError,
        ValidationError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        logger.error("Invalid Gemini response: %s", type(exc).__name__)
        raise AIServiceError(
            "Gemini returned an invalid analysis. Please try again."
        ) from exc
