# Authentication Implementation Plan (Better Auth)

## Phase II Todo Application - User Authentication with Better Auth

**Author:** System Architect
**Date:** 2026-01-17
**Status:** APPROVED - Ready for Implementation
**Supersedes:** Previous JWT-based FastAPI plan

---

## 1. Executive Summary

This plan redesigns authentication using **Better Auth** - a TypeScript-native authentication framework running in Next.js. This replaces the previous JWT-based FastAPI approach with a cleaner BFF (Backend For Frontend) pattern.

### Architecture Decision

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Auth Framework | Better Auth 2.x | TypeScript-native, battle-tested, handles complexity |
| Auth Location | Next.js API Routes | Same runtime as frontend, simpler deployment |
| Backend Role | Trusted Data Service | FastAPI focuses on business logic, trusts Next.js |
| Database | Neon PostgreSQL (shared) | Better Auth creates its own tables alongside todos |
| Session Type | Database-backed | More secure than stateless JWT for multi-device |

### Why Better Auth over Custom JWT?

1. **Fewer bugs**: Battle-tested auth library vs custom implementation
2. **Security built-in**: bcrypt, CSRF, XSS protection by default
3. **TypeScript-native**: Type-safe auth operations
4. **Maintenance**: Library updates vs maintaining custom code
5. **Hackathon speed**: Faster to implement correctly

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (User)                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────────────────┐ │
│  │ /login  │  │/signup  │  │  /dashboard (protected)     │ │
│  └────┬────┘  └────┬────┘  └─────────────┬───────────────┘ │
│       │            │                      │                 │
│       └────────────┴──────────────────────┘                 │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │ Auth Client │  authClient.signIn()     │
│                    │ (better-auth│  authClient.useSession() │
│                    │  /client)   │  authClient.signOut()    │
│                    └──────┬──────┘                          │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTP (cookies)
                            │
