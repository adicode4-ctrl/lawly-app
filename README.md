# Lawly App

Lawly App is a full-stack legal assistant prototype with a FastAPI backend and a Next.js frontend.

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm

## Quick start

Run this once from the repository root to set up the environment:

```bash
make setup
```

This command will:
- create a Python virtual environment at [.venv](.venv)
- install backend dependencies from [backend/requirements.txt](backend/requirements.txt)
- install frontend dependencies from [frontend/package.json](frontend/package.json)
- create [backend/.env](backend/.env) from [backend/.env.example](backend/.env.example)

If you prefer to do each step manually, use:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
cp -n backend/.env.example backend/.env
```

## Run the app

Open two terminals.

### Terminal 1 — backend

```bash
make backend
```

This starts the FastAPI API on:
- http://127.0.0.1:8000/docs

### Terminal 2 — frontend

```bash
make frontend
```

This starts the Next.js app on:
- http://localhost:3000

## Useful commands

```bash
make setup
make install-backend
make install-frontend
make backend
make frontend
```

## Environment variables

The backend reads these variables from [backend/.env](backend/.env):

- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- OPENROUTER_API_KEY

If these are left empty, the app will still start, but AI features will return an error until a valid key is provided.
