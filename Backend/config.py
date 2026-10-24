import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "FixProof AI"
APP_VERSION = "1.0.0"

BHARATCODE_API_KEY = os.getenv("BHARATCODE_API_KEY", "")
BHARATCODE_BASE_URL = os.getenv(
    "BHARATCODE_BASE_URL",
    "https://bharatcode.ai/api/model/v1",
)
BHARATCODE_MODEL = os.getenv(
    "BHARATCODE_MODEL",
    "qwen-3.8-27b",
)

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5173",
)

MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "20000"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
