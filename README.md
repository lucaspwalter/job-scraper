<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Job Scraper mascot" width="200">
</p>

# Job Scraper

Local job monitor with a FastAPI backend, React frontend, and workflows for OpenAI Codex. Built to centralize sources, collect job listings, prevent duplicates, and support evaluation, applications, and interview preparation.

Independent Codex adaptation; neither affiliated with nor maintained by OpenAI. Application workflows are based on Mads Lorentzen's `ai-job-search` project, licensed under MIT.

## How it works

- The backend queries configured sources, normalizes listings, and stores data in PostgreSQL with Docker or SQLite in manual mode.
- The frontend lets users manage sources and view results.
- The scheduler runs periodic searches.
- Email and WhatsApp are optional and remain disabled without credentials.
- `.agents/skills/` contains Codex workflows, including `$setup`, `$scrape`, `$rank`, `$apply`, and `$interview`.

## Running with Docker — recommended

Requirements: Git and Docker Desktop/Engine with Compose.

```bash
git clone https://github.com/lucaspwalter/job-scraper.git
cd job-scraper
docker compose up --build
```

Open:

- Interface: http://localhost:5173
- API: http://localhost:8000
- API documentation: http://localhost:8000/docs

To stop:

```bash
docker compose down
```

## Running manually — Linux/macOS

Requires Python 3.10+ and Node.js 20+.

Terminal 1:

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 seed.py
python3 main.py
```

Terminal 2:

```bash
cd frontend
npm install
npm start
```

## Running manually — Windows PowerShell

Terminal 1:

```powershell
Set-Location backend
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py seed.py
py main.py
```

Terminal 2:

```powershell
Set-Location frontend
npm install
npm start
```

If PowerShell blocks environment activation, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Using with Codex

From the project root:

```bash
codex
```

Then run `$setup`. Generated personal data is ignored by Git. Main commands:

- `$scrape`: searches for jobs.
- `$rank`: ranks results.
- `$apply <URL>`: evaluates a job and prepares an application.
- `$interview`: prepares for an interview.

## Optional configuration

Edit `backend/.env` to enable notifications. `SMTP_*`, `EVOLUTION_*`, and `NOTIFY_*` variables may remain empty.

## Private data

Do not publish `.env`, SQLite databases, personal résumés, generated cover letters, documents, trackers, or search results. `.gitignore` already protects these paths.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT. See `LICENSE`.
