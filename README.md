# FixProof AI 🔧

**An AI-assisted debugging tool for Python and JavaScript, powered by Gemini.**

FixProof AI helps developers understand likely bugs, investigate root causes, review suggested fixes, and generate test suggestions. Submitted code is analyzed as text and is **not executed** by the service.

## Current application

The deployed application uses a React + TypeScript frontend, a FastAPI backend, and the Gemini API.

### Features

- Explain likely errors and root causes
- Suggest focused code improvements
- Generate suggested tests and verification steps
- Choose beginner, intermediate, or advanced explanations
- Download a Markdown debugging report
- Keep the Gemini API key on the backend

### Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI, Pydantic |
| AI provider | Google Gemini API |
| HTTP client | HTTPX |
| Deployment | Render |

The default model is `gemini-3.5-flash-lite`. You can override it with the `GEMINI_MODEL` environment variable.

## Run locally

### 1. Backend

From the repository root:

```bash
python -m venv .venv
```

Activate the virtual environment, then install the backend dependencies:

```bash
pip install -r Backend/requirements.txt
```

Create `Backend/.env` from `Backend/.env.example` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
FRONTEND_ORIGIN=http://localhost:5173
MAX_CODE_LENGTH=20000
REQUEST_TIMEOUT=90
```

Start the API from the repository root:

```bash
uvicorn Backend.main:app --reload --host 0.0.0.0 --port 8000
```

The health endpoint is available at `http://localhost:8000/health`. It confirms that the API process is responding; it does not verify the Gemini key or call the Gemini API.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env` with:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start Vite:

```bash
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`).

## Render deployment

The root-level `render.yaml` defines two services:

1. **fixproof-ai-api** — installs `Backend/requirements.txt`, starts `Backend.main:app` with Uvicorn, and uses `/health` as its process health check.
2. **fixproof-ai-frontend** — builds the Vite app from the `frontend` directory and publishes `frontend/dist`.

Before the backend can perform AI analysis, add `GEMINI_API_KEY` as a secret environment variable for the **fixproof-ai-api** service in Render. The Blueprint intentionally uses `sync: false` so the secret value is not stored in Git.

The frontend's `VITE_API_BASE_URL` must point to the public URL of the backend service. The backend's `FRONTEND_ORIGIN` must exactly match the public origin of the frontend service (scheme and hostname, without a trailing slash). When either service URL changes, update the corresponding variable and redeploy the affected service.

## Tests

Install backend dependencies, then run from the repository root:

```bash
pytest Backend/tests
```

The tests do not require a live Gemini API key unless an integration test is added in the future.

## API endpoints

- `GET /health` — process health
- `POST /api/analyze` — analyze submitted code using Gemini
- `POST /api/report` — create a downloadable Markdown report

## Privacy and responsible use

- The backend does not execute submitted code.
- Never submit passwords, API keys, access tokens, private customer data, or other secrets in a code sample.
- AI output is a suggestion, not proof that a fix is correct. Review proposed changes and run tests in a safe environment before using them.
- Keep `GEMINI_API_KEY` in Render's backend environment or a local ignored `.env` file. Never place it in a `VITE_*` variable or commit it to GitHub.

## Legacy prototype note

The repository also retains the earlier root-level Streamlit prototype (`app.py`) and its root `requirements.txt`. Those files are not used by the current two-service Render deployment. Use the `Backend/` and `frontend/` folders for the current Gemini-powered application.

---

Built for the BharatCode Build League.
