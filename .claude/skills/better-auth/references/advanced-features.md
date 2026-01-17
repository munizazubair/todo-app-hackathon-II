# Advanced Features

## Two-Factor Authentication (2FA)

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: "MyApp",
      otpOptions: { period: 30, digits: 6 }
    })
  ]
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/client";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [twoFactorClient()]
});
```

### Enable 2FA

```typescript
const { data } = await authClient.twoFactor.enable({
  password: "current-password"
});
// data.totpURI - Use to generate QR code

await authClient.twoFactor.verifyTotp({ code: "123456" });
```

## Passkeys / WebAuthn

### Server Setup

```typescript
import { passkey } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    passkey({
      rpID: "example.com",
      rpName: "My App",
      origin: "https://example.com"
    })
  ]
});
```

### Usage

```typescript
// Register passkey
await authClient.passkey.addPasskey({ name: "My MacBook" });

// Sign in with passkey
await authClient.signIn.passkey({ callbackURL: "/dashboard" });
```

## Magic Link

### Server Setup

```typescript
import { magicLink } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    magicLink({
      sendMagicLink: async ({ email, url }) => {
        await sendEmail({
          to: email,
          subject: "Sign in to MyApp",
          html: `<a href="${url}">Click to sign in</a>`
        });
      },
      expiresIn: 300
    })
  ]
});
```

### Usage

```typescript
await authClient.signIn.magicLink({
  email: "user@example.com",
  callbackURL: "/dashboard"
});
```

## Organizations / Multi-Tenant

### Server Setup

```typescript
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
      organizationLimit: 5,
      creatorRole: "owner"
    })
  ]
});
```

### Usage

```typescript
// Create organization
await authClient.organization.create({ name: "Acme Inc", slug: "acme" });

// Invite members
await authClient.organization.inviteMember({
  organizationId: "org-id",
  email: "member@example.com",
  role: "member"
});

// Set active organization
await authClient.organization.setActive({ organizationId: "org-id" });
```

## Rate Limiting

```typescript
export const auth = betterAuth({
  rateLimit: {
    enabled: true,
    window: 60,
    max: 10,
    customRules: {
      "/api/auth/sign-in/email": { window: 60, max: 5 },
      "/api/auth/sign-up/email": { window: 3600, max: 3 }
    }
  }
});
```

## Session Management

```typescript
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24
  }
});
```

### Session Operations

```typescript
// List sessions
const { data } = await authClient.listSessions();

// Revoke session
await authClient.revokeSession({ token: "session-token" });

// Revoke all other sessions
await authClient.revokeOtherSessions();
```

## Protected Routes (Next.js)

```typescript
// middleware.ts
import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

export async function middleware(request) {
  const session = await auth.api.getSession({
    headers: request.headers
  });

  if (!session && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"]
};
```

## Hooks and Callbacks

```typescript
export const auth = betterAuth({
  callbacks: {
    onSignIn: async ({ user, session }) => {
      await logUserActivity(user.id, "sign_in");
    },
    onSignUp: async ({ user }) => {
      await sendWelcomeEmail(user.email);
    },
    onSignOut: async ({ session }) => {
      await logUserActivity(session.userId, "sign_out");
    }
  }
});
```
