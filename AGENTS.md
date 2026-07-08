# AGENTS.md

## Project scope

This is a Django app for managing local event listings.

Main apps:

- `events` — event management
- `accounts` — user authentication
- `api` — REST API endpoints

## Important project conventions

- Put business logic in `services.py`, not in views.
- Put reusable queries in `selectors.py`.
- Keep views thin.

## Commands

- Run server: `python manage.py runserver`
- Run tests: `pytest`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Constraints

- Do not edit old migrations.
- Prefer small, targeted changes.
- Add tests for new features.

## Documentation use

- Use `openspec/specs/*` as the canonical documentation.