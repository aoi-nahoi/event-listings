# Final Demo Notes

## Goal

Show that Event Listings is a working Django + HTMX application with authentication, database-backed events, responsive templates, tests, specs, and clear deployment instructions.

## Demo Flow

1. Open the deployed application or local server (`uv run python manage.py runserver`).
2. Click **Seed demo data** if the list is empty.
3. Point out the modern responsive layout, summary stats, and skip-to-content link.
4. Search for `security` or `library` and show HTMX updating results without a full reload (URL query updates too).
5. Filter by category and date range.
6. Open an event detail page as a guest and show that bookmark creation asks for login.
7. Register or log in (`sota` / `demo-pass-123` after seeding).
8. Create a bookmark and show the list updating asynchronously.
9. Create a new event, then edit and delete it as the author.
10. Show code structure: `models.py`, `services.py`, `selectors.py`, templates, tests, `openspec/specs/`, and deployment docs.
11. Hit `/healthz/` and walk through Render/Docker instructions in the README.

## Commands To Mention

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```

## Code Explanation Prompts

- Why views stay thin: business writes live in services.
- Why selectors exist: reusable filtered querysets for list + HTMX partials.
- Why templates matter for the rubric: no webpage design embedded in Python.
- Why auth gates matter: create/edit/delete/bookmark require a real user session.

## Deployment Note

Use the repository `https://github.com/aoi-nahoi/event-listings` on Render with `render.yaml`. After deployment, add the Render URL and `/healthz/` URL to the submission text file.
