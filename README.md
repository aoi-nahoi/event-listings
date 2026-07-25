# Event Listings

Event Listings is a Django + HTMX web application for the Web Engineering final project. It follows the Exercise 1 and Exercise 2 proposal by allowing users to browse local events, search by title, filter by category/date, open detail pages, create events, and bookmark events.

## Features

- Event list with title, date, location, category, and organizer.
- Search and filters powered by Django querysets.
- Event creation form backed by Django forms and models.
- Detail page with an HTMX bookmark form.
- SQLite database for course demonstration.
- WhiteNoise and Gunicorn configuration for Render deployment.

## Setup

```bash
python3 -m uv sync
python3 -m uv run python manage.py migrate
python3 -m uv run python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

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
| `/events/new/` | `events:event_create` | Create a new event |
| `/events/<id>/` | `events:event_detail` | View event details and bookmarks |
| `/events/<id>/bookmarks/` | `events:bookmark_create` | Create bookmark action |
| `/partials/events/` | `events:event_list_partial` | HTMX event list partial |
| `/seed-demo/` | `events:seed_demo` | Create demo categories, users, and events |
| `/healthz/` | health check | Deployment health check |

## Data Model

- Django `User`: event organizer account data.
- `Category`: event category such as Lecture, Concert, Workshop, Sports, or Meetup.
- `OrganizerProfile`: optional organizer display profile.
- `Event`: title, description, date, location, category, author, and status.
- `Bookmark`: visitor name and note linked to an event.

## Deployment

Render can deploy this project as a Python web service using `render.yaml`.

Build command:

```bash
pip install -U pip && pip install --force-reinstall . && PYTHONPATH=src python manage.py collectstatic --noinput
```

Start command:

```bash
PYTHONPATH=src python manage.py migrate && PYTHONPATH=src gunicorn events_site.wsgi:application --bind 0.0.0.0:$PORT
```

Set `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`.
