## Summary

- What changed and why

## Linked issues

- Closes #

## Review checklist

- [ ] Business logic stays in `services.py` / queries in `selectors.py`
- [ ] Templates contain the UI (no HTML strings in views)
- [ ] Auth and permissions are correct for create/edit/delete/bookmark
- [ ] Tests updated for model/view/form/service changes
- [ ] Docs updated when user-facing behavior changes

## Test plan

- [ ] `python3 -m uv run ruff check .`
- [ ] `python3 -m uv run python manage.py check`
- [ ] `python3 -m uv run pytest`
- [ ] Manual check of list filters (HTMX) and bookmark create while logged in
