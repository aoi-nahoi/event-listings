# Contributing

## Workflow

1. Open or update a GitHub Issue that describes the goal.
2. Create a branch and implement a focused change.
3. Reference the issue in commits (`refs #N` or `Closes #N`).
4. Open a pull request using the repository template.
5. Request review and address feedback before merge.

## Local checks

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```

## Code review expectations

Reviewers should check:

- separation of services, selectors, views, and templates
- authentication and authorization for mutating actions
- HTMX partials still work with search and pagination
- tests and docs stay in sync with behavior
