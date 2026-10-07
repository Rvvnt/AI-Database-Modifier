# ForgePilot v2 — HNX26PSI09

AI Software Engineering Agent for the challenge flow:
real repository -> understand -> minimal change -> regression tests -> proof.

## Run in VS Code / Windows
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Architecture
Repository Loader -> Codebase Mapper -> Context Retriever -> Agent Planner -> Patch Adapter -> Test Runner -> Regression Gate -> Diff/Report

The LLM provider is isolated in `app/llm.py`. Connect the team's approved model there.
For production, run untrusted repositories inside an isolated container/VM.
