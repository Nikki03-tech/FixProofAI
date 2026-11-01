import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "FixProof AI"
APP_VERSION = "1.0.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5173",
)


def _positive_int_env(name: str, default: int) -> int:
    """Read a positive integer environment variable with a safe fallback."""
    try:
        value = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


MAX_CODE_LENGTH = _positive_int_env("MAX_CODE_LENGTH", 20000)
REQUEST_TIMEOUT = _positive_int_env("REQUEST_TIMEOUT", 90)
ANALYZE_RATE_LIMIT_PER_MINUTE = _positive_int_env(
    "ANALYZE_RATE_LIMIT_PER_MINUTE", 5
)
