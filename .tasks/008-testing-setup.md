#008 — Set up testing infrastructure

## Overview

Implement comprehensive testing infrastructure for the library system including unit tests, integration tests, and end-to-end tests to ensure code quality and prevent regressions.

## Requirements

### Backend Testing (Django)

- [ ] Set up Django test framework with pytest
- [ ] Create unit tests for models (User, Book, Loan)
- [ ] Create API tests for all endpoints (books, users, loans, auth)
- [ ] Implement test fixtures for sample data
- [ ] Add coverage reporting with minimum 80% target
- [ ] Create integration tests for business logic

### Frontend Testing (JavaScript)

- [ ] Set up Vitest for unit testing
- [ ] Create tests for API helper functions
- [ ] Test authentication state management
- [ ] Test form validation and submission
- [ ] Add component testing for modals and forms
- [ ] Implement test coverage reporting

### End-to-End Testing (Playwright)

- [ ] Set up Playwright for E2E tests
- [ ] Create user journey tests (register → login → borrow book → return)
- [ ] Test role-based functionality (student vs librarian flows)
- [ ] Implement visual regression testing
- [ ] Add accessibility testing
- [ ] Create CI/CD integration for automated testing

## Technical Details

### Backend Test Structure

```
tests/
├── __init__.py
├── test_models.py      # Model unit tests
├── test_api.py         # API integration tests
├── test_auth.py        # Authentication tests
├── fixtures/
│   ├── users.json
│   ├── books.json
│   └── loans.json
└── conftest.py         # Test configuration
```

### Frontend Test Structure

```
tests/
├── unit/
│   ├── api.test.js
│   ├── auth.test.js
│   └── utils.test.js
└── e2e/
    ├── auth.spec.js
    ├── books.spec.js
    └── loans.spec.js
```

### Testing Tools

- **Backend:** pytest, pytest-django, pytest-cov, factory-boy
- **Frontend:** Vitest, @testing-library/dom
- **E2E:** Playwright
- **Coverage:** coverage.py, vitest coverage

## Acceptance Criteria

- [ ] All tests pass with >80% coverage
- [ ] CI/CD pipeline runs tests automatically
- [ ] Test failures block deployment
- [ ] Tests run locally with simple commands
- [ ] Documentation for running and writing tests

## Implementation Plan

1. Set up backend testing with pytest
2. Create model and API tests
3. Set up frontend testing with Vitest
4. Implement E2E tests with Playwright
5. Add coverage reporting and CI integration
6. Document testing procedures
