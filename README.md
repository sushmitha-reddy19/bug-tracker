# Bug Tracker - Production-Style Issue Tracking System

Full-stack bug tracker built to model real production SWE work - auth, CRUD, pagination, validation, error handling.

## Features

- Mock-token login without a real database.
- Create bugs with title, description, severity, and status.
- List bugs with pagination at 10 items per page.
- Filter bugs by severity and status.
- Update status or description and delete bugs.
- Handles empty titles, invalid severity values, empty list states, invalid page numbers, and expired authentication tokens.

## Architecture

React + TypeScript frontend -> Python FastAPI backend -> in-memory bug store. The in-memory store keeps this repository small and makes it suitable for demo and benchmark tasks.

## How to Run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Tests & Edge Cases Covered

- Test create bug success.
- Test create bug fails with empty title.
- Test create bug fails with invalid severity.
- Test pagination returns the correct page.
- Test pagination with an invalid page returns a validation error.
- Test filtering by severity works.
- Test updating a non-existent bug returns 404.
- Test deleting a bug works.
- Test expired authentication returns 401.
- Empty list state is represented by an explicit UI message.

## RL TASK IDEAS DERIVED FROM THIS REPO

### Task 1: Fix Race Condition in Pagination

**Prompt:** When a user clicks the next page quickly, duplicate bugs appear.

**Tests:** Pagination test and repeated page-request test.

**Rubric:** Correctness 40%, Edge Cases 30%, Code Quality 30%.

### Task 2: Add Validation for Bug Creation

**Prompt:** Reject empty title, invalid severity, and XSS input.

**Tests:** Validation tests and sanitization test.

**Rubric:** Correctness 50%, Security 30%, Error Messages 20%.

### Task 3: Refactor Brittle API Handler

**Prompt:** The current handler crashes on 404 and auth expiry.

**Tests:** Error-handling tests for missing bugs and expired tokens.

**Rubric:** Correctness 40%, Error Handling 40%, Maintainability 20%.

## Tech Stack

Python, FastAPI, React, TypeScript, Vite, pytest.

## Limitations

Mock auth, no real database, and in-memory storage. This repository is for demo and benchmark use.
