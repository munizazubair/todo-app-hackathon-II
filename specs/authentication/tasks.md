# Authentication & Task Management Implementation Tasks

## Phase II Todo Application - Better Auth + Task Management

**Created:** 2026-01-17
**Status:** READY FOR IMPLEMENTATION
**Based On:** specs/authentication/plan.md (Better Auth approach)
**Supersedes:** Previous JWT-based FastAPI task list (188 tasks)

---

## Overview

This task list implements authentication using **Better Auth** (TypeScript-native) running in Next.js, with FastAPI as a trusted data service. This is a complete redesign from the previous JWT-in-FastAPI approach.

### Architecture Summary

```
Browser → Better Auth Client → Next.js API Routes → Better Auth → Neon PostgreSQL
                                     ↓
                              Todo API Proxy → FastAPI (trusts X-User-ID header)
```

---

## Task Legend

- `[ ]` - Pending
- `[~]` - In Progress
- `[x]` - Completed
- `[!]` - Blocked

**Priority:** P1 (Critical) | P2 (High) | P3 (Medium)

---

## PHASE 1: BETTER AUTH SETUP (Frontend)

### 1.1 Install Dependencies

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T001 | Install `better-auth` package: `npm install better-auth` | P1 | [ ] |
| T002 | Install `@neondatabase/serverless` for Neon PostgreSQL connection: `npm install @neondatabase/serverless` | P1 | [ ] |

### 1.2 Environment Variables

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T003 | Generate secret key: `npx @better-auth/cli@latest secret` | P1 | [ ] |
| T004 | Add `BETTER_AUTH_SECRET` to `.env.local` | P1 | [ ] |
| T005 | Add `BETTER_AUTH_URL=http://localhost:3000` to `.env.local` | P1 | [ ] |
| T006 | Add `NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000` to `.env.local` | P1 | [ ] |
| T007 | Add `DATABASE_URL` (Neon connection string) to `.env.local` | P1 | [ ] |
| T008 | Add `BACKEND_URL=http://localhost:8889` to `.env.local` | P1 | [ ] |

### 1.3 Auth Server Configuration

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T009 | Create `lib/auth.ts` with Better Auth server config | P1 | [ ] |
| T010 | Configure Neon PostgreSQL Pool connection in auth.ts | P1 | [ ] |
| T011 | Enable `emailAndPassword` authentication with `autoSignIn: true` | P1 | [ ] |
| T012 | Configure session settings (7-day expiry, daily refresh) | P2 | [ ] |
| T013 | Add trusted origins (localhost:3000, localhost:3001) | P2 | [ ] |
| T014 | Export Session type for TypeScript usage | P1 | [ ] |

**Reference Code (T009-T014):**
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
    autoSignIn: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Refresh daily
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minute cache
    },
  },
  trustedOrigins: ["http://localhost:3000", "http://localhost:3001"],
});

export type Session = typeof auth.$Infer.Session;
```

### 1.4 Auth Client Configuration

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T015 | Create `lib/auth-client.ts` with Better Auth client config | P1 | [ ] |
| T016 | Export `signIn`, `signUp`, `signOut`, `useSession` from client | P1 | [ ] |

**Reference Code (T015-T016):**
```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### 1.5 API Handler Mount

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T017 | Create directory `app/api/auth/[...all]/` | P1 | [ ] |
| T018 | Create `app/api/auth/[...all]/route.ts` with Better Auth handler | P1 | [ ] |

**Reference Code (T017-T018):**
```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth.handler);
```

### 1.6 Database Schema Migration

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T019 | Run `npx @better-auth/cli@latest generate` to generate schema | P1 | [ ] |
| T020 | Run `npx @better-auth/cli@latest migrate` to apply schema to Neon | P1 | [ ] |
| T021 | Verify tables created: `user`, `session`, `account`, `verification` | P1 | [ ] |

---

## PHASE 2: AUTH UI PAGES (Frontend)

### 2.1 Auth Layout

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T022 | Create `app/(auth)/layout.tsx` for auth pages (centered, minimal) | P1 | [ ] |

**Reference Code (T022):**
```typescript
// app/(auth)/layout.tsx
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full p-6">
        {children}
      </div>
    </div>
  );
}
```

