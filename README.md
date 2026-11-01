# FixProof AI 🔧

**An AI-assisted debugging tool for Python and JavaScript, powered by Google Gemini.**

FixProof AI helps developers understand likely bugs, investigate root causes, review suggested fixes, and generate test suggestions. Submitted code is analyzed as text and is **not executed** by the service.

## Application interfaces

The project has two Gemini-powered interfaces:

- **React + FastAPI application** — the current Render deployment, with a React/TypeScript frontend and a Python FastAPI backend.
- **Streamlit application** — an alternative interface available from the root-level `app.py`, also connected directly to the Gemini API.

Both interfaces use the same `GEMINI_API_KEY` and `GEMINI_MODEL` environment-variable names. The key must remain server-side and must never be exposed through a frontend `VITE_*` variable.

## Features

- Explain likely errors and root causes
- Suggest focused code improvements
- Generate suggested tests and verification steps
- Choose the depth of explanation
- Download a Markdown debugging report
- Support Python and JavaScript

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| API backend | Python, FastAPI, Pydantic |
| Alternative interface | Streamlit |
| AI provider | Google Gemini API |
| HTTP client | HTTPX |
| Deployment | Render |

The default Gemini model is `gemini-3.5-flash-lite`. Set `GEMINI_MODEL` to use another model available to your Gemini API key.

## Configure Gemini

Create a Gemini API key in Google AI Studio, then set these environment variables for the backend:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit the real key to GitHub. For local development, use an ignored `.env` file or your platform's secret manager. For the Streamlit interface, you can also configure `GEMINI_API_KEY` in Streamlit secrets.

## Run the React + FastAPI application locally

### 1. Backend

From the repository root, create and activate a Python virtual environment, then install backend dependencies:

```bash
python -m venv .venv
pip install -r Backend/requirements.txt
```

Create `Backend/.env` from `Backend/.env.example` and set your Gemini key. Keep the local frontend origin:

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

The health endpoint is `http://localhost:8000/health`. It confirms that the API process is responding; it does not verify the Gemini key or call Gemini.

### 2. React frontend

In a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start Vite:

```bash
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`).

## Run the Streamlit interface locally

From the repository root:

```bash
pip install -r requirements.txt
```

Set `GEMINI_API_KEY` in your environment or Streamlit secrets, then run:

```bash
streamlit run app.py
```

The Streamlit interface sends requests directly to the Gemini API. Do not put the Gemini key in frontend code or commit it to the repository.

## Render deployment

The root-level `render.yaml` defines the current two-service deployment:

1. **fixproof-ai-api** — installs `Backend/requirements.txt`, starts `Backend.main:app` with Uvicorn, and uses `/health` as its process health check.
2. **fixproof-ai-frontend** — builds the Vite app from the `frontend` directory and publishes `frontend/dist`.

In the Render dashboard, make sure the **fixproof-ai-api** service has a secret environment variable named `GEMINI_API_KEY`. The Blueprint uses `sync: false` so the secret value is not stored in Git.

The frontend's `VITE_API_BASE_URL` must point to the public backend URL. The backend's `FRONTEND_ORIGIN` must exactly match the public frontend origin (scheme and hostname, without a trailing slash). If either service URL changes, update the corresponding variable and redeploy the affected service.

## Tests

Install backend dependencies and run from the repository root:

```bash
pytest Backend/tests
```

The unit tests do not require a live Gemini API key.

## API endpoints

- `GET /health` — API process health
- `POST /api/analyze` — analyze submitted code using Gemini
- `POST /api/report` — create a downloadable Markdown report

## Privacy and responsible use

- The FastAPI backend does not execute submitted code.
- Never submit passwords, API keys, access tokens, private customer data, or other secrets in a code sample.
- AI output is a suggestion, not proof that a fix is correct. Review proposed changes and run tests in a safe environment before using them.
- Keep `GEMINI_API_KEY` in backend environment variables or local ignored secrets. Never place it in a `VITE_*` variable or commit it to GitHub.
