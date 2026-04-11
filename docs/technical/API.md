<!--
DOCUMENT METADATA
Owner: @backend-developer
Update trigger: Any API endpoint is added, modified, or removed
Update scope: Full document
Read by: @frontend-developer (to know what endpoints to call and their contracts),
          @qa-engineer (for API contract testing)
-->

# API Reference

> **Base URL**: `http://localhost:8000/api` (development) · `https://api.thuvienso-fbu.com/api` (production)
> **Authentication**: Currently open (no auth required for development)
> **Content-Type**: `application/json` for all requests and responses
> **Last updated**: 2026-04-11

---

## Books API

### List Books

```
GET /api/books/
```

**Query Parameters:**

- `search` - Search in title, author, ISBN, category
- `category` - Filter by category
- `author` - Filter by author
- `ordering` - Order by: title, author, created_at

**Response:**

```json
[
  {
    "id": 1,
    "title": "Python Programming",
    "author": "John Smith",
    "isbn": "9780123456789",
    "category": "Programming",
    "description": "Learn Python programming",
    "total_quantity": 5,
    "available_quantity": 5,
    "published_date": "2023-01-01",
    "created_at": "2026-04-11T10:30:00Z",
    "updated_at": "2026-04-11T10:30:00Z"
  }
]
```

### Create Book

```
POST /api/books/
```

**Request Body:**

```json
{
  "title": "New Book",
  "author": "Author Name",
  "isbn": "9780123456789",
  "category": "Fiction",
  "description": "Book description",
  "total_quantity": 1
}
```

### Get Book Details

```
GET /api/books/{id}/
```

### Update Book

```
PUT /api/books/{id}/
```

### Delete Book

```
DELETE /api/books/{id}/
```

### Borrow Book

```
POST /api/books/{id}/borrow/
```

**Request Body:**

```json
{
  "user_id": 1,
  "due_date": "2026-04-25"
}
```

---

## Users API

### List Users

```
GET /api/users/
```

**Query Parameters:**

- `search` - Search in username, email, name
- `role` - Filter by role (student/librarian)
- `ordering` - Order by: date_joined, username

**Response:**

```json
[
  {
    "id": 1,
    "username": "student1",
    "email": "student1@example.com",
    "first_name": "Nguyen",
    "last_name": "Van A",
    "role": "student",
    "student_id": "2024001",
    "phone": null,
    "date_joined": "2026-04-11T10:30:00Z"
  }
]
```

### Create User

```
POST /api/users/
```

### Get User Details

```
GET /api/users/{id}/
```

### Update User

```
PUT /api/users/{id}/
```

### Delete User

```
DELETE /api/users/{id}/
```

---

## Loans API

### List Loans

```
GET /api/loans/
```

**Query Parameters:**

- `status` - Filter by status (borrowed/returned/overdue)
- `user` - Filter by user ID
- `book` - Filter by book ID
- `ordering` - Order by: loan_date, due_date

**Response:**

```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "student1",
      "email": "student1@example.com",
      "first_name": "Nguyen",
      "last_name": "Van A",
      "role": "student",
      "student_id": "2024001",
      "phone": null,
      "date_joined": "2026-04-11T10:30:00Z"
    },
    "book": {
      "id": 1,
      "title": "Python Programming",
      "author": "John Smith",
      "isbn": "9780123456789",
      "category": "Programming",
      "description": "Learn Python programming",
      "total_quantity": 5,
      "available_quantity": 4,
      "published_date": "2023-01-01",
      "created_at": "2026-04-11T10:30:00Z",
      "updated_at": "2026-04-11T10:30:00Z"
    },
    "loan_date": "2026-04-11T10:35:00Z",
    "due_date": "2026-04-25T00:00:00Z",
    "return_date": null,
    "status": "borrowed",
    "notes": ""
  }
]
```

### Create Loan

```
POST /api/loans/
```

**Request Body:**

```json
{
  "user_id": 1,
  "book_id": 1,
  "due_date": "2026-04-25",
  "notes": "Optional notes"
}
```

### Get Loan Details

```
GET /api/loans/{id}/
```

### Update Loan

```
PUT /api/loans/{id}/
```

### Delete Loan

```
DELETE /api/loans/{id}/
```

### Return Book

```
POST /api/loans/{id}/return_book/
```

**Request Body:**

```json
{
  "return_date": "2026-04-15"
}
```

---

## Standard Error Format

All error responses follow this structure:

```json
{
  "error": "Human-readable error message"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message 1", "Error message 2"]
}
```

}

````

**Common error codes**:
| HTTP Status | Code | Meaning |
|-------------|------|---------|
| 400 | `VALIDATION_ERROR` | Request body or params failed validation |
| 401 | `UNAUTHENTICATED` | No valid auth token provided |
| 403 | `UNAUTHORIZED` | Authenticated but insufficient permissions |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT` | Duplicate resource or state conflict |
| 422 | `UNPROCESSABLE` | Request understood but cannot be processed |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server-side error |

---

## Rate Limiting

- **Limit**: [100 requests per minute per IP / user]
- **Headers returned**:
  - `X-RateLimit-Limit` — requests allowed per window
  - `X-RateLimit-Remaining` — requests remaining in current window
  - `X-RateLimit-Reset` — Unix timestamp when window resets

---

## Endpoints

---

### Auth

#### POST /auth/register

**Auth required**: No
**Description**: Create a new user account.

**Request body**:
```json
{
  "email": "string — valid email address",
  "password": "string — minimum 8 characters",
  "name": "string — display name"
}
````

**Response 201**:

```json
{
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string",
    "createdAt": "ISO 8601 datetime"
  }
}
```

**Error codes**: `400` (validation), `409` (email already registered)

---

#### POST /auth/login

**Auth required**: No
**Description**: Authenticate with email and password. Returns a session token.

**Request body**:

```json
{
  "email": "string",
  "password": "string"
}
```

**Response 200**:

```json
{
  "token": "string — JWT or session token",
  "expiresAt": "ISO 8601 datetime",
  "user": {
    "id": "uuid",
    "email": "string",
    "name": "string"
  }
}
```

**Error codes**: `400` (validation), `401` (invalid credentials)

---

#### POST /auth/logout

**Auth required**: Yes
**Description**: Invalidate the current session token.

**Request body**: None

**Response 204**: No content

---

#### POST /auth/password-reset/request

**Auth required**: No
**Description**: Send a password reset email to the specified address.

**Request body**:

```json
{
  "email": "string"
}
```

**Response 200**: Always returns 200 to prevent email enumeration.

```json
{
  "message": "If an account exists, a reset email has been sent."
}
```

---

### [Resource: e.g., Users]

#### GET /users/me

**Auth required**: Yes
**Description**: Return the authenticated user's profile.

**Response 200**:

```json
{
  "id": "uuid",
  "email": "string",
  "name": "string",
  "role": "string",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime"
}
```

---

#### PATCH /users/me

**Auth required**: Yes
**Description**: Update the authenticated user's profile fields.

**Request body** (all fields optional):

```json
{
  "name": "string"
}
```

**Response 200**: Returns updated user object (same shape as GET /users/me)

**Error codes**: `400` (validation)

---

### [Resource 2: add sections below as endpoints are built]

---

## Changelog

| Date         | Change                                  |
| ------------ | --------------------------------------- |
| [YYYY-MM-DD] | Initial API definition — auth endpoints |
