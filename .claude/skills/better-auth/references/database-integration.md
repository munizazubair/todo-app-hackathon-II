# Database Integration

## Supported Databases

- **Prisma** - Popular TypeScript ORM
- **Drizzle** - TypeScript ORM with SQL-like syntax
- **Kysely** - Type-safe SQL query builder
- **MongoDB** - NoSQL database
- **LibSQL/Turso** - Edge-compatible SQLite

## Prisma Setup

```typescript
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql" // or "mysql", "sqlite"
  })
});
```

### Generate Schema

```bash
npx @better-auth/cli generate --output prisma/schema.prisma
```

## Drizzle Setup

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "./db";
import * as schema from "./schema";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema
  })
});
```

## Kysely Setup

```typescript
import { betterAuth } from "better-auth";
import { kyselyAdapter } from "better-auth/adapters/kysely";
import { db } from "./db";

export const auth = betterAuth({
  database: kyselyAdapter(db, {
    provider: "pg"
  })
});
```

## MongoDB Setup

```typescript
import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { MongoClient } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI!);
const db = client.db("your-database");

export const auth = betterAuth({
  database: mongodbAdapter(db)
});
```

## Schema CLI Commands

```bash
# Generate schema
npx @better-auth/cli generate --output ./schema.ts

# Apply migrations (Kysely)
npx @better-auth/cli migrate
```

## Custom User Fields

```typescript
export const auth = betterAuth({
  user: {
    additionalFields: {
      role: {
        type: "string",
        required: false,
        defaultValue: "user"
      },
      phone: {
        type: "string",
        required: false
      }
    }
  }
});
```

## Database Hooks

```typescript
export const auth = betterAuth({
  databaseHooks: {
    user: {
      create: {
        before: async (user) => {
          return { data: { ...user, role: "user" } };
        },
        after: async (user) => {
          await sendWelcomeEmail(user.email);
        }
      }
    }
  }
});
```
