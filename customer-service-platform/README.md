# Group 8 – AI Customer Service Platform (Alpha MVP)

A small educational MVP with a React chat interface, FastAPI backend, PostgreSQL persistence, and an optional OpenAI-powered response provider.

## Features
- Send customer messages and receive an AI-generated response when an API key is configured.
- Demo fallback response when no OpenAI key is configured (clearly labeled).
- Persist conversations and messages in PostgreSQL.
- Basic input validation and API error handling.
- Health endpoint and automated backend tests.
- GitHub Actions workflow for backend tests.

> This is a classroom MVP, not a production customer-support system. Do not enter real customer personal, payment, or sensitive information.

## Requirements
- Docker Desktop (includes Docker Compose)
- Git
- Node.js 20+ (only needed if running the frontend outside Docker)
- OpenAI API key (optional; API usage may incur separate charges)

## Run with Docker Compose
1. Copy `.env.example` to `.env`.
2. Optionally add your own OpenAI API key to `OPENAI_API_KEY` in `.env`.
3. From this folder, run:

   ```bash
   docker compose up --build
   ```

4. Open the frontend at http://localhost:5173
5. API docs are at http://localhost:8000/docs

To stop: `Ctrl+C`, then `docker compose down`.

To remove the local database volume too (this deletes local demo data):
`docker compose down -v`

## Run backend tests locally
The tests use SQLite in-memory so PostgreSQL is not required for the test command.

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Configuration
- `DATABASE_URL`: PostgreSQL connection string. Docker Compose sets this automatically.
- `OPENAI_API_KEY`: optional. Keep it private; never commit `.env`.
- `OPENAI_MODEL`: model name, default `gpt-4o-mini`.

## API
- `GET /health` – health status
- `POST /api/chat` – accepts `{"message": "..."}` and returns `{"reply": "...", "mode": "openai" | "demo"}`

## Suggested team workflow
- Each person should work on a separate feature branch.
- Open a pull request and request a teammate's review before merging.
- Use meaningful commit messages describing actual changes.
- Record actual tests and review feedback in your submission; do not claim work or reviews that did not happen.
