# Project Review Evidence

## Reviewed Materials

- Exercise 1 proposal: Event Listings
- Exercise 2 architecture plan
- Django implementation in `src/events_app/`
- Tests in `tests/`
- Deployment configuration in `render.yaml`

## Rubric Coverage

| Rubric item | Evidence |
| --- | --- |
| Tools/AI setup | `.gitignore`, `AGENTS.md`, `pyproject.toml`, Ruff, pytest |
| Managerial practices | Git issues, commits, pull request, and review comments can be linked around this evidence |
| Database schema | Django User, Category, OrganizerProfile, Event, and Bookmark models with relationships |
| Business logic/views | Services, selectors, Django views, forms, pagination, and seed workflow |
| Use of templates | Templates render all HTML pages; Python views do not contain page design |
| User input | Event form, bookmark form, search/filter form, seed demo action |
| Rich interface/HTMX | Async event filtering and bookmark partial update |
| Tests/specs/docs | pytest coverage, README, docs, presentation notes |
| Project deployment | Render commands and `render.yaml` |
| Presentation performance | Demo script and code explanation files |

## Verification

- `python3 -m uv run ruff check .`
- `python3 -m uv run python manage.py check`
- `python3 -m uv run pytest`

## GitHub Evidence

- Issue #1 reviews rubric coverage.
- Issue #2 tracks code quality review.
- Issue #3 tracks final demo and deployment evidence.
- Issue #4 tracks simple UI and accessibility polish.
- Pull request review comments should mention services, selectors, templates, HTMX, and deployment settings.

## Known Limitations

- SQLite is used for the course demo.
- The app uses a simple organizer selection form instead of a full login workflow.
