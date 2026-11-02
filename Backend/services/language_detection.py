import re

from Backend.schemas import SupportedLanguage


PYTHON_PATTERNS = [
    (r"\bdef\s+\w+\s*\([^)]*\)\s*:", 4),
    (r"^\s*(?:if|elif|else|for|while|try|except|with|class)\b.*:\s*$", 2),
    (r"\b(?:None|True|False|self|elif|lambda|pass|yield)\b", 2),
    (r"\bprint\s*\(", 2),
    (r"\b(?:from\s+\w+\s+import|import\s+\w+)\b", 1),
    (r"^\s{4,}\S", 1),
]

JAVASCRIPT_PATTERNS = [
    (r"\b(?:const|let|var)\s+\w+", 2),
    (r"\bconsole\s*\.\s*(?:log|error|warn)\s*\(", 3),
    (r"=>", 2),
    (r"\bfunction\s+\w*\s*\(", 4),
    (r"\b(?:undefined|null|true|false|this|export)\b", 1),
    (r";\s*(?:$|//)", 1),
]


def detect_language(code: str) -> SupportedLanguage | None:
    """Infer Python or JavaScript only when several clear signals agree."""
    python_score = sum(
        points * len(re.findall(pattern, code, flags=re.MULTILINE))
        for pattern, points in PYTHON_PATTERNS
    )
    javascript_score = sum(
        points * len(re.findall(pattern, code, flags=re.MULTILINE))
        for pattern, points in JAVASCRIPT_PATTERNS
    )

    if python_score >= 2 and python_score >= javascript_score + 2:
        return "python"
    if javascript_score >= 2 and javascript_score >= python_score + 2:
        return "javascript"
    return None
