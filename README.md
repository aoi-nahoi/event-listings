# Event Listings

Event Listings is a Django + HTMX web application for the Web Engineering final project. Visitors can browse, search, and filter local events. Registered users can create, edit, delete, and bookmark events.

## Features

- Event list with title, date, location, category, and organizer profile name
- Async search and filters with HTMX (`hx-push-url`, live results, accessible status updates)
- Account registration, login, and logout
- Authenticated event create / edit / delete (author or staff)
- Authenticated bookmark create with partial page updates
- SQLite database for course demonstration
- WhiteNoise + Gunicorn + `render.yaml` for Render deployment
- OpenSpec, AGENTS.md, Cursor skills, and GitHub templates as project-management evidence

## Development Environment

- Python 3.11+
- uv
- Git and GitHub
- Django 5
- Ruff / Pylint config
- pytest

## Setup

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Demo accounts after seeding: `sota` / `mika` / `ren` with password `demo-pass-123`.

## Useful Commands

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
python3 -m uv run python manage.py collectstatic --noinput
```

## Routes

| URL | Name | Purpose |
| --- | --- | --- |
| `/` | `events:event_list` | Browse, search, and filter events |
| `/accounts/register/` | `accounts:register` | Create an account |
| `/accounts/login/` | `accounts:login` | Log in |
| `/accounts/logout/` | `accounts:logout` | Log out |
| `/events/new/` | `events:event_create` | Create a new event (login required) |
| `/events/<id>/` | `events:event_detail` | Event details and bookmarks |
| `/events/<id>/edit/` | `events:event_edit` | Edit event (author/staff) |
| `/events/<id>/delete/` | `events:event_delete` | Delete event (author/staff) |
| `/events/<id>/bookmarks/` | `events:bookmark_create` | Bookmark action (login required) |
| `/partials/events/` | `events:event_list_partial` | HTMX event list partial |
| `/seed-demo/` | `events:seed_demo` | Create demo categories, users, and events |
| `/healthz/` | health check | Deployment health check |

## Data Model

- Django `User`: account used for authorship and login
- `Category`: Lecture, Concert, Workshop, Sports, Meetup, and more
- `OrganizerProfile`: display name and contact email for organizers
- `Event`: title, description, date, location, category, author, status
- `Bookmark`: attendee name and note linked to an event

## Architecture Notes

- Templates own the HTML layout
- `events_app/services.py` owns writes
- `events_app/selectors.py` owns reusable reads
- Views stay thin and handle request/response only

## Deployment

### Render (recommended)

Render can deploy this project as a Python web service using `render.yaml`.

Build command:

```bash
pip install -U pip && pip install --force-reinstall . && PYTHONPATH=src python manage.py collectstatic --noinput
```

Start command:

```bash
PYTHONPATH=src python manage.py migrate && PYTHONPATH=src gunicorn events_site.wsgi:application --bind 0.0.0.0:$PORT
```

Environment variables:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` (required in production)
- `DJANGO_ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1`

After deploy, verify `https://<your-service>.onrender.com/healthz/`.

### Docker (optional local/prod-like run)

```bash
docker build -t event-listings .
docker run --rm -p 8000:8000 \
  -e DJANGO_DEBUG=0 \
  -e DJANGO_SECRET_KEY=change-me \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  event-listings
```

## Documentation

- Rubric mapping: `docs/rubric-alignment.md`
- Review evidence: `docs/project-review.md`
- Demo script: `docs/final-demo-notes.md`
- Specs: `openspec/specs/`
- Contributing / review flow: `CONTRIBUTING.md`
