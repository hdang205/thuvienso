#005 — Implement user authentication and management

## Overview

Implement user authentication system with login/register functionality, session management, and role-based access control for the library system.

## Requirements

### Backend Authentication

- [ ] Set up Django authentication with custom User model
- [ ] Create login/register API endpoints
- [ ] Implement JWT token authentication
- [ ] Add role-based permissions (librarian, student)
- [ ] Create user profile management endpoints

### Frontend Authentication

- [ ] Create login/register forms in frontend
- [ ] Implement session management and token storage
- [ ] Add authentication state management
- [ ] Create protected routes/pages based on user role
- [ ] Add logout functionality

### Security Features

- [ ] Password hashing and validation
- [ ] CSRF protection
- [ ] Rate limiting for auth endpoints
- [ ] Secure token storage in frontend

## Technical Details

### API Endpoints to Create

```
POST /api/auth/login/ - User login
POST /api/auth/register/ - User registration
POST /api/auth/logout/ - User logout
GET /api/auth/me/ - Get current user info
PUT /api/auth/profile/ - Update user profile
```

### Frontend Pages

- Login page with form validation
- Registration page with role selection
- User profile page
- Role-based navigation (librarian vs student views)

### Database Changes

- Ensure User model supports roles
- Add any additional auth-related fields if needed

## Acceptance Criteria

- [ ] Users can register with email, username, password, and role
- [ ] Users can login and receive JWT tokens
- [ ] Frontend stores tokens securely and handles expiration
- [ ] Role-based UI (librarians see admin features, students see basic features)
- [ ] Logout clears session properly
- [ ] API endpoints are protected and require authentication

## Testing

- [ ] Unit tests for auth endpoints
- [ ] E2E tests for login/register flow
- [ ] Test role-based access control
