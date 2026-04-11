<!--
DOCUMENT METADATA
Owner: @database-expert
Update trigger: Any schema change, migration, index addition, or significant query pattern decision
Update scope: Full document
Read by: @backend-developer (to write queries), @systems-architect (for scaling and architecture decisions)
-->

# Database Reference

> **Engine**: SQLite (development), MySQL (production)
> **ORM / Query layer**: Django ORM
> **Connection**: Via DATABASES setting in settings.py
> **Last updated**: 2026-04-11

---

## Schema Overview

The database schema supports a digital library management system with users (students and librarians), books inventory, and loan transactions.

```
users ──< loans >── books
```

**Key relationships**:

- `users` → `loans`: One user can have many loans (borrow history)
- `books` → `loans`: One book can have many loans (borrow history)
- Users have roles: student or librarian

---

## Tables

---

### library_user

**Purpose**: Stores all user accounts with roles for library management.

| Column       | Type         | Constraints                  | Description                         |
| ------------ | ------------ | ---------------------------- | ----------------------------------- |
| id           | integer      | PK, NOT NULL, AUTO_INCREMENT | Primary key                         |
| password     | varchar(128) | NOT NULL                     | Password hash                       |
| last_login   | datetime     | NULL                         | Last login timestamp                |
| is_superuser | bool         | NOT NULL                     | Superuser flag                      |
| username     | varchar(150) | NOT NULL, UNIQUE             | Username                            |
| first_name   | varchar(150) | NOT NULL                     | First name                          |
| last_name    | varchar(150) | NOT NULL                     | Last name                           |
| email        | varchar(254) | NOT NULL                     | Email address                       |
| is_staff     | bool         | NOT NULL                     | Staff status                        |
| is_active    | bool         | NOT NULL                     | Active status                       |
| date_joined  | datetime     | NOT NULL                     | Join date                           |
| role         | varchar(10)  | NOT NULL, DEFAULT 'student'  | User role: 'student' or 'librarian' |
| student_id   | varchar(20)  | NULL                         | Student ID number                   |
| phone        | varchar(15)  | NULL                         | Phone number                        |

---

### library_book

**Purpose**: Stores book inventory information.

| Column             | Type         | Constraints                  | Description           |
| ------------------ | ------------ | ---------------------------- | --------------------- |
| id                 | integer      | PK, NOT NULL, AUTO_INCREMENT | Primary key           |
| title              | varchar(200) | NOT NULL                     | Book title            |
| author             | varchar(100) | NOT NULL                     | Book author           |
| isbn               | varchar(13)  | NOT NULL, UNIQUE             | ISBN number           |
| category           | varchar(50)  | NOT NULL                     | Book category/genre   |
| description        | text         |                              | Book description      |
| total_quantity     | integer      | NOT NULL, DEFAULT 1          | Total copies owned    |
| available_quantity | integer      | NOT NULL, DEFAULT 1          | Available copies      |
| published_date     | date         | NULL                         | Publication date      |
| created_at         | datetime     | NOT NULL                     | Creation timestamp    |
| updated_at         | datetime     | NOT NULL                     | Last update timestamp |

---

### library_loan

**Purpose**: Tracks book borrowing and returning transactions.

| Column      | Type        | Constraints                    | Description                               |
| ----------- | ----------- | ------------------------------ | ----------------------------------------- |
| id          | integer     | PK, NOT NULL, AUTO_INCREMENT   | Primary key                               |
| user_id     | integer     | NOT NULL, FK → library_user.id | Borrower                                  |
| book_id     | integer     | NOT NULL, FK → library_book.id | Borrowed book                             |
| loan_date   | datetime    | NOT NULL                       | Borrow date                               |
| due_date    | datetime    | NOT NULL                       | Due date                                  |
| return_date | datetime    | NULL                           | Return date                               |
| status      | varchar(10) | NOT NULL, DEFAULT 'borrowed'   | Status: 'borrowed', 'returned', 'overdue' |
| notes       | text        |                                | Additional notes                          |

