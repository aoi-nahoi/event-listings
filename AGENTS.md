# Project Agent Notes

Event Listings is a Django + HTMX web application for the Web Engineering final project.

## Rules
- Keep UI structure in Django templates, not in Python view strings.
- Put workflow logic in `events_app/services.py`.
- Put reusable query logic in `events_app/selectors.py`.
- Keep tests updated when models, views, or forms change.
- Use English for user-facing application text and project documentation.

## Verification
- `python3 -m uv run ruff check .`
- `python3 -m uv run python manage.py check`
- `python3 -m uv run pytest`