┌───────────────────────────┼─────────────────────────────────┐
│              NEXT.JS SERVER (API Routes)                    │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │      /api/auth/[...all]/route.ts                     │   │
│  │              (Better Auth Handler)                    │   │
│  │                                                       │   │
│  │  Endpoints created automatically:                     │   │
│  │  • POST /api/auth/sign-up/email                      │   │
│  │  • POST /api/auth/sign-in/email                      │   │
│  │  • POST /api/auth/sign-out                           │   │
│  │  • GET  /api/auth/session                            │   │
│  └───────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │         /api/todos/route.ts (Proxy)                  │   │
│  │  1. Validate session via Better Auth                 │   │
│  │  2. Extract user.id from session                     │   │
│  │  3. Forward to FastAPI with X-User-ID header         │   │
│  └───────────────────────┬───────────────────────────────┘   │
│                          │                                 │
│  ┌───────────────────────▼───────────────────────────┐     │
│  │              middleware.ts                         │     │
│  │  • Protects /dashboard/*                          │     │
│  │  • Redirects unauthenticated → /login             │     │
│  │  • Redirects authenticated away from /login       │     │
│  └───────────────────────────────────────────────────┘     │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTP + X-User-ID header
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                  FASTAPI BACKEND                            │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │         Dependency: get_current_user                 │   │
│  │         Reads X-User-ID header from trusted proxy    │   │
│  └───────────────────────┬───────────────────────────────┘   │
│                          │                                 │
│  ┌───────────────────────▼───────────────────────────┐     │
│  │              /api/todos/* routes                   │     │
│  │  • Filters all queries by user_id                 │     │
│  │  • Sets user_id on create                         │     │
│  │  • Verifies ownership on update/delete            │     │
│  └───────────────────────────────────────────────────┘     │
└───────────────────────────┼─────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                  NEON POSTGRESQL                            │
│                           │                                 │
│  ┌─────────────┐    ┌─────▼─────┐    ┌─────────────┐       │
│  │   user      │───<│   todos   │    │  session    │       │
│  │(Better Auth)│ 1:N│  (yours)  │    │(Better Auth)│       │
│  └─────────────┘    └───────────┘    └─────────────┘       │
│                                                             │
│  Tables created by Better Auth: user, session, account,    │
│  verification (we only use user + session)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Implementation Checklist

Reference: `.claude/skills/better-auth/SKILL.md`

### Step 1: Install Package ✅
```bash
cd phase-II/frontend
npm install better-auth @neondatabase/serverless
```

### Step 2: Environment Variables ✅
```env
# .env.local
BETTER_AUTH_SECRET=<32-char-random-secret>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...?sslmode=require
BACKEND_URL=http://localhost:8889
```

### Step 3: Create Auth Server ✅
File: `lib/auth.ts`

### Step 4: Generate Schema ✅
```bash
npx @better-auth/cli generate
```

### Step 5: Mount API Handler ✅
File: `app/api/auth/[...all]/route.ts`

### Step 6: Create Client ✅
File: `lib/auth-client.ts`

### Step 7: Sign-Up/Sign-In UI ✅
Files: `app/(auth)/login/page.tsx`, `app/(auth)/signup/page.tsx`

### Step 8: Session Management ✅
Using `authClient.useSession()` hook

### Step 9: Protected Routes ✅
File: `middleware.ts`

### Step 10: Update API Proxies ✅
Add auth validation to todo proxy routes

### Step 11: Test Flow ✅
Complete auth flow testing

---

## 4. File Structure

```
phase-II/frontend/
├── app/
│   ├── (auth)/                      # Public auth pages
│   │   ├── layout.tsx               # Centered, minimal layout
│   │   ├── login/
│   │   │   └── page.tsx             # Login form
│   │   └── signup/
│   │       └── page.tsx             # Signup form
│   │
│   ├── (protected)/                 # Auth-required pages
│   │   ├── layout.tsx               # Full app layout
│   │   └── dashboard/
│   │       └── page.tsx             # Main todo dashboard
│   │
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...all]/
│   │   │       └── route.ts         # Better Auth catch-all
│   │   └── todos/
│   │       ├── route.ts             # GET/POST with auth
│   │       ├── stats/
│   │       │   └── route.ts         # Stats with auth
│   │       └── [id]/
│   │           ├── route.ts         # GET/PUT/DELETE with auth
│   │           └── status/
│   │               └── route.ts     # PATCH status with auth
│   │
│   ├── layout.tsx                   # Root layout
│   └── page.tsx                     # Landing/redirect
│
├── lib/
│   ├── auth.ts                      # Better Auth server config
│   ├── auth-client.ts               # Better Auth client
│   └── api.ts                       # Existing API utilities
│
├── middleware.ts                    # Route protection
│
├── .env.local                       # Environment variables
└── package.json
```

---

## 5. Implementation Details

### 5.1 Auth Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "@neondatabase/serverless";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,         // Auto sign-in after signup
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days
    updateAge: 60 * 60 * 24,       // Refresh daily
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5,              // 5 minute cache
    },
  },
  trustedOrigins: ["http://localhost:3000", "http://localhost:3001"],
});

export type Session = typeof auth.$Infer.Session;
```

### 5.2 Auth Client Configuration

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### 5.3 API Handler

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

### 5.4 Middleware Protection

```typescript
// middleware.ts
import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const { pathname } = request.nextUrl;
  const isAuthPage = pathname.startsWith("/login") || pathname.startsWith("/signup");
  const isProtectedRoute = pathname.startsWith("/dashboard");

  // Redirect authenticated users away from auth pages
  if (session && isAuthPage) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Redirect unauthenticated users to login
  if (!session && isProtectedRoute) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/signup"],
};
```

### 5.5 Todo Proxy with Auth

```typescript
// app/api/todos/route.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8889";

async function getSession(request: NextRequest) {
  return auth.api.getSession({ headers: request.headers });
}

export async function GET(request: NextRequest) {
  const session = await getSession(request);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const response = await fetch(`${BACKEND_URL}/api/todos/`, {
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": session.user.id,
    },
  });

  return NextResponse.json(await response.json());
}

export async function POST(request: NextRequest) {
  const session = await getSession(request);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const response = await fetch(`${BACKEND_URL}/api/todos/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": session.user.id,
    },
    body: JSON.stringify(body),
  });

  return NextResponse.json(await response.json(), { status: response.status });
}
```

### 5.6 FastAPI User Dependency

```python
# core/deps.py
from fastapi import Header, HTTPException
from typing import Optional

async def get_current_user_from_header(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
) -> str:
    """Get user ID from trusted Next.js proxy header."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return x_user_id
```

---

## 6. Database Schema

Better Auth will create these tables automatically:

```sql
-- Created by: npx @better-auth/cli generate

CREATE TABLE "user" (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT false,
    name TEXT,
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE "session" (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE "account" (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    account_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    -- OAuth fields (not used for email/password)
    access_token TEXT,
    refresh_token TEXT,
    UNIQUE(provider_id, account_id)
);

CREATE TABLE "verification" (
    id TEXT PRIMARY KEY,
    identifier TEXT NOT NULL,
    value TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(identifier, value)
);
```

**Your existing `todos` table** keeps `user_id` but references Better Auth's `user.id`:

```sql
-- Existing todos table modification
ALTER TABLE todos ADD COLUMN user_id TEXT REFERENCES "user"(id);
CREATE INDEX idx_todos_user_id ON todos(user_id);
```

---

## 7. Environment Variables

### Frontend (.env.local)

```env
# Better Auth (required)
BETTER_AUTH_SECRET=generate-a-32-char-random-string-here
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# Database (Better Auth uses this)
DATABASE_URL=postgresql://neondb_owner:xxx@host/db?sslmode=require

# Backend proxy
BACKEND_URL=http://localhost:8889
```

### Backend (.env)

```env
# Existing
DATABASE_URL=postgresql://neondb_owner:xxx@host/db?sslmode=require
API_HOST=0.0.0.0
API_PORT=8889
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
ENVIRONMENT=development

# Auth is now handled by Next.js, no JWT config needed
```

---

## 8. Testing Checklist

- [ ] **Signup**: New user can create account
- [ ] **Duplicate email**: Shows error for existing email
- [ ] **Login**: Valid credentials create session
- [ ] **Invalid login**: Shows error message
- [ ] **Session persistence**: Refreshing page keeps user logged in
- [ ] **Logout**: Clears session, redirects to login
- [ ] **Protected routes**: Unauthenticated users redirected to login
- [ ] **Auth pages**: Authenticated users redirected to dashboard
- [ ] **Todo isolation**: Users only see their own todos
- [ ] **Create todo**: New todo assigned to current user
- [ ] **Update/Delete**: Can only modify own todos

---

## 9. Migration from Previous Plan

The previous plan implemented JWT auth on FastAPI. To switch to Better Auth:

1. **Remove** FastAPI auth routes (`/auth/*`)
2. **Remove** JWT utilities from backend
3. **Keep** `user_id` column on todos
4. **Update** FastAPI to trust `X-User-ID` header
5. **Generate** Better Auth schema (creates new user table)
6. **Migrate** existing users if needed (or start fresh for hackathon)

---

## 10. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Better Auth schema conflicts | Use fresh DB or prefix tables |
| User ID type mismatch | Better Auth uses TEXT, ensure todos.user_id matches |
| CORS issues | Same-origin by default (localhost:3000) |
| Session not persisting | Check cookie settings, verify HTTPS in production |

---

## 11. Success Criteria

### Must Have
- [x] Users can sign up with email/password
- [x] Users can sign in and get session
- [x] Users can sign out
- [x] Protected routes redirect unauthenticated users
- [x] Each user sees only their own todos
- [x] Todos created with correct user_id

### Nice to Have (Post-Hackathon)
- [ ] Email verification
- [ ] Password reset
- [ ] Rate limiting
- [ ] Multiple sessions view

---

**Plan Version**: 2.0.0 (Better Auth)
**Created**: 2026-01-17
**Author**: Claude (sp.plan)
