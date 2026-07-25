# Final Demo Notes

## Goal

Show that Event Listings is a working Django + HTMX web application with database-backed events, user input, responsive templates, tests, and deployment documentation.

## Demo Flow

1. Open the deployed application or local server.
2. Click "Seed demo data" if the event list is empty.
3. Browse event cards with date, category, organizer, and location.
4. Search for a keyword such as `lecture`.
5. Filter by category and date range.
6. Open an event detail page.
7. Add a bookmark and show that the list updates without a full page reload.
8. Create a new event from `/events/new/`.
9. Show the Django models, services, selectors, templates, and tests.
10. Show deployment commands and the health check route.

## Commands To Mention

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```
