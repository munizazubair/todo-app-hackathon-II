---
id: 0001
title: Better Auth Plan Redesign
stage: plan
date: 2026-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: authentication
branch: 001-animated-ui-storytelling
user: SIBGHAT
command: /sp.plan
labels: ["authentication", "better-auth", "next.js", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/authentication/plan.md
  - .claude/skills/better-auth/SKILL.md
tests:
  - null
---

## Prompt

redesign the authentication plan with better auth You are implementing authentication using Better Auth for a Next.js + FastAPI project.

Rules:
- Prefer MCP queries to Better Auth whenever available.
- Follow Better Auth official patterns and APIs exactly.
- Use skill.md as a checklist and execution guide, not a source of truth.
- Do NOT invent APIs, plugins, or features.
- Target: Email & Password authentication only (no OAuth, no 2FA, no Passkeys).
- Focus on completing only what is needed for hackathon Phase II.

Context:
- Phase I and Phase II CRUD features are complete.
- The only remaining part is authentication.
- Database is already configured with users and tasks tables.

Task:
Plan the authentication step-by-step for the project:
1. Outline the **server setup** (Better Auth + FastAPI integration).
2. Outline the **frontend setup** (Better Auth client in Next.js).
3. Show how to **sign up, sign in, and maintain sessions**.
4. Include **middleware / route protection**.
5. Reference skill.md checklist where relevant.
6. Explain each step **briefly and safely**, so I can implement it immediately.

Constraints:
- Keep it simple and hackathon-friendly.
- Only implement what is required to get email/password auth fully working.
- Explain any critical environment variables or configuration needed.

## Response snapshot

Created comprehensive authentication plan using Better Auth with BFF (Backend For Frontend) architecture:

**Key Architecture Decision**: Better Auth runs in Next.js API routes, FastAPI becomes a trusted backend that receives user context via X-User-ID header.

**Plan Highlights**:
1. Install better-auth + @neondatabase/serverless in frontend
2. Create auth server config (lib/auth.ts) with Neon Pool adapter
3. Generate database schema via CLI (npx @better-auth/cli generate)
4. Mount catch-all handler at /api/auth/[...all]/route.ts
5. Create auth client (lib/auth-client.ts) for frontend hooks
6. Build login/signup pages using authClient.signIn.email / signUp.email
7. Add middleware.ts for route protection
8. Update todo proxy routes to validate session and pass X-User-ID to FastAPI
9. Simplify FastAPI to trust proxy headers instead of JWT validation

**Files Created/Updated**:
- specs/authentication/plan.md (v2.0.0 - Better Auth)

## Outcome

- ✅ Impact: Redesigned auth architecture from custom JWT to Better Auth
- 🧪 Tests: Checklist defined in plan section 8
- 📁 Files: 1 plan updated (specs/authentication/plan.md)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Better Auth significantly simplifies auth compared to custom JWT; BFF pattern cleanly separates concerns

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generation successful
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): Standard sp.plan with Better Auth skill context
- Next experiment (smallest change to try): Implement Step 1 (install packages) and verify Better Auth imports work