---

## Indexes

- `library_book_isbn` on `library_book.isbn` (UNIQUE)
- `library_loan_user_id` on `library_loan.user_id`
- `library_loan_book_id` on `library_loan.book_id`
- `library_loan_status` on `library_loan.status`
- `library_loan_loan_date` on `library_loan.loan_date`

---

## Data Integrity Rules

- Available quantity cannot exceed total quantity
- Cannot loan a book with 0 available copies
- Due dates must be after loan dates
- Return dates must be after loan dates when status is 'returned'
  | email_verified_at | timestamptz | NULL | NULL until email is verified |
  | created_at | timestamptz | NOT NULL, DEFAULT now() | Record creation time |
  | updated_at | timestamptz | NOT NULL, DEFAULT now() | Last modification time |

**Indexes**:

- `idx_users_email` on `(email)` — frequent lookup by email at login

**Notes**: Soft deletes not used — accounts are hard-deleted. Ensure all related records are cascade-deleted.

---

### sessions

**Purpose**: Active authentication sessions for logged-in users.

| Column     | Type        | Constraints                               | Description                          |
| ---------- | ----------- | ----------------------------------------- | ------------------------------------ |
| id         | uuid        | PK, NOT NULL, DEFAULT gen_random_uuid()   | Session token (used as Bearer token) |
| user_id    | uuid        | NOT NULL, FK → users.id ON DELETE CASCADE | The authenticated user               |
| expires_at | timestamptz | NOT NULL                                  | Session expiry time                  |
| created_at | timestamptz | NOT NULL, DEFAULT now()                   | Session creation time                |
| user_agent | text        | NULL                                      | Browser/client identifier            |
| ip_address | inet        | NULL                                      | Client IP at session creation        |

**Indexes**:

- `idx_sessions_user_id` on `(user_id)` — list sessions per user
- `idx_sessions_expires_at` on `(expires_at)` — efficient cleanup of expired sessions

**Relationships**:

- `user_id` → `users.id` (ON DELETE CASCADE — deleting a user removes all their sessions)

---

### [table_name]

**Purpose**: [What this table stores and why]

| Column     | Type        | Constraints                             | Description   |
| ---------- | ----------- | --------------------------------------- | ------------- |
| id         | uuid        | PK, NOT NULL, DEFAULT gen_random_uuid() | Primary key   |
| [column]   | [type]      | [constraints]                           | [description] |
| created_at | timestamptz | NOT NULL, DEFAULT now()                 |               |
| updated_at | timestamptz | NOT NULL, DEFAULT now()                 |               |

**Indexes**: [None / list with reason for each]

**Relationships**: [None / list FK relationships]

**Notes**: [Denormalization decisions, soft-delete patterns, business rules in constraints]

---

## Migrations Log

| Migration File            | Date         | Description           | Reversible | Deployment Risk |
| ------------------------- | ------------ | --------------------- | ---------- | --------------- |
| `001_create_users.sql`    | [YYYY-MM-DD] | Create users table    | Yes        | None            |
| `002_create_sessions.sql` | [YYYY-MM-DD] | Create sessions table | Yes        | None            |

---

## Query Patterns

### Common Patterns

**Get user by email (login)**:

```sql
SELECT id, email, password_hash, role
FROM users
WHERE email = $1
LIMIT 1;
```

Uses `idx_users_email` index — fast.

**Validate session token**:

```sql
SELECT s.user_id, u.email, u.role
FROM sessions s
JOIN users u ON u.id = s.user_id
WHERE s.id = $1
  AND s.expires_at > now();
```

**Cleanup expired sessions** (run as scheduled job):

```sql
DELETE FROM sessions
WHERE expires_at < now();
```

---

## Known Issues & Tech Debt

| Issue                            | Impact                          | Plan                                 |
| -------------------------------- | ------------------------------- | ------------------------------------ |
| [e.g., No soft deletes on users] | [Hard deletes lose audit trail] | [Consider adding `deleted_at` in v2] |
