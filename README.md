
# FixProof AI 🔧

**An AI-powered debugging assistant built with the BharatCode API.**

FixProof AI helps developers understand errors, investigate likely root causes, review suggested code fixes, and generate test cases for Python and JavaScript code.

## ✨ Features

- Explain errors in beginner-friendly language
- Identify likely root causes
- Suggest corrected code
- Generate test cases and a testing plan
- Support Python and JavaScript
- Choose the depth of explanation
- Keep API credentials outside source code

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenAI Python SDK
- BharatCode API (`qwen-3.8-27b`)

## 🚀 Run Locally

1. Install Python 3.10 or newer.
2. Clone this repository.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your BharatCode API key in an environment variable named `BHARATCODE_API_KEY`.

5. Start the application:

   ```bash
   streamlit run app.py
   ```

## 🔐 API Key Security

Never commit your real API key to GitHub. Configure it using an environment variable locally or Streamlit secrets when deploying.

## ⚠️ Responsible Use

FixProof AI provides AI-generated debugging suggestions. Review the proposed changes and run tests in a safe environment before using them in production. AI-generated suggestions may be incorrect.

## 🎯 Project Goal

Make debugging easier for students and developers by turning confusing error messages into understandable explanations and actionable testing guidance.

---

Built for the BharatCode Build League.
