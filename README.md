# Bug Tracker
A minimal in-memory bug tracker with a Flask API and React + TypeScript client.

## Features
Create, list, filter, paginate, update status, and delete bugs. Titles and severities are validated.

## How to Run
```bash
pip install flask pytest && pytest backend/test_app.py
python backend/app.py
```

## Tests & Edge Cases
1. Create a bug
2. Reject an empty title
3. Reject an invalid severity
4. Filter and paginate the list
5. Handle an invalid page
6. Update status and delete a bug

## RL TASKS FROM THIS REPO
- **Task 1: Fix Pagination Race** — Rubric: Correctness 40%, Edge 30%, Quality 30%
- **Task 2: Add Validation** — Rubric: Correctness 50%, Security 30%, Errors 20%
- **Task 3: Fix Brittle Error Handling** — Rubric: Correctness 40%, Error Handling 40%, Maintainability 20%
