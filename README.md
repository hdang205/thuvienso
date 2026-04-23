# thư viện số FBU

> Dự án này giúp sinh viên chọn lựa sách mượn trả, quản lý thư viện sách một cách số hóa.

---

## Overview

Dự án này giúp sinh viên chọn lựa sách mượn trả, quản lý thư viện sách một cách số hóa. Nó phục vụ thủ thư và sinh viên. Giải quyết vấn đề thủ thư tốn nhiều thời gian hơn để quản lý nhập kho, sinh viên chọn sách sai với hướng học tập và quên trả sách đúng hạn.

Hệ thống cho phép thủ thư quản lý kho sách hiệu quả hơn, trong khi sinh viên có thể dễ dàng tìm kiếm và mượn sách phù hợp với nhu cầu học tập. Điều này giúp tối ưu hóa quy trình quản lý thư viện và cải thiện trải nghiệm người dùng.

---

## Tech Stack

| Layer    | Technology            | Notes                |
| -------- | --------------------- | -------------------- |
| Frontend | HTML, CSS, JavaScript | Static website       |
| Backend  | JavaScript, Django    | API and server logic |
| Database | MySQL                 | Data storage         |
| ORM      | Sequelize             | Database queries     |
| Hosting  | GitHub Pages          | Static site hosting  |

---

## Getting Started

### Prerequisites

- Node.js LTS (see `.nvmrc`)
- npm
- MySQL server running locally

### Installation

```bash
# Clone the repository
git clone https://github.com/[org]/[repo].git
cd [repo]

# Install dependencies
npm install

# Set up database
# Create MySQL database and update connection details
```

### Running Locally

```bash
# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Running Tests

```bash
# Unit tests
npm test

# E2E tests (requires dev server running)
npm run test:e2e
```

---

## Project Structure

```
[project-root]/
├── src/
│   ├── app/              # [e.g., Next.js App Router pages and layouts]
│   ├── components/       # Shared UI components
│   └── lib/              # Utilities, helpers, shared logic
├── tests/
│   └── e2e/              # Playwright E2E tests
├── docs/
│   ├── user/             # User-facing documentation
│   └── technical/        # Architecture, API, database docs
├── .claude/agents/       # Claude Code specialist agents
├── public/               # Static assets
├── PRD.md                # Product requirements (source of truth)
├── TODO.md               # Project backlog
└── CLAUDE.md             # Claude AI instructions
```

---

## Authentication

### Login via Email

The login endpoint (`POST /api/auth/login/`) accepts **both email and username**:

```json
{ "email": "librarian1@example.com", "password": "password123" }
```

or

```json
{ "username": "librarian1", "password": "password123" }
```

Demo accounts seeded by `populate_data.py`:

| Role      | Email                      | Username    | Password    |
| --------- | -------------------------- | ----------- | ----------- |
| Student   | student1@example.com       | student1    | password123 |
| Librarian | librarian1@example.com     | librarian1  | password123 |

---

## Environment Variables

| Variable          | Required | Description                                          |
| ----------------- | -------- | ---------------------------------------------------- |
| DB_HOST           | Yes      | MySQL database host                                  |
| DB_USER           | Yes      | MySQL database user                                  |
| DB_PASSWORD       | Yes      | MySQL database password                              |
| DB_NAME           | Yes      | MySQL database name                                  |
| NODE_ENV          | No       | Environment (development/production)                 |
| ADMIN_EMAIL       | No       | Email for the admin account created at deploy time   |
| ADMIN_PASSWORD    | No       | Password for the admin account (use a strong value)  |
| ADMIN_USERNAME    | No       | Username for the admin (defaults to ADMIN_EMAIL)     |
| ADMIN_FIRST_NAME  | No       | Admin first name                                     |
| ADMIN_LAST_NAME   | No       | Admin last name                                      |

See `.env.example` for all available variables.

---

## Admin Account Seeding

Use the `ensure_admin_user` management command to safely create or update an admin
account via environment variables. **Never hardcode credentials in source code.**

### Running locally

```bash
ADMIN_EMAIL=admin@library.edu \
ADMIN_PASSWORD=YourStrongPassword123! \
python manage.py ensure_admin_user
```

### On Railway / Render / any backend host

1. Go to your backend service settings and add the environment variables:
   - `ADMIN_EMAIL` — the admin's email address
   - `ADMIN_PASSWORD` — a strong password (min 12 characters recommended)
   - `ADMIN_USERNAME` *(optional)* — defaults to the email value
2. In your deploy hook / release command, run:
   ```
   python manage.py migrate && python manage.py ensure_admin_user
   ```

### Vercel + separate backend note

If your **frontend is on Vercel** and your **backend is on Railway/Render/Fly.io**:
- Set env vars on the **backend** host, not on Vercel.
- Vercel only serves the static frontend; it cannot run Django management commands.
- The `ADMIN_EMAIL` / `ADMIN_PASSWORD` variables should **never** be added to Vercel.

---

## Deployment

The application deploys automatically via GitHub Actions on merge to `main`.

- **Production**: [URL]
- **Staging**: [URL]

Manual deployment:

```bash
[npm run build]
[deployment command]
```

---

## License

[MIT / proprietary / other] — see [LICENSE](LICENSE)
