
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

MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "20000"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "90"))
