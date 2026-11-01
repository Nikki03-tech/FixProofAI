# FixProof AI — Project Overview

## Current application

FixProof AI is an AI-assisted debugging application for Python and JavaScript. Its AI provider is the Google Gemini API.

The repository includes two Gemini-powered interfaces:
- React + TypeScript frontend with a FastAPI backend (the current Render deployment).
- An alternative Streamlit interface in `app.py`.

Both integrations use the `GEMINI_API_KEY` environment variable and configurable `GEMINI_MODEL`. The default model is `gemini-3.5-flash-lite`.

## Problem

Developers, especially beginners, often struggle to understand error messages and identify reliable fixes.

## Solution

FixProof AI analyzes submitted code and error descriptions as text, then provides explanations, likely root causes, proposed fixes, and testing guidance. The FastAPI service does not execute submitted code.

## Technology stack

- React
- TypeScript
- Vite
- Python
- FastAPI
- Streamlit
- Pydantic
- HTTPX
- Google Gemini API
- Render

## Core features

1. Beginner-friendly error explanations.
2. Likely root-cause analysis.
3. Suggested code improvements.
4. Test-case generation and testing guidance.
5. Python and JavaScript support.
6. Adjustable explanation depth.
7. Markdown debugging report generation.

## Responsible AI

AI suggestions may be incorrect. Review proposed fixes and test them safely before using them in production. Never submit passwords, API keys, access tokens, or private data in code samples.
