## Why

The current agentic setup (AGENTS.md, OpenSpec config, .opencode) is sparse — it lacks project-specific context, domain knowledge, tech stack details, and structured capability specs. This makes agent interactions less effective: the AI lacks awareness of the Django project's architecture, testing patterns, deployment strategy, and conventions, leading to generic suggestions and more back-and-forth. Refining the setup will make agent interactions faster, more accurate, and more autonomous.

## What Changes

- Enrich `AGENTS.md` with tech stack details, app structure descriptions, testing patterns, and Django-specific conventions.
- Populate `openspec/config.yaml` with project context and per-artifact rules.
- Create initial capability specs under `openspec/specs/` for the three main apps (`events`, `accounts`, `api`).
- Review and organize `.opencode/` directory — ensure commands/skills are properly configured.
- Improve `.opencode/commands/` descriptions where needed for discoverability.

## Capabilities

### New Capabilities
- `project-context`: Project-level metadata, tech stack, conventions, directory layout — the foundation all agents need.
- `event-management`: Requirements for creating, listing, searching, and managing local event listings.
- `user-auth`: Requirements for user authentication (registration, login, password management, session handling).
- `api-endpoints`: Requirements for REST API endpoints exposed by the API app.

### Modified Capabilities

- *(none — no existing specs to modify)*

## Impact

- No application code changed — purely agentic configuration and documentation.
- All agents interacting with this repo will have richer context, leading to better suggestions.
- Existing agent workflows (opencode commands/skills) may need minor updates for consistency.
