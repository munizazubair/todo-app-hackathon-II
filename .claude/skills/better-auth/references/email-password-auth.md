# Email/Password Authentication

## Basic Setup

Enable email/password authentication in your auth configuration:

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    // your database config
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true, // Auto sign in after signup
    requireEmailVerification: false, // Enable for production
  }
});
```

## Sign Up

```typescript
// Client-side
const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe", // Optional
  image: "https://example.com/avatar.jpg" // Optional
});

if (error) {
  console.error("Sign up failed:", error.message);
} else {
  console.log("User created:", data.user);
}
```

## Sign In

```typescript
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
  callbackURL: "/dashboard", // Redirect after login
  rememberMe: true // Extended session
});
```

## Email Verification

### Enable Verification

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendResetPassword: async ({ user, url, token }, request) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Click to verify</a>`
      });
    }
  }
});
```

### Send Verification Email

```typescript
await authClient.sendVerificationEmail({
  email: "user@example.com",
  callbackURL: "/email-verified"
});
```

## Password Reset

### Configure Reset Handler

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url, token }, request) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `<a href="${url}">Reset Password</a>`
      });
    }
  }
});
```

### Request Reset

```typescript
await authClient.forgetPassword({
  email: "user@example.com",
  redirectTo: "/reset-password"
});
```

### Reset Password

```typescript
await authClient.resetPassword({
  token: "reset-token-from-url",
  newPassword: "newSecurePassword123"
});
```

## Username Authentication (Plugin)

### Enable Username Plugin

```typescript
import { betterAuth } from "better-auth";
import { username } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    username({
      minLength: 3,
      maxLength: 20
    })
  ]
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/client";
import { usernameClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [usernameClient()]
});
```

### Sign In with Username

```typescript
await authClient.signIn.username({
  username: "johndoe",
  password: "secure123"
});
```

## Framework Setup

### Next.js App Router

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

### Express

```typescript
import express from "express";
import { auth } from "./auth";
import { toNodeHandler } from "better-auth/node";

const app = express();
app.all("/api/auth/*", toNodeHandler(auth));
```

## Password Requirements

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    password: {
      minLength: 8,
      maxLength: 128,
      validate: (password) => {
        if (!/[A-Z]/.test(password)) {
          return { valid: false, message: "Must contain uppercase" };
        }
        if (!/[0-9]/.test(password)) {
          return { valid: false, message: "Must contain number" };
        }
        return { valid: true };
      }
    }
  }
});
```

## Error Handling

| Error Code | Description |
|------------|-------------|
| `USER_NOT_FOUND` | Email not registered |
| `INVALID_PASSWORD` | Wrong password |
| `EMAIL_NOT_VERIFIED` | Email verification required |
| `USER_ALREADY_EXISTS` | Email already registered |
| `INVALID_TOKEN` | Expired/invalid reset token |
