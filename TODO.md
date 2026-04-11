# TODO / Backlog

> **Governor**: @project-manager — invoke for sprint planning, prioritization, and feature breakdown
> **Agents**: May add items to "Backlog" and move completed items to "Completed". Preserve section order. Never reorder items within a section — priority position is set by humans or @project-manager when explicitly asked.

---

## In Progress

- [ ] #005 — Implement user authentication and management [area: backend] → [.tasks/005-user-auth.md](.tasks/005-user-auth.md)

---

## Up Next (prioritized)

---

## Backlog

- [ ] #006 — Add loan/borrow functionality [area: backend] → [.tasks/006-loan-system.md](.tasks/006-loan-system.md)
- [ ] #007 — Integrate AI chatbox for book recommendations [area: frontend] → [.tasks/007-ai-chatbox.md](.tasks/007-ai-chatbox.md)
- [ ] #008 — Set up testing infrastructure [area: qa] → [.tasks/008-testing-setup.md](.tasks/008-testing-setup.md)
- [ ] #009 — Deploy to GitHub Pages [area: infra] → [.tasks/009-deployment.md](.tasks/009-deployment.md)

---

## Completed

- [x] #000 — Initial project setup and template configuration → [.tasks/000-initial-project-setup.md](.tasks/000-initial-project-setup.md)
- [x] #001 — Set up project dependencies and basic structure [area: setup] → [.tasks/001-project-setup.md](.tasks/001-project-setup.md)
- [x] #002 — Design MySQL database schema for books, users, and loans [area: database] → [.tasks/002-database-schema.md](.tasks/002-database-schema.md)
- [x] #003 — Implement backend API with Django for CRUD operations [area: backend] → [.tasks/003-backend-api.md](.tasks/003-backend-api.md)
- [x] #004 — Create frontend interface for book management [area: frontend] → [.tasks/004-frontend-books.md](.tasks/004-frontend-books.md)

---

## Item Format Guide

When adding new items, use this format:

```
- [ ] #NNN — Brief description of the task [area: frontend|backend|database|qa|docs|infra|design] → [.tasks/NNN-short-title.md](.tasks/NNN-short-title.md)
```

Every TODO item must have a corresponding `.tasks/NNN-*.md` file. @project-manager creates both together.

**Area tags** help agents know which specialist to use:

- `frontend` → @frontend-developer
- `backend` → @backend-developer
- `database` → @database-expert
- `design` → @ui-ux-designer
- `qa` → @qa-engineer
- `docs` → @documentation-writer
- `infra` → @systems-architect
- `setup` → general

**Priority**: Items higher in "Up Next" are higher priority. Agents move completed items to "Completed" and may add new items to "Backlog". Only humans reorder items within a section to change priority, unless explicitly asked to reprioritize.
