# Backend-dev-plan.md, Template & Rules

This is the authoritative template for the `Backend-dev-plan.md` document this skill
produces. Follow it exactly, do not invent a different structure, and check whether a
conditional section is actually required before including it.

## Hard constraints (must follow exactly)
- Backend: FastAPI (Python 3.13, async)
- Database: MongoDB Atlas only, no local instance, using Motor and Pydantic v2 models
- No Docker
- Include only features explicitly visible or required in the frontend/PRD
- Background tasks: synchronous by default; use FastAPI `BackgroundTasks` only if
  strictly necessary (no Celery, no queues)
- Manual testing required after every task, not just after sprints
- Git workflow: a single `main` branch only
- API base path: `/api/v1/*`
- Pagination: only if the frontend actually shows pagination controls
- Use inline sensible defaults for anything unspecified rather than stalling

## Output rules
- Output only one markdown file: `Backend-dev-plan.md`
- Bullets only, no tables or paragraphs
- Omit any section or feature not visible in / required by the frontend
- Every task must include:
  - **Manual Test Step**, the exact frontend action + expected result
  - **User Test Prompt**, a copy-paste-friendly instruction the user can hand to
    whoever is testing

## Document structure

### 1. Executive Summary
- What will be built and why
- Mention the constraints (FastAPI 3.13, MongoDB Atlas, no Docker, per-task testing,
  single-branch git)
- State the (dynamic) number of sprints needed to cover all frontend features

### 2. In-Scope & Success Criteria
- Bullet every frontend feature in scope
- Success Criteria: all frontend features functional end-to-end; all task-level tests
  pass via the UI; each sprint's code pushed to `main` after verification

### 3. API Design
- Base path: `/api/v1`; filtering/sorting only if visible in the UI
- Error envelope: `{"error": "message"}`
- For each endpoint: method + path, purpose, minimal request/response shape,
  validation notes

### 4. Data Model (MongoDB Atlas)
- List every collection with: fields (name, type, required/default), embedded vs.
  referenced (only if the UI depends on it), one short example JSON document
- No index discussion

### 5. Frontend Audit & Feature Map
- For each screen/component: route/component name, purpose & data needed, required
  endpoint(s) + model(s), auth requirement (if any), optional notes

### 6. Configuration & ENV Vars (core only)
- `APP_ENV`, environment (development, production)
- `PORT`, HTTP port (e.g. 8000)
- `MONGODB_URI`, MongoDB Atlas connection string
- `JWT_SECRET`, token signing key
- `JWT_EXPIRES_IN`, seconds before JWT expiry
- `CORS_ORIGINS`, allowed frontend URL(s)

### 7. Background Work (only if required, omit otherwise)
- Trigger, purpose, and idempotency
- How the UI checks completion (e.g. a status field or a polling endpoint)

### 8. Integrations (only if required, omit otherwise)
- List real integrations only (file uploads, payments, etc.)
- Minimal flow + any extra env vars needed

### 9. Testing Strategy (manual via frontend only)
- Validation happens only through the frontend UI, no automated test suite
- Every task includes a Manual Test Step + a User Test Prompt (see Output rules)
- After all tasks in a sprint pass: commit and push to `main`
- If any task fails: fix and retest before pushing

### 10. Dynamic Sprint Plan & Backlog (S0 → Sn)
- Create as many sprints as needed to cover every in-scope feature
- Each sprint includes: Objectives, User Stories, Tasks (each with Manual Test Step +
  User Test Prompt), Definition of Done, and a post-sprint push to `main`

## Sprint S0, Environment Setup & Frontend Connection (always included)
**Objectives:**
- Create the FastAPI skeleton with `/api/v1` and `/healthz`
- Connect to MongoDB Atlas using `MONGODB_URI`
- `/healthz` performs a DB ping and returns a JSON status
- Enable CORS for the frontend
- Replace the dummy API URLs in the frontend with the real backend URLs
- Initialize git only once, at the project root, default branch `main`, push to GitHub
- Create a single root `.gitignore` (ignore `__pycache__`, `.env`, `*.pyc`, etc.)

**Definition of Done:**
- Backend runs locally and connects to MongoDB Atlas
- `/healthz` returns success; frontend renders live data
- Repo is live on GitHub, `main` branch

**Manual Test Step:** Run the backend, open the frontend, check Network → `/healthz` →
200 OK with DB status.
**User Test Prompt:** "Start the backend and refresh the app. Confirm that the status
shows a successful DB connection."

## Sprint S1, Basic Auth (Signup / Login / Logout), worked example
**Objectives:**
- Implement JWT-based signup, login, and logout
- Protect one backend route + one frontend page

**Endpoints:**
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- (Optional) `GET /api/v1/auth/me`

**Tasks:**
- Store user in MongoDB (hashed password via Argon2)
  - Manual Test Step: Sign up via the UI → success message visible
  - User Test Prompt: "Create a new account and verify the confirmation."
- Implement login issuing a JWT
  - Manual Test Step: Log in → token saved → redirected to dashboard
  - User Test Prompt: "Log in and confirm redirection to the dashboard."
- Implement logout (clear client token)
  - Manual Test Step: Click logout → protected pages blocked
  - User Test Prompt: "After logout, refresh a protected page, it should redirect to
    login."

**Definition of Done:** Auth flow works end-to-end in the frontend.
**Post-sprint:** Commit and push to `main`.

## Sprints S2 → Sn, Remaining Feature Sprints
- One sprint per major frontend feature still uncovered
- Each follows the same pattern: Objectives, User Stories, Tasks (each with Manual
  Test Step + User Test Prompt), Definition of Done, post-sprint push to `main`

## Style & compliance checklist (verify before finishing)
- [ ] Bullets only, no tables or prose
- [ ] Only visible frontend features mentioned
- [ ] APIs/models are minimal and aligned with the UI
- [ ] MongoDB Atlas only; Python 3.13 runtime
- [ ] Every task has its own Manual Test Step + User Test Prompt
- [ ] The plan document itself ends after all sprints are defined, "commit & push to
      main" is the last *described* action per sprint, not an instruction for this
      skill to actually start coding
