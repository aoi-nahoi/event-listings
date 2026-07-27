---
name: event-listings
description: Conventions for the Event Listings Django + HTMX project. Use when editing events_app, accounts, templates, tests, docs, or OpenSpec files in this repository.
---

# Event Listings Agent Skill

## Architecture

- Keep HTML in Django templates only.
- Put business logic in `events_app/services.py`.
- Put reusable queries in `events_app/selectors.py`.
- Keep views thin (request/response only).
- Prefer English for user-facing text and documentation.

## Auth rules

- Event create/edit/delete and bookmark create require login.
- Only the event author or staff may edit or delete an event.
- Guests may browse, search, and filter published events.

## Verification

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```

## Docs evidence

- Rubric mapping: `docs/rubric-alignment.md`
- Demo script: `docs/final-demo-notes.md`
- Specs: `openspec/specs/`
