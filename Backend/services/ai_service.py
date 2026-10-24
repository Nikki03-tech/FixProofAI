import json

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI
from pydantic import ValidationError

from Backend.config import (
    BHARATCODE_API_KEY,
    BHARATCODE_BASE_URL,
    BHARATCODE_MODEL,
    REQUEST_TIMEOUT,
)
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
    if not BHARATCODE_API_KEY:
        raise AIServiceError(
            "The AI service is not configured. Add BHARATCODE_API_KEY "
            "to the backend environment variables."
        )

    client = OpenAI(
        api_key=BHARATCODE_API_KEY,
        base_url=BHARATCODE_BASE_URL,
        timeout=REQUEST_TIMEOUT,
        max_retries=1,
    )

    prompt = build_analysis_prompt(
        code=code,
        language=language,
        explanation_level=explanation_level,
        include_tests=include_tests,
    )

    try:
        completion = client.chat.completions.create(
            model=BHARATCODE_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FixProof AI. Return only a valid JSON object "
                        "matching the requested schema. Never claim code was run."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        content = completion.choices[0].message.content
        if not content:
            raise AIServiceError("The AI service returned an empty response.")

        payload = json.loads(content)
        result = AnalysisResponse.model_validate(payload)

        if not include_tests:
            result.tests = []

        return result

    except (APIConnectionError, APITimeoutError) as exc:
        raise AIServiceError(
            "Could not connect to the AI service. Please try again."
        ) from exc
    except APIStatusError as exc:
        raise AIServiceError(
            f"The AI service returned an error (HTTP {exc.status_code})."
        ) from exc
    except (json.JSONDecodeError, ValidationError, IndexError, AttributeError) as exc:
        raise AIServiceError(
            "The AI service returned an invalid analysis. Please try again."
        ) from exc

