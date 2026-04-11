# #001 — Set up project dependencies and basic structure

**Area**: setup  
**Status**: In Progress  
**Assigned**: @project-manager (initial), then delegate to specialists  
**Priority**: High  
**Estimated effort**: 2-3 hours

## Objective

Initialize the project with basic dependencies, folder structure, and configuration files for both frontend (HTML/CSS/JS) and backend (Django + MySQL).

## Requirements

- Set up Node.js environment for frontend
- Set up Python/Django environment for backend
- Install necessary packages (npm for frontend, pip for backend)
- Create basic project structure
- Configure environment variables template (.env.example)
- Ensure development scripts work

## Acceptance Criteria

- [ ] `npm install` succeeds for frontend dependencies
- [ ] Django project initialized with basic settings
- [ ] MySQL connection configured
- [ ] `npm run dev` starts development server
- [ ] Basic folder structure matches CLAUDE.md
- [ ] .env.example created with required variables

## Implementation Notes

- Frontend: Static site with HTML/CSS/JS, hosted on GitHub Pages
- Backend: Django REST API for data operations
- Database: MySQL with Sequelize ORM
- Use LTS versions of Node and Python

## Risks

- Version conflicts between packages
- MySQL setup issues on local machine

## Next Steps

After completion, move to #002 (database schema design).
