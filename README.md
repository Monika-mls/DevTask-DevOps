# DevTask: A Task Management Application with Automated CI

A simple DevOps course-based project using Flask, SQLite, GitHub, GitHub Actions, Docker, and PyTest.

## Features
- Add tasks
- View tasks and counts
- Mark tasks complete/incomplete
- Delete tasks
- Health endpoint at `/health`

## Windows setup (PowerShell in VS Code)

Install Python 3.12+ and ensure `py` works:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. If activation is blocked, skip activation and use `.\.venv\Scripts\python.exe` instead of `python`.

## Tests

```powershell
python -m pytest -q
```

## Docker

Install Docker Desktop and start it. Then run:

```powershell
docker build -t devtask .
docker run --rm -p 5000:5000 -v devtask-data:/data devtask
```

Open http://localhost:5000. Stop any `python app.py` process first or port 5000 will be occupied.

## GitHub Actions

Create a GitHub repository, push all files including `.github/workflows/ci.yml`, and open the Actions tab. Each push and pull request runs the tests and builds the Docker image. The workflow does NOT automatically deploy the application to a server; Docker deployment is demonstrated locally.

## Architecture

Browser -> Flask routes -> SQLite database

Git push/PR -> GitHub Actions -> install dependencies -> PyTest -> Docker image build

## Notes

This is a local educational demo without user accounts, CSRF protection or production database hardening. Do not expose it to the public internet as-is.
