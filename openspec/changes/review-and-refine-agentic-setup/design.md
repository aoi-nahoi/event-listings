## Context

The project is a Django application skeleton — no Django project has been scaffolded yet. The `AGENTS.md` has basic structure (3 apps: `events`, `accounts`, `api`) and conventions (services.py for logic, selectors.py for queries, thin views). The OpenSpec directory has an empty `specs/` directory and a bare-minimum `config.yaml`. The `.opencode/` directory has 5 opsx commands and 5 skills for the experimental workflow.

There are no Django models, views, URLs, serializers, or tests yet. The intent is to build a local event listings platform.

## Goals / Non-Goals

**Goals:**
- Enrich `AGENTS.md` with Django-specific conventions, testing patterns, and a complete picture of the project's intended architecture.
- Populate `openspec/config.yaml` with project context, tech stack, and per-artifact rules.
- Create initial capability specs for the four foundational areas: project-context, event-management, user-auth, api-endpoints.
- Ensure the `.opencode/` commands have clear, consistent descriptions.

**Non-Goals:**
- Scaffolding the actual Django project (that's implementation, not setup).
- Writing application code of any kind.
- Setting up CI/CD or deployment pipelines.

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Spec granularity | One spec per AGENTS.md app plus a project-context spec | Aligns with existing mental model; easy to maintain and reference |
| Project context location | `openspec/config.yaml` for machine-readable context + `AGENTS.md` for agent-facing instructions | Keeps concerns separate; config.yaml feeds OpenSpec, AGENTS.md feeds the opencode agent directly |
| Spec content level | Capability-level with key requirements and scenarios, not exhaustive | The project is pre-implementation; specs should guide future work without over-committing to design details |
| `.opencode/commands` descriptions | Review and add `description` frontmatter where missing | Improves `/` command discoverability for the user |

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Specs may become stale as the project evolves | Treat them as living documents; update during implementation changes |
| Over-specifying before implementation | Keep specs at capability level, avoids detailed technical specs that belong in design docs |
