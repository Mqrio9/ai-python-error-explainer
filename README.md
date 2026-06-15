# AI Python Error Explainer

A small Python Flask AI app. Users paste a Python error or broken code, and the app explains it in simple beginner English.

## Features

- Working public web page
- AI feature using OpenAI API
- Empty-input bug handled
- `/health` route returns 200 OK for grader checks

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your API key:

### Windows PowerShell

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

Close and reopen the terminal after using `setx`.

### macOS/Linux

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Deploy

You can deploy this on Render, Railway, or another Python hosting service.

Set environment variable:

```text
OPENAI_API_KEY = your_api_key_here
```

Optional:

```text
OPENAI_MODEL = gpt-5.5-mini
```

Start command:

```bash
gunicorn app:app
```

## Submission checklist

- Live URL:
- 3 user feedback screenshots/quotes:
- QA bug handled:

### QA bug example

Bug: Empty input made the app send a useless request.

1. Found issue: User clicked Explain with empty box.
2. Reproduced: I cleared the box and clicked Explain.
3. Cause: The app did not validate input first.
4. Fixed it: Added a check that tells the user to paste Python code/error first.
5. Retested: Empty input now shows a clear warning and does not call the AI.
