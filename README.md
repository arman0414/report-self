# ReportSelf

Turn any topic into a citation-backed research report with a council of planning, research, critique, and writing agents. Works locally with no API keys — clone, run one command, open the UI.

## Requirements

- Python 3.11+ (3.10+ usually works)
- Or Docker, if you prefer containers

## Run locally (after GitHub download)

### Option 1 — one command (recommended)

```bash
git clone https://github.com/arman0414/report-self.git
cd report-self
chmod +x start.sh
./start.sh
```

Then open:

- **App UI:** http://127.0.0.1:8013/
- **API docs:** http://127.0.0.1:8013/docs
- **Health:** http://127.0.0.1:8013/health

`start.sh` creates a virtualenv, installs dependencies, and starts the server with auto-reload.

Custom port or host:

```bash
PORT=8080 HOST=0.0.0.0 ./start.sh
```

Use `HOST=0.0.0.0` only on a trusted network if you want other machines on your LAN to reach the app.

### Option 2 — manual setup

```bash
git clone https://github.com/arman0414/report-self.git
cd report-self
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8013
```

### Option 3 — Docker

```bash
git clone https://github.com/arman0414/report-self.git
cd report-self
docker compose up --build
```

Same URLs as above (`8013`).

## Try it

1. Start the server (any option above).
2. Open http://127.0.0.1:8013/
3. Click **Run research agents** (or **Use example** first).
4. View claims on the pinboard and the generated brief on the right.

CLI demo (no browser):

```bash
source .venv/bin/activate
python scripts/run_demo.py
```

## Tests

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## Highlights

- Planner, researcher, critic, and writer agents
- Async orchestration with clear task boundaries
- Source-grounded claims with confidence scoring
- Contradiction and weak-evidence checks
- Markdown report generation endpoint
- Local corpus so the project works without API keys

## Architecture

```text
app/
  agents/        planner, researcher, critic, writer
  api/           research endpoints
  corpus/        local source search
  schemas/       typed workflow contracts
  services/      orchestration and report lifecycle
  static/        ReportSelf web UI
```

## API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/research` | Run the agent pipeline and create a report |
| `GET` | `/api/reports/{id}` | Fetch a report by id |
| `GET` | `/api/reports/{id}/markdown` | Fetch report markdown only |

Topics work best when they relate to AI, RAG, reliability, security, or event streaming (the bundled local corpus). Plug in real search or LLM providers later without changing the orchestration contract.
