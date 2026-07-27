# User authentication

## Requirements

### Requirement: Visitors can register
The system SHALL allow visitors to create an account with username, email, and password.

#### Scenario: Successful registration
- **WHEN** a visitor submits a valid registration form
- **THEN** the system SHALL create the user and redirect to the events list

### Requirement: Users can log in and log out
The system SHALL provide login and logout flows.

#### Scenario: Login
- **WHEN** a registered user submits valid credentials
- **THEN** the system SHALL authenticate the session and redirect to the events list

#### Scenario: Logout
- **WHEN** an authenticated user logs out
- **THEN** the system SHALL end the session and return to the events list
