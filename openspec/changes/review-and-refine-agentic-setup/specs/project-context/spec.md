## ADDED Requirements

### Requirement: Tech stack is documented
The project SHALL document its tech stack so agents can make informed decisions.

#### Scenario: Stack is discoverable
- **WHEN** an agent reads AGENTS.md or openspec/config.yaml
- **THEN** it SHALL find Python 3.10+, Django, SQLite (dev), Black, Ruff, pytest, pytest-cov listed as the tech stack

### Requirement: Project structure is documented
The project SHALL document its intended directory layout and app roles.

#### Scenario: Agent understands app boundaries
- **WHEN** an agent reads AGENTS.md
- **THEN** it SHALL find that `events` handles event CRUD, `accounts` handles auth, and `api` exposes REST endpoints

### Requirement: Conventions are documented
The project SHALL document coding conventions that agents must follow.

#### Scenario: Business logic placement
- **WHEN** an agent writes business logic
- **THEN** it SHALL put it in `services.py`, not in views

#### Scenario: Query placement
- **WHEN** an agent writes database queries
- **THEN** it SHALL put reusable queries in `selectors.py`

#### Scenario: View thinness
- **WHEN** an agent creates views
- **THEN** they SHALL delegate to services/selectors and contain minimal logic

### Requirement: Migration policy is documented
The project SHALL document a policy for database migrations.

#### Scenario: Old migrations are immutable
- **WHEN** a migration already exists and is committed
- **THEN** an agent SHALL NOT edit it; it SHALL create a new migration instead
