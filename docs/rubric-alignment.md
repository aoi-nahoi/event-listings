# Rubric Alignment

| Rubric item | Target | Evidence in this project |
| --- | --- | --- |
| Tools/AI setup | Solid (3) | `.gitignore`, `AGENTS.md`, `.pylintrc`, `.cursor/skills/event-listings/`, `.opencode/skills/`, `openspec/`, Ruff in `pyproject.toml` |
| Managerial practices | Solid (3) | GitHub Issues #1–#4 linked in commits/PR #5, `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, issue templates |
| Database schema | Solid (3) | `Category`, `OrganizerProfile`, `Event`, `Bookmark`, Django `User` with foreign keys in `models.py` |
| Business logic/views | Solid (3) | `services.py`, `selectors.py`, thin `views.py`, forms validation, seed workflow |
| Use of templates | Solid (3) | All pages/partials in Django templates; no HTML design strings in Python views |
| User input | Solid (3) | Register/login/logout, search/filter validation, event CRUD forms, bookmark form |
| Rich interface/HTMX | Solid (3) | Async filters with `hx-push-url`, bookmark partials, responsive CSS, skip link, `:focus-visible`, `aria-live` |
| Tests/specs/docs | Extensive (4) | `tests/`, `openspec/specs/`, `README.md`, `docs/*` |
| Project deployment | Solid (3) | `render.yaml`, WhiteNoise, Gunicorn, `/healthz/`, Docker instructions in README |
| Presentation performance | Solid (3) | `docs/final-demo-notes.md` and `docs/project-review.md` for run/demo/code explanation |

## Score plan

Maximum for these rows: **31**. This repository is organized so each Solid/Extensive cell has concrete files a reviewer can open during the demo.
