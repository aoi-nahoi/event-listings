# AGENTS.md

## Project Scope

Event Listings is a Django + HTMX web application for the Web Engineering final project. It allows users to browse, search, filter, create, and bookmark local events.

Main implementation:

- `events_app` — event management, filters, templates, HTMX partials, and bookmarks
- `events_site` — Django project settings and root URL configuration
- `openspec/` — project context and agentic setup evidence from the repository

## Important Project Conventions

- Keep UI structure in Django templates, not in Python view strings.
- Put business logic in `events_app/services.py`, not in views.
- Put reusable queries in `events_app/selectors.py`.
- Keep views thin and focused on request/response handling.
- Keep tests updated when models, views, forms, or services change.
- Use English for user-facing application text and project documentation.
- Do not edit old migrations after they are committed.
- Prefer small, targeted changes.

## Commands

- Run server: `python3 -m uv run python manage.py runserver`
- Create migrations: `python3 -m uv run python manage.py makemigrations`
- Apply migrations: `python3 -m uv run python manage.py migrate`
- Lint: `python3 -m uv run ruff check .`
- Django check: `python3 -m uv run python manage.py check`
- Tests: `python3 -m uv run pytest`

## Documentation Use

- Use `docs/` for final project review and demo evidence.
- Use `openspec/specs/*` as supporting repository documentation when reviewing project intent.
