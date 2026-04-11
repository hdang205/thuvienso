# #003 — Implement backend API with Django for CRUD operations

**Area**: backend  
**Status**: In Progress  
**Assigned**: @backend-developer  
**Priority**: High  
**Estimated effort**: 2-3 hours

## Objective

Create REST API endpoints for CRUD operations on books, users, and loans using Django REST Framework.

## Requirements

- Create serializers for User, Book, Loan models
- Implement ViewSets for CRUD operations
- Set up URL routing
- Add proper permissions and authentication
- Test API endpoints

## Acceptance Criteria

- [ ] GET /api/books/ - list all books
- [ ] POST /api/books/ - create new book
- [ ] GET /api/books/{id}/ - get book details
- [ ] PUT /api/books/{id}/ - update book
- [ ] DELETE /api/books/{id}/ - delete book
- [ ] Similar endpoints for users and loans
- [ ] API returns proper JSON responses
- [ ] CORS configured for frontend access

## Implementation Notes

- Use ModelViewSet for standard CRUD
- Add search/filter functionality
- Handle book availability logic
- Document API in docs/technical/API.md

## Risks

- Authentication complexity
- Permission handling

## Next Steps

After completion, move to #004 (frontend interface).
