## ADDED Requirements

### Requirement: Users can register
The system SHALL allow new users to create an account with email and password.

#### Scenario: Successful registration
- **WHEN** a visitor submits a registration form with valid email, password, and password confirmation
- **THEN** the system SHALL create the user account, log them in, and redirect to the home page

#### Scenario: Duplicate email registration
- **WHEN** a visitor submits a registration form with an email that is already registered
- **THEN** the system SHALL display an error message indicating the email is already in use

### Requirement: Users can log in and log out
The system SHALL allow registered users to log in and log out.

#### Scenario: Successful login
- **WHEN** a registered user submits valid credentials
- **THEN** the system SHALL log them in and redirect to the home page

#### Scenario: Failed login
- **WHEN** a user submits invalid credentials
- **THEN** the system SHALL display an error message and stay on the login page

#### Scenario: Logout
- **WHEN** an authenticated user clicks logout
- **THEN** the system SHALL log them out and redirect to the home page

### Requirement: Users can reset their password
The system SHALL allow users to reset their password via email.

#### Scenario: Password reset request
- **WHEN** a user submits their email on the password reset page
- **THEN** the system SHALL send a password reset link to that email

#### Scenario: Password reset with valid token
- **WHEN** a user clicks a valid password reset link and submits a new password
- **THEN** the system SHALL update their password and redirect to the login page

### Requirement: Users have profiles
The system SHALL allow users to view and edit their profile (name, bio, profile picture).

#### Scenario: View own profile
- **WHEN** an authenticated user navigates to their profile page
- **THEN** the system SHALL display their account details

#### Scenario: Edit profile
- **WHEN** an authenticated user submits profile edits
- **THEN** the system SHALL update their profile and display the updated information
