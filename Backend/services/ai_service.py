
import json
import os

import httpx
from pydantic import ValidationError

from Backend.config import REQUEST_TIMEOUT
from Backend.schemas import AnalysisResponse
from Backend.services.prompt_service import build_analysis_prompt


class AIServiceError(Exception):
    """Raised when the AI service cannot produce a valid analysis."""


def analyze_code(
    code: str,
    language: str,
    explanation_level: str = "beginner",
    include_tests: bool = True,
) -> AnalysisResponse:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

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
        "v1beta/models/gemini-2.5-flash:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    body = {
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "You are FixProof AI, an expert code debugging assistant. "
                        "Return only a valid JSON object matching the requested "
                        "schema. Never claim code was executed or tested."
                    )
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
        },
    }

    try:
        response = httpx.post(
            url,
            headers=headers,
            json=body,
            timeout=REQUEST_TIMEOUT,
        )

        if response.is_error:
            raise AIServiceError(
                f"Gemini returned an error (HTTP {response.status_code}). "
                "Please check the API key, model availability, and free-tier quota."
            )

        data = response.json()
        candidates = data.get("candidates", [])

        if not candidates:
            raise AIServiceError(
                "Gemini returned no analysis. Please try again with different code."
            )

        parts = candidates[0].get("content", {}).get("parts", [])
        content = "".join(
            part.get("text", "") for part in parts
            if isinstance(part.get("text"), str)
        )

        if not content.strip():
            raise AIServiceError("Gemini returned an empty response.")

        payload = json.loads(content)
        result = AnalysisResponse.model_validate(payload)

        if not include_tests:
            result.tests = []

        return result

    except AIServiceError:
        raise
    except httpx.TimeoutException as exc:
        raise AIServiceError(
            "Gemini took too long to respond. Please try again."
        ) from exc
    except httpx.RequestError as exc:
        raise AIServiceError(
            "Could not connect to Gemini. Please try again."
        ) from exc
    except (json.JSONDecodeError, ValidationError, KeyError, TypeError, ValueError) as exc:
        raise AIServiceError(
            "Gemini returned an invalid analysis. Please try again."
        ) from exc
