# Tasks: Phase II Full-Stack Web Application - Bug Fixes & Completion

**Input**: Design documents from `/specs/002-phase-ii-web-app/`
**Feature Branch**: `002-phase-ii-web-app`
**Status**: 🔴 CRITICAL BUGS - Immediate Fix Required

## Critical Issues Identified

1. **Frontend Styling Broken**: Tailwind CSS and Framer Motion not rendering properly (raw HTML appearance)
2. **Backend Connection Failed**: Frontend displays "Failed to load todos" - API connectivity issue
3. **CORS Configuration**: Frontend (port 3002) not allowed in backend CORS origins (configured for 3000)

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, etc.) for feature work
- Include exact file paths

---

## Phase 1: Critical Bug Fixes (IMMEDIATE)

**Purpose**: Fix broken styling and API connectivity

### Issue 1: Frontend Styling Not Rendering

- [X] T001 Verify Tailwind CSS PostCSS configuration in phase-II/frontend/postcss.config.js
- [X] T002 Check Next.js configuration in phase-II/frontend/next.config.js for CSS handling
- [X] T003 Verify globals.css is imported in phase-II/frontend/app/layout.tsx
- [X] T004 Check if node_modules are installed - run npm install in phase-II/frontend/
- [X] T005 Clear Next.js cache - delete .next directory and rebuild
- [X] T006 Verify Framer Motion is installed in package.json dependencies
- [X] T007 Test Tailwind class generation - check if .next/static/css files exist

### Issue 2: Backend API Connection Failed

- [X] T008 Update CORS_ORIGINS in phase-II/backend/core/config.py to include http://localhost:3002
- [X] T009 Create/update .env file with correct CORS_ORIGINS
- [X] T010 Verify DATABASE_URL is set correctly in .env with Neon DB connection string
- [X] T011 Restart backend server to apply new CORS configuration
- [X] T012 Test API health endpoint: curl http://localhost:8889/health
- [X] T013 Test API todos endpoint: curl http://localhost:8889/api/todos/
- [X] T014 Update API_BASE_URL in phase-II/frontend/lib/constants.ts to match backend port (8889)

**Checkpoint**: After these fixes, styling should render and API should connect

---

## Success Criteria

✅ **Immediate Success** (MVP):
- Tailwind CSS and Framer Motion render correctly (no raw HTML)
- Frontend connects to backend API successfully
- Database connection established
- Can create, view, update, delete todos

---

**Document Version**: 2.0 (Bug Fix & Completion)
**Last Updated**: 2026-01-13
**Author**: Claude Sonnet 4.5
**Status**: Ready for Execution
