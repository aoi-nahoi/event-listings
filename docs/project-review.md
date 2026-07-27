# Project Review Evidence

## Reviewed Materials

- Exercise 1 proposal: Event Listings
- Exercise 2 architecture plan
- Django implementation in `src/events_app/` and `src/accounts/`
- Tests in `tests/`
- Deployment configuration in `render.yaml` and README Docker section
- Specs in `openspec/specs/`

## Rubric Coverage

| Rubric item | Evidence |
| --- | --- |
| Tools/AI setup | `.gitignore`, `AGENTS.md`, `.pylintrc`, Cursor skill, OpenSpec config/specs, Ruff, pytest |
| Managerial practices | GitHub issues, linked commits, pull request review comments, CONTRIBUTING, PR/issue templates |
| Database schema | Django User, Category, OrganizerProfile, Event, and Bookmark with relationships |
| Business logic/views | Services, selectors, Django views, forms with validation, pagination, seed workflow |
| Use of templates | Templates render all HTML pages and HTMX partials; Python views do not contain page design |
| User input | Registration/login, event form, bookmark form, search/filter form with date-range validation |
| Rich interface/HTMX | Async event filtering with URL push, bookmark partial update, responsive and accessible UI |
| Tests/specs/docs | pytest coverage, README, docs, OpenSpec specs, presentation notes |
| Project deployment | Render commands, `render.yaml`, health check, Docker run instructions |
| Presentation performance | Demo script and code explanation notes |

## Verification

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```

## GitHub Evidence

- Issue #1 reviews rubric coverage.
- Issue #2 tracks code quality review.
- Issue #3 tracks final demo and deployment evidence.
- Issue #4 tracks UI and accessibility polish.
- Pull request review comments should mention services, selectors, templates, HTMX, auth, and deployment settings.

## Architecture Talking Points

1. `views.py` stays thin and delegates writes to `services.py`.
2. `selectors.py` centralizes published-event filtering including title/description/location search.
3. Templates own markup; CSS provides the modern responsive presentation.
4. `@login_required` protects create/edit/delete/bookmark; author/staff checks protect edit/delete.

## Known Limitations

- SQLite is used for the course demo.
- Bookmark records store an attendee name rather than a hard User foreign key, but creation still requires login.
