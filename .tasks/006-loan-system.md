#006 — Add loan/borrow functionality

## Overview

Implement the complete loan/borrow system allowing students to borrow books and librarians to manage loan transactions.

## Requirements

### Backend Loan Management

- [ ] Create loan creation endpoint with book availability checking
- [ ] Implement loan return functionality
- [ ] Add loan status tracking (borrowed, returned, overdue)
- [ ] Create overdue loan detection and notifications
- [ ] Add loan history and reporting

### Frontend Loan Interface

- [ ] Create loan request form for students
- [ ] Add loan management interface for librarians
- [ ] Implement loan status display and filtering
- [ ] Add return book functionality
- [ ] Create loan history views

### Business Logic

- [ ] Prevent borrowing when book unavailable
- [ ] Auto-calculate due dates (14 days default)
- [ ] Handle overdue loans with penalties
- [ ] Update book availability when loans change
- [ ] Role-based access (students can only see their loans)

## Technical Details

### New API Endpoints

```
POST /api/loans/ - Create new loan (borrow book)
POST /api/loans/{id}/return/ - Return a book
GET /api/loans/my-loans/ - Get current user's loans
GET /api/loans/overdue/ - Get overdue loans (librarian only)
```

### Database Updates

- Ensure loan model has all required fields
- Add constraints for data integrity
- Consider adding loan policies table

### Frontend Updates

- Add loan section to navigation
- Create loan request modal/form
- Add loan status indicators
- Implement loan filtering and search

## Acceptance Criteria

- [ ] Students can request to borrow available books
- [ ] Librarians can approve/deny loan requests
- [ ] Books show correct availability status
- [ ] Loan due dates are properly calculated
- [ ] Overdue loans are highlighted
- [ ] Users can return books through the interface
- [ ] Loan history is maintained and accessible

## Testing

- [ ] Test loan creation with availability checking
- [ ] Test return functionality
- [ ] Test overdue detection
- [ ] Test role-based access to loan management
