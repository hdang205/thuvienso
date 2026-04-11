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

## Environment Variables

| Variable    | Required | Description                          |
| ----------- | -------- | ------------------------------------ |
| DB_HOST     | Yes      | MySQL database host                  |
| DB_USER     | Yes      | MySQL database user                  |
| DB_PASSWORD | Yes      | MySQL database password              |
| DB_NAME     | Yes      | MySQL database name                  |
| NODE_ENV    | No       | Environment (development/production) |

See `.env.example` for all available variables.

---

## Deployment

[Describe the deployment process. E.g.:]

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
