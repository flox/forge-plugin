# Sample Eval App

A minimal FastAPI application used as the test project for
Forge plugin evaluation runs.

## What this is

This project is a fixture — a realistic-looking Python web
service that gives the Forge plugin something meaningful to
analyze during eval scenarios.

## Running

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

- `GET /health` — Health check
- `GET /items/{item_id}` — Placeholder items endpoint

## Purpose

The eval harness (`eval/`) uses this project to test that
Forge commands work correctly in a real project context. The
app is simple enough to set up quickly but realistic enough
to exercise Forge's project analysis capabilities.