### 2.2 Signup Page

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T023 | Create `app/(auth)/signup/page.tsx` | P1 | [ ] |
| T024 | Build signup form with name, email, password fields | P1 | [ ] |
| T025 | Add client-side validation (email format, password min 8 chars) | P1 | [ ] |
| T026 | Call `authClient.signUp.email()` on form submit | P1 | [ ] |
| T027 | Handle success: redirect to `/dashboard` (auto sign-in enabled) | P1 | [ ] |
| T028 | Handle errors: display error messages (email taken, etc.) | P1 | [ ] |
| T029 | Add "Already have an account? Login" link | P2 | [ ] |
| T030 | Add loading state to submit button | P2 | [ ] |

**Reference Code (T023-T030):**
```typescript
// app/(auth)/signup/page.tsx
"use client";
import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const { data, error: signUpError } = await authClient.signUp.email({
      name,
      email,
      password,
      callbackURL: "/dashboard",
    });

    setLoading(false);

    if (signUpError) {
      setError(signUpError.message || "Signup failed");
      return;
    }

    router.push("/dashboard");
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-center">Create Account</h1>
      {error && <p className="text-red-500 text-center">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full p-3 border rounded"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full p-3 border rounded"
        />
        <input
          type="password"
          placeholder="Password (min 8 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          minLength={8}
          required
          className="w-full p-3 border rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full p-3 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {loading ? "Creating account..." : "Sign Up"}
        </button>
      </form>
      <p className="text-center">
        Already have an account? <Link href="/login" className="text-blue-600">Login</Link>
      </p>
    </div>
  );
}
```

### 2.3 Login Page

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T031 | Create `app/(auth)/login/page.tsx` | P1 | [ ] |
| T032 | Build login form with email, password fields | P1 | [ ] |
| T033 | Call `authClient.signIn.email()` on form submit | P1 | [ ] |
| T034 | Handle success: redirect to `/dashboard` | P1 | [ ] |
| T035 | Handle errors: display error messages (invalid credentials) | P1 | [ ] |
| T036 | Add "Don't have an account? Sign up" link | P2 | [ ] |
| T037 | Add loading state to submit button | P2 | [ ] |

**Reference Code (T031-T037):**
```typescript
// app/(auth)/login/page.tsx
"use client";
import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const { data, error: signInError } = await authClient.signIn.email({
      email,
      password,
      callbackURL: "/dashboard",
    });

    setLoading(false);

    if (signInError) {
      setError(signInError.message || "Invalid credentials");
      return;
    }

    router.push("/dashboard");
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-center">Welcome Back</h1>
      {error && <p className="text-red-500 text-center">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full p-3 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full p-3 border rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full p-3 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {loading ? "Signing in..." : "Sign In"}
        </button>
      </form>
      <p className="text-center">
        Don't have an account? <Link href="/signup" className="text-blue-600">Sign up</Link>
      </p>
    </div>
  );
}
```

---

## PHASE 3: ROUTE PROTECTION (Frontend)

### 3.1 Middleware Protection

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T038 | Create `middleware.ts` in frontend root | P1 | [ ] |
| T039 | Protect `/dashboard` routes (redirect unauthenticated to `/login`) | P1 | [ ] |
| T040 | Redirect authenticated users away from `/login` and `/signup` | P1 | [ ] |

**Reference Code (T038-T040):**
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

### 3.2 Protected Layout

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T041 | Create `app/(protected)/layout.tsx` for protected pages | P1 | [ ] |
| T042 | Move existing dashboard/todo UI into `app/(protected)/dashboard/page.tsx` | P1 | [ ] |

### 3.3 Navigation Updates

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T043 | Update header component to show user email when logged in | P2 | [ ] |
| T044 | Add logout button to header | P1 | [ ] |
| T045 | Implement logout: call `authClient.signOut()` and redirect to `/login` | P1 | [ ] |

**Reference Code (T044-T045):**
```typescript
// In header component
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

const { data: session } = authClient.useSession();
const router = useRouter();

const handleLogout = async () => {
  await authClient.signOut({
    fetchOptions: {
      onSuccess: () => {
        router.push("/login");
      },
    },
  });
};
```

---

## PHASE 4: TODO API PROXY (Frontend)

### 4.1 Authenticated Todo Proxy Routes

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T046 | Update `app/api/todos/route.ts` to validate session via Better Auth | P1 | [ ] |
| T047 | Extract `user.id` from session and pass as `X-User-ID` header to FastAPI | P1 | [ ] |
| T048 | Return 401 if no valid session | P1 | [ ] |
| T049 | Update `app/api/todos/[id]/route.ts` with same auth pattern | P1 | [ ] |
| T050 | Update `app/api/todos/stats/route.ts` with same auth pattern | P1 | [ ] |
| T051 | Update `app/api/todos/[id]/status/route.ts` with same auth pattern | P1 | [ ] |

