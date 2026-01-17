# OAuth Providers

## Supported Providers

Better Auth supports 20+ OAuth providers out of the box:

- GitHub, Google, Discord, Twitter/X, Facebook, Apple, Microsoft, LinkedIn, Spotify, Twitch, GitLab, Dropbox, and more...

## Basic Configuration

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    }
  }
});
```

## Provider-Specific Setup

### GitHub

1. Go to GitHub Settings > Developer Settings > OAuth Apps
2. Create new OAuth App
3. Set callback URL: `{YOUR_URL}/api/auth/callback/github`

```typescript
github: {
  clientId: process.env.GITHUB_CLIENT_ID!,
  clientSecret: process.env.GITHUB_CLIENT_SECRET!,
  scope: ["user:email", "read:user"]
}
```

### Google

1. Go to Google Cloud Console > APIs & Services > Credentials
2. Create OAuth 2.0 Client ID
3. Set callback URL: `{YOUR_URL}/api/auth/callback/google`

```typescript
google: {
  clientId: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  scope: ["openid", "email", "profile"]
}
```

### Discord

1. Go to Discord Developer Portal > Applications
2. Create new application > OAuth2
3. Set callback URL: `{YOUR_URL}/api/auth/callback/discord`

```typescript
discord: {
  clientId: process.env.DISCORD_CLIENT_ID!,
  clientSecret: process.env.DISCORD_CLIENT_SECRET!,
  scope: ["identify", "email"]
}
```

## Client Usage

### Sign In with OAuth

```typescript
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard"
});
```

### Link Account

```typescript
await authClient.linkSocial({
  provider: "github",
  callbackURL: "/settings/accounts"
});
```

### Unlink Account

```typescript
await authClient.unlinkAccount({
  providerId: "github"
});
```

## Custom OAuth Provider

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  socialProviders: {
    custom: {
      id: "custom-provider",
      name: "Custom Provider",
      type: "oauth2",
      clientId: process.env.CUSTOM_CLIENT_ID!,
      clientSecret: process.env.CUSTOM_CLIENT_SECRET!,
      authorization: {
        url: "https://provider.com/oauth/authorize",
        params: { scope: "openid email profile" }
      },
      token: { url: "https://provider.com/oauth/token" },
      userinfo: { url: "https://provider.com/userinfo" },
      profile: (profile) => ({
        id: profile.sub,
        email: profile.email,
        name: profile.name,
        image: profile.picture
      })
    }
  }
});
```

## Account Linking Options

```typescript
export const auth = betterAuth({
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github"],
      allowDifferentEmail: false
    }
  }
});
```

## Environment Variables Template

```env
# GitHub
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Google
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Discord
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
```
