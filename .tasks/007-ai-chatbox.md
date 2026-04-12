# Task #007: Integrate AI Chatbox for Book Recommendations

**Type**: Feature
**Area**: Frontend/Backend Integration  
**Status**: In Progress
**Assigned to**: @frontend-developer (primary), @backend-developer (API support)

---

## Overview

Add an AI-powered chatbot to the digital library that helps students discover book recommendations based on their interests, academic major, and reading preferences.

---

## Acceptance Criteria

1. **Chatbox UI Component**
   - [ ] Floating chat widget visible on all pages
   - [ ] Expandable/collapsible modal window
   - [ ] Message display with user and bot responses
   - [ ] Text input field with send button
   - [ ] Mobile-responsive design

2. **Backend Chatbot Logic**
   - [ ] `/api/chat/recommend/` endpoint for bookmark recommendations
   - [ ] Integration with book database to provide relevant suggestions
   - [ ] Simple recommendation algorithm (category match, rating-based, etc.)
   - [ ] Response rate-limiting to prevent abuse

3. **Recommendation Features**
   - [ ] Bot can suggest books by category/genre
   - [ ] Bot can suggest books by difficulty level
   - [ ] Bot can suggest books by user ratings
   - [ ] Bot responses include book title, author, and brief description

4. **Testing**
   - [ ] Unit tests for recommendation algorithm
   - [ ] API endpoint tests
   - [ ] UI component tests (basic interaction)
   - [ ] Minimum 70% code coverage for chatbox code

5. **Documentation**
   - [ ] Update user guide with chatbox usage
   - [ ] Document recommendation algorithm
   - [ ] Add API endpoint documentation

---

## Technical Details

### Frontend Implementation
- Vue/vanilla JavaScript chatbox component
- Store chat history in localStorage
- WebSocket or REST API for real-time chat

### Backend Implementation
- Django REST Framework endpoint
- Simple rule-based recommendation engine
- (Optional: Later integrate with actual LLM like GPT/Claude)

### API Endpoint
```
POST /api/chat/recommend/
Request: { "query": "books about machine learning", "user_id": 1 }
Response: { "suggestions": [...], "message": "..." }
```

---

## Notes

- v1 uses rule-based recommendations, not actual AI/LLM
- Keep scope minimal for initial release
- Focus on UX of the chatbox component
- Can integrate with real LLM later (post-v1)

---

## Related Tasks
- #004 — Frontend books
- #003 — Backend API