**Reference Code (T046-T048):**
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

  const { searchParams } = new URL(request.url);
  const queryString = searchParams.toString();
  const url = `${BACKEND_URL}/api/todos/${queryString ? `?${queryString}` : ""}`;

  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      "X-User-ID": session.user.id,
    },
  });

  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
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

  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
```

---

## PHASE 5: BACKEND USER ISOLATION (FastAPI)

### 5.1 User ID Dependency

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T052 | Create/update `core/deps.py` with `get_current_user_from_header` dependency | P1 | [ ] |
| T053 | Read `X-User-ID` header from trusted Next.js proxy | P1 | [ ] |
| T054 | Raise 401 if `X-User-ID` header is missing | P1 | [ ] |

**Reference Code (T052-T054):**
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

### 5.2 Update Todo Routes for User Filtering

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T055 | Add `get_current_user_from_header` dependency to `GET /api/todos` | P1 | [ ] |
| T056 | Filter todos query by `user_id = current_user` | P1 | [ ] |
| T057 | Add dependency to `GET /api/todos/stats` and filter by user | P1 | [ ] |
| T058 | Add dependency to `GET /api/todos/{id}` and verify ownership | P1 | [ ] |
| T059 | Add dependency to `POST /api/todos` and set `user_id = current_user` | P1 | [ ] |
| T060 | Add dependency to `PUT /api/todos/{id}` and verify ownership | P1 | [ ] |
| T061 | Add dependency to `PATCH /api/todos/{id}/status` and verify ownership | P1 | [ ] |
| T062 | Add dependency to `DELETE /api/todos/{id}` and verify ownership | P1 | [ ] |
| T063 | Return 404 (not 403) when accessing another user's todo | P1 | [ ] |

### 5.3 Update Todo Model for Better Auth User ID

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T064 | Change `todos.user_id` type from UUID to TEXT (Better Auth uses TEXT IDs) | P1 | [ ] |
| T065 | Create Alembic migration for user_id type change | P1 | [ ] |
| T066 | Run migration to update todos table | P1 | [ ] |

**Note:** Better Auth creates a `user` table with TEXT `id` field, not UUID. Our `todos.user_id` should reference this.

---

## PHASE 6: TASK MANAGEMENT UI (Frontend)

### 6.1 Dashboard Page

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T067 | Ensure dashboard page displays todos from API (already exists, verify auth) | P1 | [ ] |
| T068 | Verify todo list only shows current user's todos | P1 | [ ] |

### 6.2 Task CRUD Operations

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T069 | **Add Task**: Verify add form calls POST /api/todos | P1 | [ ] |
| T070 | **View Tasks**: Verify list displays with title, category, due date, status | P1 | [ ] |
| T071 | **Update Task**: Verify edit form calls PUT /api/todos/{id} | P1 | [ ] |
| T072 | **Delete Task**: Verify delete button calls DELETE /api/todos/{id} | P1 | [ ] |
| T073 | **Mark Complete**: Verify status toggle calls PATCH /api/todos/{id}/status | P1 | [ ] |

### 6.3 Error Handling

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T074 | Handle 401 responses globally: clear session and redirect to login | P1 | [ ] |
| T075 | Display user-friendly error messages for API failures | P1 | [ ] |

---

## PHASE 7: TESTING & VERIFICATION

### 7.1 Authentication Flow Tests

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T076 | Test: New user can sign up with email/password | P1 | [ ] |
| T077 | Test: Duplicate email shows error | P1 | [ ] |
| T078 | Test: User can sign in with valid credentials | P1 | [ ] |
| T079 | Test: Invalid credentials show error | P1 | [ ] |
| T080 | Test: Session persists on page refresh | P1 | [ ] |
| T081 | Test: Logout clears session and redirects | P1 | [ ] |

### 7.2 Route Protection Tests

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T082 | Test: Unauthenticated users redirected from /dashboard to /login | P1 | [ ] |
| T083 | Test: Authenticated users redirected from /login to /dashboard | P1 | [ ] |

### 7.3 User Isolation Tests

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T084 | Test: User A creates todo, User B cannot see it | P1 | [ ] |
| T085 | Test: User A creates todo, User B cannot update it (404) | P1 | [ ] |
| T086 | Test: User A creates todo, User B cannot delete it (404) | P1 | [ ] |
| T087 | Test: Todo created without session returns 401 | P1 | [ ] |

### 7.4 End-to-End Flow

| ID | Task | Priority | Status |
|----|------|----------|--------|
| T088 | E2E: Sign up → Auto login → Create todo → Mark complete → Delete → Logout | P2 | [ ] |

---

## EXECUTION ORDER

### Stage 1: Better Auth Foundation (T001-T021)
```
T001 → T002 (Install deps)
T003 → T004 → T005 → T006 → T007 → T008 (Env vars)
T009 → T010 → T011 → T012 → T013 → T014 (Auth server)
T015 → T016 (Auth client)
T017 → T018 (API handler)
T019 → T020 → T021 (Database migration)
```

### Stage 2: Auth UI (T022-T037)
```
T022 (Auth layout)
T023 → T024 → T025 → T026 → T027 → T028 → T029 → T030 (Signup)
T031 → T032 → T033 → T034 → T035 → T036 → T037 (Login)
```

### Stage 3: Route Protection (T038-T045)
```
T038 → T039 → T040 (Middleware)
T041 → T042 (Protected layout)
T043 → T044 → T045 (Navigation)
```

### Stage 4: API Proxy Auth (T046-T051)
```
T046 → T047 → T048 (Main todos route)
T049 → T050 → T051 (Other todo routes)
```

### Stage 5: Backend User Isolation (T052-T066)
```
T052 → T053 → T054 (Dependency)
T055 → T056 → T057 → T058 → T059 → T060 → T061 → T062 → T063 (Route updates)
T064 → T065 → T066 (Model migration)
```

### Stage 6: Task Management Verification (T067-T075)
```
T067 → T068 (Dashboard)
T069 → T070 → T071 → T072 → T073 (CRUD)
T074 → T075 (Error handling)
```

### Stage 7: Testing (T076-T088)
```
T076 → T077 → T078 → T079 → T080 → T081 (Auth tests)
T082 → T083 (Route protection tests)
T084 → T085 → T086 → T087 (Isolation tests)
T088 (E2E)
```

---

## SUMMARY

| Phase | Tasks | P1 | P2 |
|-------|-------|----|----|
| 1. Better Auth Setup | 21 | 18 | 3 |
| 2. Auth UI Pages | 16 | 12 | 4 |
| 3. Route Protection | 8 | 6 | 2 |
| 4. API Proxy Auth | 6 | 6 | 0 |
| 5. Backend User Isolation | 15 | 15 | 0 |
| 6. Task Management UI | 9 | 9 | 0 |
| 7. Testing | 13 | 12 | 1 |
| **TOTAL** | **88** | **78** | **10** |

---

## Key Differences from Previous Plan

| Aspect | Previous (188 tasks) | New (88 tasks) |
|--------|---------------------|----------------|
| Auth Location | FastAPI | Next.js (Better Auth) |
| Auth Method | Custom JWT | Better Auth library |
| User Table | SQLModel User | Better Auth `user` table |
| Session Storage | Stateless JWT | Database-backed sessions |
| Backend Auth | JWT validation | Trust X-User-ID header |
| Complexity | High | Low (library handles it) |

---

## Quick Start Commands

```bash
# 1. Install dependencies
cd phase-II/frontend
npm install better-auth @neondatabase/serverless

