## ADDED Requirements

### Requirement: Users can create events
The system SHALL allow authenticated users to create local event listings with title, description, date/time, location, and category.

#### Scenario: Create event with all fields
- **WHEN** an authenticated user submits a valid event creation form with title, description, date, time, location, and category
- **THEN** the system SHALL save the event and redirect to the event detail page

#### Scenario: Create event with missing required fields
- **WHEN** an authenticated user submits an event creation form with missing required fields
- **THEN** the system SHALL display validation errors and not save the event

### Requirement: Users can browse events
The system SHALL allow any visitor (authenticated or not) to browse a list of upcoming events.

#### Scenario: Browse all upcoming events
- **WHEN** a visitor navigates to the events listing page
- **THEN** the system SHALL display a paginated list of upcoming events sorted by date

### Requirement: Users can search events
The system SHALL allow visitors to search events by keyword, date range, location, and category.

#### Scenario: Search by keyword
- **WHEN** a visitor enters a search keyword
- **THEN** the system SHALL return events whose title or description matches the keyword

#### Scenario: Filter by category
- **WHEN** a visitor selects a category filter
- **THEN** the system SHALL return only events in that category

### Requirement: Event creators can edit and delete their events
The system SHALL allow the event creator to edit or delete their own events.

#### Scenario: Edit own event
- **WHEN** the creator of an event submits edits to that event
- **THEN** the system SHALL update the event and redirect to the event detail page

#### Scenario: Delete own event
- **WHEN** the creator of an event requests deletion
- **THEN** the system SHALL remove the event and redirect to the events listing page

#### Scenario: Non-creator cannot edit
- **WHEN** a user who is not the creator attempts to edit an event
- **THEN** the system SHALL return a 403 Forbidden response

### Requirement: Events have categories
The system SHALL categorize events (e.g., Music, Sports, Arts, Tech, Food, Other).

#### Scenario: Category selection
- **WHEN** a user creates or edits an event
- **THEN** they SHALL be able to select from a predefined list of categories
