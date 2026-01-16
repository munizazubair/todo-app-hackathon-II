# Authentication Implementation Plan

## Phase 2 Todo Application - User Authentication

**Author:** System Architect
**Date:** 2026-01-16
**Status:** DRAFT - Pending Approval

---

## 1. Executive Summary

This plan outlines the implementation of JWT-based user authentication for the Phase 2 Todo application. The goal is to transform the current single-user MVP into a secure multi-user application where each user can only access and manage their own tasks.

### Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Method | Email + Password | Simple, universal, no third-party dependency |
| Password Storage | bcrypt hash | Industry standard, resistant to rainbow tables |
| Token Type | JWT (stateless) | Scalable, backend remains stateless |
| Token Delivery | Authorization header (Bearer) | RESTful standard, works with API proxies |
| Token Storage (FE) | HTTP-only cookie | XSS protection, automatic inclusion |
| User ID Type | UUID | Non-sequential, prevents enumeration attacks |

---

## 2. Architecture Overview

### 2.1 High-Level Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

  SIGN UP FLOW:
  ─────────────
  User → [Sign Up Form] → POST /auth/signup → [Validate Email Unique]
                                            → [Hash Password (bcrypt)]
                                            → [Create User Record]
                                            → [Return Success]
                                            → [Redirect to Login]

  SIGN IN FLOW:
  ─────────────
  User → [Login Form] → POST /auth/login → [Find User by Email]
                                         → [Verify Password (bcrypt)]
                                         → [Generate JWT Token]
                                         → [Set HTTP-only Cookie]
                                         → [Return User Info]
                                         → [Redirect to Dashboard]

  AUTHENTICATED REQUEST FLOW:
  ───────────────────────────
  User → [Any Todo Action] → [Request with Cookie/Bearer Token]
                           → [JWT Validation Middleware]
                           → [Extract user_id from Token]
                           → [Query filtered by user_id]
                           → [Return User's Data Only]

  LOGOUT FLOW:
  ────────────
  User → [Logout Button] → POST /auth/logout → [Clear HTTP-only Cookie]
                                             → [Redirect to Login]
```

### 2.2 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Next.js)                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  /login     │  │  /signup    │  │  /dashboard │  │  /tasks     │      │
│  │  (public)   │  │  (public)   │  │ (protected) │  │ (protected) │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │                │              │
│         └────────────────┴────────────────┴────────────────┘              │
│                                   │                                       │
│                    ┌──────────────┴──────────────┐                        │
│                    │     Auth Context Provider    │                        │
│                    │  - user state               │                        │
│                    │  - isAuthenticated          │                        │
│                    │  - login/logout methods     │                        │
│                    └──────────────┬──────────────┘                        │
│                                   │                                       │
│                    ┌──────────────┴──────────────┐                        │
│                    │   Next.js API Routes        │                        │
│                    │   (Proxy + Cookie Handler)  │                        │
│                    └──────────────┬──────────────┘                        │
└───────────────────────────────────┼───────────────────────────────────────┘
                                    │
                          HTTP (with cookies)
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                           BACKEND (FastAPI)                               │
│                                   │                                       │
│                    ┌──────────────┴──────────────┐                        │
│                    │      Auth Middleware        │                        │
│                    │  - JWT validation           │                        │
│                    │  - User extraction          │                        │
│                    └──────────────┬──────────────┘                        │
│                                   │                                       │
│         ┌─────────────────────────┼─────────────────────────┐            │
│         │                         │                         │            │
│  ┌──────┴──────┐          ┌───────┴───────┐         ┌───────┴───────┐    │
│  │ Auth Routes │          │  Todo Routes  │         │ User Routes   │    │
│  │ /auth/*     │          │  /api/todos/* │         │ /api/users/*  │    │
│  │ (public)    │          │  (protected)  │         │ (protected)   │    │
│  └──────┬──────┘          └───────┬───────┘         └───────┬───────┘    │
│         │                         │                         │            │
│         └─────────────────────────┼─────────────────────────┘            │
│                                   │                                       │
│                    ┌──────────────┴──────────────┐                        │
│                    │     SQLModel ORM Layer      │                        │
│                    └──────────────┬──────────────┘                        │
└───────────────────────────────────┼───────────────────────────────────────┘
                                    │
                              PostgreSQL
                                    │
┌───────────────────────────────────┼───────────────────────────────────────┐
│                         DATABASE (Neon)                                   │
│                                   │                                       │
│         ┌─────────────────────────┼─────────────────────────┐            │
│         │                         │                         │            │
│  ┌──────┴──────┐          ┌───────┴───────┐                             │
│  │   users     │──────────│    todos      │                             │
│  │             │  1:N     │               │                             │
│  │ id (UUID)   │──────────│ user_id (FK)  │                             │
│  │ email       │          │ id            │                             │
│  │ password    │          │ title         │                             │
│  │ created_at  │          │ status        │                             │
│  └─────────────┘          │ ...           │                             │
│                           └───────────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema Design

### 3.1 Users Table

```
TABLE: users
─────────────────────────────────────────────────────────────────
Column          │ Type                │ Constraints
─────────────────────────────────────────────────────────────────
id              │ UUID                │ PRIMARY KEY, DEFAULT uuid_generate_v4()
email           │ VARCHAR(255)        │ UNIQUE, NOT NULL, INDEX
hashed_password │ VARCHAR(255)        │ NOT NULL
created_at      │ TIMESTAMP WITH TZ   │ NOT NULL, DEFAULT NOW()
updated_at      │ TIMESTAMP WITH TZ   │ NOT NULL, DEFAULT NOW()
─────────────────────────────────────────────────────────────────

INDEXES:
  - users_email_idx ON users(email) -- for login lookup
```

### 3.2 Modified Todos Table

```
TABLE: todos (MODIFIED)
─────────────────────────────────────────────────────────────────
Column          │ Type                │ Constraints
─────────────────────────────────────────────────────────────────
id              │ INTEGER             │ PRIMARY KEY, AUTO INCREMENT
user_id         │ UUID                │ NOT NULL, FOREIGN KEY → users(id)
title           │ VARCHAR(500)        │ NOT NULL
category        │ VARCHAR(50)         │ NULLABLE
due_date        │ DATE                │ NULLABLE
status          │ VARCHAR(20)         │ NOT NULL, DEFAULT 'pending'
created_at      │ TIMESTAMP WITH TZ   │ NOT NULL, DEFAULT NOW()
updated_at      │ TIMESTAMP WITH TZ   │ NOT NULL, DEFAULT NOW()
version         │ INTEGER             │ NOT NULL, DEFAULT 1
─────────────────────────────────────────────────────────────────

NEW INDEXES:
  - todos_user_id_idx ON todos(user_id) -- for user filtering
  - todos_user_status_idx ON todos(user_id, status) -- for filtered queries

FOREIGN KEY:
  - user_id REFERENCES users(id) ON DELETE CASCADE
```

### 3.3 Entity Relationship

```
┌─────────────┐          ┌─────────────┐
│   users     │          │   todos     │
├─────────────┤          ├─────────────┤
│ id (PK)     │─────────<│ user_id(FK) │
│ email       │    1:N   │ id (PK)     │
│ hashed_pwd  │          │ title       │
│ created_at  │          │ status      │
│ updated_at  │          │ ...         │
└─────────────┘          └─────────────┘

Relationship: One User → Many Todos
Cascade: DELETE user → DELETE all user's todos
```

---

## 4. Backend API Design

### 4.1 Authentication Routes (Public)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AUTH ROUTES (/auth)                               │
└─────────────────────────────────────────────────────────────────────────┘

POST /auth/signup
─────────────────
Request Body:
  {
    "email": "user@example.com",
    "password": "SecurePass123!"
  }

Validation:
  - Email: valid format, unique in database
  - Password: minimum 8 characters

Success Response (201 Created):
  {
    "message": "User created successfully",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "created_at": "2026-01-16T12:00:00Z"
    }
  }

Error Responses:
  - 400: Invalid email format
  - 400: Password too weak
  - 409: Email already registered


POST /auth/login
────────────────
Request Body:
  {
    "email": "user@example.com",
    "password": "SecurePass123!"
  }

Success Response (200 OK):
  Headers:
    Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Lax; Path=/

  Body:
  {
    "message": "Login successful",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com"
    }
  }

Error Responses:
  - 401: Invalid email or password


POST /auth/logout
─────────────────
Success Response (200 OK):
  Headers:
    Set-Cookie: access_token=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0

  Body:
  {
    "message": "Logged out successfully"
  }


GET /auth/me
────────────
(Requires Authentication)

Success Response (200 OK):
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-01-16T12:00:00Z"
  }

Error Response:
  - 401: Not authenticated
```

### 4.2 Protected Todo Routes (Modified)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   TODO ROUTES (/api/todos) - ALL PROTECTED               │
└─────────────────────────────────────────────────────────────────────────┘

All routes now require authentication and filter by user_id.

GET /api/todos
──────────────
- Automatically filters: WHERE user_id = <authenticated_user_id>
- Response contains ONLY the authenticated user's todos

GET /api/todos/stats
────────────────────
- Statistics calculated ONLY for authenticated user's todos
- Response: { total, pending, completed, overdue } for current user

POST /api/todos
───────────────
- Automatically sets: user_id = <authenticated_user_id>
- User cannot create todos for other users

GET /api/todos/{id}
───────────────────
- Returns 404 if todo belongs to different user
- Prevents information leakage

PUT /api/todos/{id}
───────────────────
- Verifies: todo.user_id == authenticated_user_id
- Returns 404 if not owner (not 403, to prevent enumeration)

PATCH /api/todos/{id}/status
────────────────────────────
- Verifies ownership before status update

DELETE /api/todos/{id}
──────────────────────
- Verifies ownership before deletion
- Returns 404 if not owner
```

### 4.3 Authentication Dependency Flow

```
REQUEST LIFECYCLE WITH AUTH:
───────────────────────────

1. Request arrives at protected endpoint
                │
                ▼
2. Auth dependency extracts token
   - Check Authorization header (Bearer token)
   - OR check access_token cookie
                │
                ▼
3. JWT validation
   - Verify signature with SECRET_KEY
   - Check expiration (exp claim)
   - Extract user_id from payload
                │
                ▼
4. User lookup (optional, for full user object)
   - Query users WHERE id = token.user_id
   - Return 401 if user not found
                │
                ▼
5. Inject current_user into route handler
                │
                ▼
6. Route handler uses current_user.id
   - Filter queries: WHERE user_id = current_user.id
   - Verify ownership for updates/deletes
```

---

## 5. Frontend Architecture

### 5.1 New Pages Structure

```
app/
├── (auth)/                    # Auth route group (public)
│   ├── layout.tsx            # Auth pages layout (centered, no nav)
│   ├── login/
│   │   └── page.tsx          # Login form
│   └── signup/
│       └── page.tsx          # Sign up form
│
├── (protected)/               # Protected route group
│   ├── layout.tsx            # Requires authentication
│   ├── page.tsx              # Main dashboard (current page.tsx)
│   └── tasks/
│       └── page.tsx          # Task management
│
├── api/
│   ├── auth/
│   │   ├── login/route.ts    # Proxy to backend /auth/login
│   │   ├── signup/route.ts   # Proxy to backend /auth/signup
│   │   ├── logout/route.ts   # Proxy to backend /auth/logout
│   │   └── me/route.ts       # Proxy to backend /auth/me
│   └── todos/                # Existing proxies (now protected)
│       └── ...
│
└── layout.tsx                 # Root layout with AuthProvider
```

### 5.2 Authentication Context

```
AUTH CONTEXT STRUCTURE:
──────────────────────

AuthProvider (wraps entire app)
│
├── State:
│   ├── user: User | null
│   ├── isAuthenticated: boolean
│   ├── isLoading: boolean
│   └── error: string | null
│
├── Methods:
│   ├── login(email, password) → Promise<void>
│   ├── signup(email, password) → Promise<void>
│   ├── logout() → Promise<void>
│   └── checkAuth() → Promise<void>
│
└── Effects:
    └── On mount: checkAuth() to restore session
```

### 5.3 Protected Route Flow

```
USER ACCESSES PROTECTED ROUTE:
──────────────────────────────

1. User navigates to /tasks
              │
              ▼
2. ProtectedLayout checks isAuthenticated
              │
       ┌──────┴──────┐
       │             │
   NOT AUTH      AUTHENTICATED
       │             │
       ▼             ▼
3a. Redirect    3b. Render
    to /login       children
       │
       ▼
4. After login success:
   Redirect to original destination
```

### 5.4 API Client Modifications

```
MODIFIED API CLIENT FLOW:
─────────────────────────

Current: /api/todos → Backend (no auth)

New:     /api/todos → Next.js Route Handler
                            │
                            ▼
                      Read access_token cookie
                            │
                            ▼
                      Add Authorization header
                            │
                            ▼
                      Forward to Backend /api/todos
                            │
                            ▼
                      Backend validates JWT
                            │
                            ▼
                      Return user-filtered data
```

---

## 6. Security Implementation Details

### 6.1 Password Handling

```
PASSWORD SECURITY FLOW:
──────────────────────

SIGNUP:
  1. Receive plain password from user
  2. Validate strength (min 8 chars, complexity optional)
  3. Generate bcrypt hash:
     - Cost factor: 12 (2^12 iterations)
     - Automatic salt generation
  4. Store ONLY the hash in database
  5. Plain password NEVER stored or logged

LOGIN:
  1. Receive plain password from user
  2. Retrieve hashed_password from database
  3. Use bcrypt.verify(plain, hashed)
  4. bcrypt handles salt extraction and comparison
  5. Timing-safe comparison prevents timing attacks
```

### 6.2 JWT Token Structure

```
JWT TOKEN COMPOSITION:
─────────────────────

Header (base64):
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload (base64):
{
  "sub": "user-uuid-here",     // Subject (user ID)
  "email": "user@example.com", // User email (for convenience)
  "iat": 1705401600,           // Issued at (Unix timestamp)
  "exp": 1705488000            // Expiration (24 hours later)
}

Signature:
HMACSHA256(
  base64(header) + "." + base64(payload),
  SECRET_KEY
)

Final Token:
<header>.<payload>.<signature>
```

### 6.3 Token Security Configuration

```
JWT CONFIGURATION:
─────────────────

SECRET_KEY:
  - Minimum 32 characters
  - Stored in environment variable
  - NEVER committed to version control
  - Rotate periodically

EXPIRATION:
  - Access token: 24 hours (configurable)
  - Consideration: Add refresh token for longer sessions

COOKIE SETTINGS:
  - HttpOnly: true (prevents XSS access)
  - Secure: true (HTTPS only in production)
  - SameSite: Lax (CSRF protection)
  - Path: / (available to all routes)
```

### 6.4 Security Checklist

```
SECURITY REQUIREMENTS:
─────────────────────

[✓] Passwords hashed with bcrypt (cost 12)
[✓] Plain passwords never stored
[✓] JWT signed with strong secret
[✓] Tokens expire after 24 hours
[✓] HTTP-only cookies prevent XSS
[✓] SameSite cookies prevent CSRF
[✓] User can only access own todos
[✓] 404 returned for unauthorized access (no enumeration)
[✓] Email uniqueness enforced at database level
[✓] Password validation on signup
[✓] Sensitive fields excluded from responses
```

---

## 7. User Data Isolation (Critical)

### 7.1 Isolation Strategy

```
DATA ISOLATION ENFORCEMENT:
──────────────────────────

PRINCIPLE: Backend is the ONLY authority for data access control.
           Frontend restrictions are UX only, not security.

ENFORCEMENT POINTS:

1. CREATE TODO:
   - Backend automatically sets user_id from JWT
   - User CANNOT specify user_id in request body
   - Any user_id in body is IGNORED

2. READ TODOS (List):
   - Query: SELECT * FROM todos WHERE user_id = :current_user_id
   - No todos from other users ever returned

3. READ TODO (Single):
   - Query: SELECT * FROM todos WHERE id = :id AND user_id = :current_user_id
   - Returns 404 if not found OR not owned

4. UPDATE TODO:
   - First query: SELECT * FROM todos WHERE id = :id AND user_id = :current_user_id
   - If not found → 404 (not 403)
   - Then perform update

5. DELETE TODO:
   - Same pattern as UPDATE
   - Verify ownership, then delete
```

### 7.2 Why 404 Instead of 403

```
SECURITY CONSIDERATION:
──────────────────────

Wrong Approach (403 Forbidden):
  - Reveals that the resource EXISTS
  - Attacker knows ID is valid, just not theirs
  - Enables enumeration attacks

Correct Approach (404 Not Found):
  - Resource appears to not exist
  - Attacker cannot determine valid IDs
  - Consistent with "your view of the world"
```

---

## 8. Migration Strategy

### 8.1 Database Migration Steps

```
MIGRATION SEQUENCE:
──────────────────

STEP 1: Create users table
  - New migration: create_users_table
  - Add UUID extension if not exists
  - Create users table with indexes

STEP 2: Add user_id to todos (nullable first)
  - New migration: add_user_id_to_todos
  - Add user_id column as NULLABLE
  - Add foreign key constraint
  - Add index on user_id

STEP 3: Create default user for existing todos
  - Create a "legacy" user OR
  - Assign existing todos to first registered user
  - Decision: Create migration that handles existing data

STEP 4: Make user_id NOT NULL
  - After data migration
  - New migration: make_user_id_required
  - ALTER COLUMN SET NOT NULL
```

### 8.2 Backward Compatibility

```
TRANSITION PERIOD:
─────────────────

Option A: Hard Cutover
  - Deploy auth, existing todos orphaned
  - Users must re-create todos
  - Simplest but loses data

Option B: Migration User (RECOMMENDED)
  - Create system user for existing todos
  - Existing todos assigned to system user
  - System user can be claimed by first signup
  - OR system user todos can be migrated manually

Option C: Public Period
  - Existing todos visible to all users temporarily
  - Users gradually claim/migrate their todos
  - Complex, security concerns
```

---

## 9. Implementation Phases

### Phase 1: Backend Auth Foundation
```
TASKS:
  1. Add auth dependencies (python-jose, passlib, bcrypt)
  2. Create User model (SQLModel)
  3. Create users table migration
  4. Implement password hashing utilities
  5. Implement JWT utilities (create, verify)
  6. Create auth routes (signup, login, logout, me)
  7. Create get_current_user dependency
  8. Unit tests for auth utilities
```

### Phase 2: Backend Todo Integration
```
TASKS:
  1. Add user_id to Todo model
  2. Create migration for user_id column
  3. Handle existing todos migration
  4. Modify todo routes to use get_current_user
  5. Update all queries to filter by user_id
  6. Update tests for multi-user scenarios
```

### Phase 3: Frontend Auth Pages
```
TASKS:
  1. Create AuthContext provider
  2. Create login page (/login)
  3. Create signup page (/signup)
  4. Add auth API proxy routes
  5. Implement protected route wrapper
  6. Add logout functionality
  7. Update navigation for auth state
```

### Phase 4: Frontend Integration
```
TASKS:
  1. Wrap app with AuthProvider
  2. Protect todo routes
  3. Update API client for auth
  4. Add error handling for 401s
  5. Redirect flows (login → dashboard, 401 → login)
  6. Loading states during auth checks
```

### Phase 5: Testing & Polish
```
TASKS:
  1. End-to-end auth flow testing
  2. Multi-user data isolation testing
  3. Security audit
  4. Error message review
  5. UX polish (loading, transitions)
  6. Documentation update
```

---

## 10. Configuration Requirements

### 10.1 New Environment Variables

```
BACKEND (.env):
──────────────
# Existing
DATABASE_URL=postgresql://...
API_HOST=0.0.0.0
API_PORT=8889
CORS_ORIGINS=http://localhost:3000,...
ENVIRONMENT=development

# NEW - Authentication
JWT_SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440  # 24 hours
BCRYPT_ROUNDS=12


FRONTEND (.env.local):
─────────────────────
# Existing
NEXT_PUBLIC_API_URL=http://localhost:8889/api

# No new public vars needed (auth handled server-side)
```

### 10.2 New Dependencies

```
BACKEND (requirements.txt additions):
────────────────────────────────────
python-jose[cryptography]==3.3.0  # JWT handling
passlib[bcrypt]==1.7.4            # Password hashing
bcrypt==4.1.2                     # bcrypt backend


FRONTEND (package.json additions):
─────────────────────────────────
# No new dependencies required
# Using built-in Next.js features (cookies, middleware)
```

---

## 11. API Response Codes Summary

```
AUTH ENDPOINTS:
──────────────
POST /auth/signup
  201 - User created successfully
  400 - Invalid email format
  400 - Password too weak
  409 - Email already registered
  500 - Server error

POST /auth/login
  200 - Login successful
  401 - Invalid credentials
  500 - Server error

POST /auth/logout
  200 - Logged out successfully

GET /auth/me
  200 - User info returned
  401 - Not authenticated


TODO ENDPOINTS (Protected):
──────────────────────────
All existing codes plus:
  401 - Not authenticated (no/invalid token)

Note: 404 returned for "not found" AND "not owned"
      (never 403 for ownership issues)
```

---

## 12. Acceptance Criteria

### Must Have
- [ ] Users can sign up with email and password
- [ ] Users can sign in and receive JWT token
- [ ] Users can sign out (token invalidated)
- [ ] Passwords are bcrypt hashed (never plain text)
- [ ] Each user sees ONLY their own todos
- [ ] Users cannot access/modify other users' todos
- [ ] 401 returned for unauthenticated requests to protected routes
- [ ] JWT tokens expire after configured time

### Should Have
- [ ] Password strength validation on signup
- [ ] Email format validation
- [ ] Proper error messages for auth failures
- [ ] Loading states during auth operations
- [ ] Automatic redirect after login/logout

### Nice to Have
- [ ] Remember me functionality
- [ ] Password reset flow
- [ ] Email verification
- [ ] Session management (view active sessions)

---

## 13. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| JWT secret key exposure | Critical | Store in env vars, never commit |
| SQL injection in user lookup | Critical | Use parameterized queries (SQLModel) |
| Timing attacks on password | Medium | bcrypt has constant-time comparison |
| Token theft via XSS | High | HTTP-only cookies |
| CSRF attacks | Medium | SameSite cookie attribute |
| User enumeration | Low | Consistent 404 responses |
| Existing data migration | Medium | Create migration user, plan carefully |

---

## 14. Open Questions

1. **Existing Todos**: How should existing todos be handled?
   - Option A: Orphan them (users re-create)
   - Option B: Assign to first user who signs up
   - Option C: Create migration/admin process

2. **Token Refresh**: Should we implement refresh tokens?
   - Current plan: Single access token, 24hr expiry
   - Future: Add refresh token for better UX

3. **Password Requirements**: What complexity rules?
   - Minimum: 8 characters
   - Optional: uppercase, number, special char

4. **Rate Limiting**: Should auth endpoints be rate-limited?
   - Recommended: Yes, to prevent brute force
   - Implementation: Separate concern, future phase

---

## 15. Conclusion

This plan provides a comprehensive roadmap for implementing secure user authentication in the Phase 2 Todo application. The architecture ensures:

1. **Security**: bcrypt passwords, JWT tokens, HTTP-only cookies
2. **Isolation**: Users can only access their own data
3. **Scalability**: Stateless backend, no server-side sessions
4. **Maintainability**: Clean separation of concerns

The implementation should proceed in phases, with backend auth foundation first, followed by todo integration, and finally frontend implementation.

---

**Next Steps:**
1. Review and approve this plan
2. Create detailed task breakdown
3. Begin Phase 1 implementation