# 2. Generate secret
npx @better-auth/cli@latest secret

# 3. After creating auth.ts, generate and apply schema
npx @better-auth/cli@latest generate
npx @better-auth/cli@latest migrate

# 4. Start development
npm run dev
```

---

## Files to Create/Modify

### New Files (Frontend)
- `lib/auth.ts` - Better Auth server config
- `lib/auth-client.ts` - Better Auth client
- `app/api/auth/[...all]/route.ts` - Auth API handler
- `app/(auth)/layout.tsx` - Auth pages layout
- `app/(auth)/login/page.tsx` - Login page
- `app/(auth)/signup/page.tsx` - Signup page
- `app/(protected)/layout.tsx` - Protected pages layout
- `app/(protected)/dashboard/page.tsx` - Dashboard (move existing)
- `middleware.ts` - Route protection

### Modified Files (Frontend)
- `.env.local` - Add auth environment variables
- `app/api/todos/route.ts` - Add auth validation
- `app/api/todos/[id]/route.ts` - Add auth validation
- `app/api/todos/stats/route.ts` - Add auth validation
- Header component - Add logout button

### Modified Files (Backend)
- `core/deps.py` - Add user header dependency
- `api/todos.py` - Add user filtering
- `models/todo.py` - Change user_id to TEXT type
- Alembic migration - Update user_id column

---

## NEXT STEPS

1. ✅ Review and approve this task list
2. Begin with Stage 1 (Better Auth Setup)
3. Track progress by updating Status column
4. Create PHR after each completed stage
