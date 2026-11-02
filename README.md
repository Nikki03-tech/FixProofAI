# FixProof AI

**AI-assisted code debugging for Python and JavaScript, powered by Google Gemini.**

FixProof AI reviews source code as text, explains likely issues and root causes, proposes fixes, and creates suggested tests. **Submitted code is not executed.** AI findings are estimates and must be reviewed by a developer.

## Live application

- **Main application:** https://fixproofai.onrender.com/
- **Source code:** https://github.com/Nikki03-tech/FixProofAI

The main public demo URL above is the one supplied by the project owner. A separate public API URL has not yet been confirmed, so do not use an assumed API hostname as a demo link. The FastAPI service exposes `/health` when deployed; confirm its actual Render URL in the Render dashboard.

## Features

- Python and JavaScript source-code analysis
- Beginner, intermediate, and advanced explanations
- Potential issue list and likely root cause
- Severity classification and AI confidence estimate
- Suggested code fixes and test cases
- Actionable verification checklist
- Downloadable Markdown report
- API health indicator in the React frontend
- Request validation, request-size guard, and per-instance analysis rate limiting

## Architecture

```mermaid
flowchart LR
  U[Developer] --> F[React + TypeScript UI]
  F -->|JSON request| A[FastAPI API]
  A --> V[Pydantic validation]
  V --> S[Gemini service]
  S --> G[Google Gemini API]
  G --> S
  S --> R[Structured analysis]
  R --> F
  F --> D[Markdown report download]
```

### Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite |
| Backend | Python, FastAPI, Pydantic |
| AI | Google Gemini API |
| HTTP client | HTTPX |
| Tests | Pytest, FastAPI TestClient, GitHub Actions |
| Hosting | Render |

## Local setup

### Backend

From the repository root:

```bash
python -m venv .venv
# Activate the virtual environment
pip install -r Backend/requirements.txt
```

Create `Backend/.env` using `Backend/.env.example` as a reference:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
FRONTEND_ORIGIN=http://localhost:5173
MAX_CODE_LENGTH=20000
REQUEST_TIMEOUT=90
ANALYZE_RATE_LIMIT_PER_MINUTE=5
```

Run the API from the repository root:

```bash
uvicorn Backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env` and set `VITE_API_BASE_URL` to the actual backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Open the local Vite URL, normally `http://localhost:5173`.

## Tests and build

Run backend tests from the repository root:

```bash
python -m pytest Backend/tests -q
```

Build the frontend:

```bash
cd frontend
npm install
npm run build
```

GitHub Actions runs backend tests and the frontend production build on pushes and pull requests to `main`.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API process health |
| POST | `/api/analyze` | Gemini-powered source analysis |
| POST | `/api/report` | Generate Markdown report |

Example analysis request:

```json
{
  "code": "def average(numbers): return sum(numbers) / len(number)",
  "language": "python",
  "explanation_level": "beginner",
  "include_tests": true
}
```

## Deployment on Render

The root `render.yaml` provides a two-service Blueprint configuration for a React static frontend and FastAPI backend. The project owner's current public demo link is `https://fixproofai.onrender.com/`; confirm the API service's actual hostname independently in Render before using it in `VITE_API_BASE_URL`.

Set `GEMINI_API_KEY` as a secret in the backend Render environment. Do not commit it or place it in a frontend `VITE_*` variable. The backend's `FRONTEND_ORIGIN` must match the deployed frontend's exact origin.

## Security and limitations

- The backend does not execute submitted source code.
- Analysis requests have a configurable code-character limit.
- API analysis requests have a per-process fixed-window rate limit (default: 5 per minute).
- Request bodies with a declared Content-Length above the configured guard are rejected.
- The in-memory limiter is intended as a basic single-instance safeguard. Multiple instances require a shared rate-limit store such as Redis.
- A Content-Length guard is not a substitute for edge/proxy request-size enforcement.
- Never submit API keys, passwords, tokens, or private customer data.
- Gemini output, severity, and confidence are AI-generated estimates, not guarantees. Review suggestions and run tests in a safe environment before applying changes.

## Alternative interface

A Streamlit interface is also available from the root-level `app.py`. Configure the same Gemini environment variables, install root `requirements.txt`, and run:

```bash
streamlit run app.py
```
