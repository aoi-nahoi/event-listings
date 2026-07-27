# Event management

## Requirements

### Requirement: Users can browse published events
The system SHALL allow any visitor to browse a paginated list of published events.

#### Scenario: Browse events
- **WHEN** a visitor opens the home page
- **THEN** the system SHALL show published events with title, date, location, category, and organizer

### Requirement: Users can search and filter events
The system SHALL allow visitors to search by keyword and filter by category and date range.

#### Scenario: Keyword search
- **WHEN** a visitor enters a keyword
- **THEN** the system SHALL return events matching title, description, or location

#### Scenario: Category and date filters
- **WHEN** a visitor selects a category and/or date range
- **THEN** the system SHALL return only matching published events

### Requirement: Authenticated users can create events
The system SHALL allow authenticated users to create events with category, title, description, date, location, and status.

#### Scenario: Create requires login
- **WHEN** an anonymous visitor opens the create event page
- **THEN** the system SHALL redirect to login

### Requirement: Authors can edit and delete their events
The system SHALL allow the event author or staff to edit or delete an event.

#### Scenario: Non-author cannot edit
- **WHEN** another authenticated user opens the edit page
- **THEN** the system SHALL return 403 Forbidden

### Requirement: Authenticated users can bookmark events
The system SHALL allow logged-in users to bookmark an event with a name and optional note via HTMX.

#### Scenario: Bookmark requires login
- **WHEN** an anonymous visitor posts a bookmark
- **THEN** the system SHALL redirect to login and not create a bookmark
