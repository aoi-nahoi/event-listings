## ADDED Requirements

### Requirement: API exposes event CRUD
The API SHALL provide REST endpoints for creating, reading, updating, and deleting events.

#### Scenario: List events via API
- **WHEN** a GET request is made to `/api/events/`
- **THEN** the API SHALL return a paginated JSON list of upcoming events

#### Scenario: Create event via API
- **WHEN** an authenticated user sends a POST request to `/api/events/` with valid event data
- **THEN** the API SHALL create the event and return the event data with a 201 status

#### Scenario: Retrieve event detail via API
- **WHEN** a GET request is made to `/api/events/{id}/`
- **THEN** the API SHALL return the JSON representation of that event

#### Scenario: Update event via API
- **WHEN** the event creator sends a PUT/PATCH request to `/api/events/{id}/` with updated data
- **THEN** the API SHALL update the event and return the updated data

#### Scenario: Delete event via API
- **WHEN** the event creator sends a DELETE request to `/api/events/{id}/`
- **THEN** the API SHALL delete the event and return a 204 status

### Requirement: API requires authentication for mutations
The API SHALL require authentication for write operations (create, update, delete).

#### Scenario: Unauthenticated create rejected
- **WHEN** an unauthenticated user sends a POST to `/api/events/`
- **THEN** the API SHALL return a 401 Unauthorized response

#### Scenario: Non-creator update rejected
- **WHEN** a user who did not create the event sends a PUT to `/api/events/{id}/`
- **THEN** the API SHALL return a 403 Forbidden response

### Requirement: API exposes user registration and auth
The API SHALL provide endpoints for user registration, login, and token management.

#### Scenario: Register via API
- **WHEN** a POST request is made to `/api/auth/register/` with valid user data
- **THEN** the API SHALL create the user and return an auth token

#### Scenario: Login via API
- **WHEN** a POST request is made to `/api/auth/login/` with valid credentials
- **THEN** the API SHALL return an auth token

### Requirement: API supports search and filtering
The API SHALL support query parameters for searching and filtering events.

#### Scenario: Search events by keyword
- **WHEN** a GET request is made to `/api/events/?search=keyword`
- **THEN** the API SHALL return events matching the keyword in title or description

#### Scenario: Filter events by category
- **WHEN** a GET request is made to `/api/events/?category=Music`
- **THEN** the API SHALL return only events in the Music category
