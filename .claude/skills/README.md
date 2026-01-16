# Claude Skills Registry

Custom skills for the Hackathon II Todo Application project.

---

## Available Skills

### 1. NeonPostgresSkill
**Type**: Database Management
**Framework**: Neon Postgres (Serverless PostgreSQL)
**Format**: Claude Code Skill
**Location**: `.claude/skills/neon-postgres-skill/`

**Purpose**:
Scaffolds and manages Neon Postgres serverless databases. Provides schema templates, connection management, query generation, and validation scripts for Next.js and FastAPI applications.

**Key Features**:
- ✅ Neon account and database setup guidance
- ✅ Production-ready schema templates
- ✅ Connection string configuration and validation
- ✅ Database creation and migration scripts
- ✅ Example SQL queries (CRUD, aggregations, advanced)
- ✅ Connection pooling setup (PgBouncer)
- ✅ Next.js and FastAPI integration examples
- ✅ Python utility functions for database operations

**Activation Triggers**:
- "Neon Postgres"
- "Neon database"
- "serverless Postgres"
- "database setup"
- "PostgreSQL connection"

**Files**:
- `SKILL.md` - Main skill definition with metadata and comprehensive guidance
- `reference.md` - Complete Neon Postgres documentation and best practices
- `examples.md` - Practical integration examples (Next.js, FastAPI)
- `scripts/` - Utility scripts
  - `create_db.py` - Database and schema creation
  - `validate_connection.py` - Connection validation
  - `generate_queries.py` - SQL query generation
- `template/` - Ready-to-use templates
  - `schema.sql` - Production-ready database schema
  - `queries.sql` - Example SQL queries
  - `env.example` - Environment variable template
  - `utils.py` - Python database utility functions

---

### 2. NextJSSkill
**Type**: Frontend Development
**Framework**: Next.js 14+
**Format**: Claude Code Skill
**Location**: `.claude/skills/nextjs-skill/`

**Purpose**:
Provides expert guidance for scaffolding and managing Next.js frontend applications for Phase II and beyond.

**Key Features**:
- ✅ Project initialization and scaffolding
- ✅ Component generation (TodoList, TodoItem, TodoForm, FilterBar, SearchBar)
- ✅ API client integration with FastAPI backend
- ✅ Client-side validation with Zod
- ✅ Responsive design patterns (Tailwind CSS)
- ✅ TypeScript interfaces and type safety
- ✅ Configuration templates (next.config.js, tailwind.config.ts)

**Activation Triggers**:
- "Next.js"
- "Phase II frontend"
- "scaffold"
- "routing"
- "components"

**Files**:
- `SKILL.md` - Main skill definition with metadata and comprehensive guidance
- `reference.md` - Complete technical reference and documentation
- `examples.md` - Practical walkthroughs and examples
- `scripts/` - Utility scripts
  - `validate-nextjs-setup.py` - Project validation
  - `generate-component.py` - Component generator
- `template/` - Ready-to-use code templates

---

### 3. FastAPISkill
**Type**: Backend Development
**Framework**: FastAPI 2+
**Format**: Claude Code Skill
**Location**: `.claude/skills/fastapi-skill/`

**Purpose**:
Reusable skill module for scaffolding and managing FastAPI backend applications across multiple projects and phases.

**Key Features**:
- ✅ Complete project scaffolding
- ✅ Router and endpoint generation
- ✅ SQLModel + Pydantic model creation
- ✅ Database configuration (PostgreSQL, MySQL, SQLite)
- ✅ CORS middleware setup
- ✅ Environment configuration
- ✅ API documentation generation
- ✅ Alembic migrations setup

**Core Capabilities**:
- Project creation with standard structure
- Database integration (SQLModel, SQLAlchemy, Tortoise)
- Model and schema generation
- CRUD router templates
- CORS configuration
- Production-ready patterns

**Files**:
- `SKILL.md` - Main skill definition with metadata and guidance
- `reference.md` - Complete technical reference and best practices
- `examples.md` - Practical walkthroughs and Phase II setup
- `scripts/` - Utility scripts
  - `create_project.py` - Project scaffolding tool
  - `validate_setup.py` - Structure validation
- `template/` - Code templates for FastAPI projects

---

### 4. TailwindSkill
**Type**: Styling & Design
**Framework**: Tailwind CSS 3+
**Format**: Claude Code Skill
**Location**: `.claude/skills/tailwind-skill/`

**Purpose**:
Scaffolds and manages Tailwind CSS configuration for Next.js applications with enhanced theme customization and validation.

**Key Features**:
- ✅ Configuration generation (tailwind.config.ts)
- ✅ Global styles setup (globals.css with custom layers)
- ✅ Pre-built component templates (Button, Card, Navbar)
- ✅ Theme customization (colors, fonts, spacing, animations)
- ✅ Setup validation and verification
- ✅ Dark mode support
- ✅ Responsive design utilities
- ✅ Custom animations and keyframes

**Core Capabilities**:
- Generate production-ready Tailwind configuration
- Create globals.css with @layer directives
- Provide reusable styled components
- Validate Tailwind integration
- Support custom theme extensions

**Files**:
- `SKILL.md` - Main skill definition with metadata and guidance
- `reference.md` - Complete Tailwind CSS reference and best practices
- `examples.md` - Practical examples and component usage
- `scripts/` - Utility scripts
  - `generate-config.py` - Configuration generator
  - `validate-setup.py` - Setup validation
- `template/` - Ready-to-use templates
  - `tailwind.config.ts` - Enhanced Tailwind config
  - `globals.css` - Base styles with custom layers
  - `components/` - Styled component templates

---

### 5. ShadcnSkill
**Type**: UI Component System
**Framework**: shadcn/ui + Radix UI
**Format**: Claude Code Skill
**Location**: `.claude/skills/shadcn-skill/`

**Purpose**:
Scaffolds and manages shadcn/ui components for Next.js + Tailwind projects. Provides accessible, customizable UI components built on Radix UI primitives.

**Key Features**:
- ✅ shadcn/ui component generation (Button, Card, Input, Modal, Navbar)
- ✅ Radix UI integration with accessibility built-in
- ✅ class-variance-authority (CVA) for component variants
- ✅ cn() utility for className merging
- ✅ Layout templates with provider setup
- ✅ Custom hooks (useModal) for state management
- ✅ Full TypeScript support
- ✅ Setup validation and verification

**Core Capabilities**:
- Generate accessible UI components
- Copy-paste component model (own your code)
- Tailwind CSS integration
- Dark mode support
- Composable component primitives
- Form-ready inputs
- Modal/Dialog management

**Files**:
- `SKILL.md` - Main skill definition with metadata and guidance
- `reference.md` - Complete shadcn/ui reference and best practices
- `examples.md` - Practical examples and component usage
- `scripts/` - Utility scripts
  - `generate-components.py` - Component generator
  - `validate-setup.py` - Setup validation
- `template/` - Ready-to-use templates
  - `layout.tsx` - Layout with provider
  - `components/` - shadcn/ui components (Button, Card, Input, Modal, Navbar)
  - `hooks/` - Helper hooks (useModal)

---

## Usage

### NeonPostgresSkill

Neon Postgres skill can be used via scripts or Claude conversation:

```bash
# Create database and apply schema
python .claude/skills/neon-postgres-skill/scripts/create_db.py

# Validate connection and setup
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py

# Generate SQL queries
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py --output database/queries.sql
```

Or simply ask Claude:
```
"Set up Neon Postgres for the todo app"
"Apply Neon database schema"
"Validate Neon connection"
"Generate SQL queries for todos"
```

### NextJSSkill

Skills in Claude Code format are automatically activated based on conversation context:

```bash
# Ask Claude about Next.js and the skill activates automatically
"How do I scaffold the Phase II Next.js frontend?"

# Or use utility scripts directly
python .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py phase-II/frontend
python .claude/skills/nextjs-skill/scripts/generate-component.py TodoCard --client
```

### FastAPISkill

FastAPI skill can be used via Claude conversation or scripts:

```bash
# Create a new FastAPI project
python .claude/skills/fastapi-skill/scripts/create_project.py \
  --name todo_backend \
  --output ./phase-II/backend \
  --database postgresql

# Validate existing project structure
python .claude/skills/fastapi-skill/scripts/validate_setup.py phase-II/backend
```

Or simply ask Claude:
```
"Create a FastAPI backend for Phase II"
"Set up the Todo API with SQLModel and PostgreSQL"
```

### TailwindSkill

Tailwind skill can be used via scripts or Claude conversation:

```bash
# Generate Tailwind configuration
python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir phase-II/frontend

# Validate Tailwind setup
python .claude/skills/tailwind-skill/scripts/validate-setup.py phase-II/frontend
```

Or simply ask Claude:
```
"Set up Tailwind CSS with custom theme"
"Generate Tailwind config with dark mode support"
```

### ShadcnSkill

shadcn/ui skill can be used via scripts or Claude conversation:

```bash
# Generate shadcn/ui components
python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir phase-II/frontend/app

# Validate shadcn/ui setup
python .claude/skills/shadcn-skill/scripts/validate-setup.py phase-II/frontend
```

Or simply ask Claude:
```
"Set up shadcn/ui components"
"Generate shadcn Button and Modal components"
"Apply shadcn skill to project"
```

---

## Phase II Integration

All five skills are designed to work together for Phase II implementation:

### Database (NeonPostgresSkill)
1. Create Neon account and project
2. Configure connection string in environment variables
3. Apply database schema with todos table
4. Set up connection pooling for production
5. Validate connection and table setup
6. Generate example queries for development

### Frontend (NextJSSkill)
1. Scaffold Next.js project: `phase-II/frontend/`
2. Generate components: TodoList, TodoItem, TodoForm, FilterBar, SearchBar
3. Configure API client for FastAPI backend
4. Set up environment variables (NEXT_PUBLIC_API_URL)
5. Implement responsive UI with Tailwind CSS

### Styling (TailwindSkill)
1. Generate enhanced Tailwind configuration
2. Create globals.css with custom layers and utilities
3. Set up dark mode support
4. Provide pre-built component templates (Button, Card, Navbar)
5. Validate Tailwind integration

### UI Components (ShadcnSkill)
1. Generate shadcn/ui accessible components
2. Set up Radix UI primitives integration
3. Create cn() utility for className merging
4. Provide form-ready inputs and modals
5. Validate shadcn/ui configuration

### Backend (FastAPISkill)
1. Scaffold FastAPI project: `phase-II/backend/`
2. Configure PostgreSQL database with SQLModel
3. Create Todo model with proper schema
4. Generate todos router with CRUD endpoints
5. Apply CORS for Next.js frontend
6. Set up Alembic migrations

### Workflow Example

```bash
# 0. Setup Neon Postgres database
# Create Neon account at https://neon.tech and get connection string
# Add to .env: DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require
python .claude/skills/neon-postgres-skill/scripts/create_db.py
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py

# 1. Create backend
python .claude/skills/fastapi-skill/scripts/create_project.py \
  --name "Todo API" \
  --output phase-II/backend \
  --database postgresql

# 2. Create frontend
cd phase-II
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --import-alias '@/*'

# 3. Set up Tailwind CSS
python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir phase-II/frontend

# 4. Generate shadcn/ui components
python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir phase-II/frontend/app

# 5. Validate all components
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
python .claude/skills/fastapi-skill/scripts/validate_setup.py phase-II/backend
python .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py phase-II/frontend
python .claude/skills/tailwind-skill/scripts/validate-setup.py phase-II/frontend
python .claude/skills/shadcn-skill/scripts/validate-setup.py phase-II/frontend
```

---

## Directory Structure

All skills follow a consistent standardized structure:

```
.claude/skills/
├── README.md                       # This file (Skills registry)
│
├── neon-postgres-skill/            # Neon Postgres Database Skill
│   ├── SKILL.md                    # Skill definition
│   ├── reference.md                # Technical reference
│   ├── examples.md                 # Practical examples
│   ├── scripts/                    # Utility scripts
│   │   ├── create_db.py
│   │   ├── validate_connection.py
│   │   └── generate_queries.py
│   └── template/                   # Code templates
│       ├── schema.sql
│       ├── queries.sql
│       ├── env.example
│       └── utils.py
│
├── nextjs-skill/                   # Next.js Frontend Skill
│   ├── SKILL.md                    # Skill definition
│   ├── reference.md                # Technical reference
│   ├── examples.md                 # Practical examples
│   ├── scripts/                    # Utility scripts
│   │   ├── validate-nextjs-setup.py
│   │   └── generate-component.py
│   └── template/                   # Code templates
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── types/
│
├── fastapi-skill/                  # FastAPI Backend Skill
│   ├── SKILL.md                    # Skill definition
│   ├── reference.md                # Technical reference
│   ├── examples.md                 # Practical examples
│   ├── scripts/                    # Utility scripts
│   │   ├── create_project.py
│   │   └── validate_setup.py
│   └── template/                   # Code templates
│       ├── core.py
│       └── utils.py
│
├── tailwind-skill/                 # Tailwind CSS Styling Skill
│   ├── SKILL.md                    # Skill definition
│   ├── reference.md                # Technical reference
│   ├── examples.md                 # Practical examples
│   ├── scripts/                    # Utility scripts
│   │   ├── generate-config.py
│   │   └── validate-setup.py
│   └── template/                   # Code templates
│       ├── tailwind.config.ts
│       ├── globals.css
│       └── components/
│           ├── Button.tsx
│           ├── Card.tsx
│           └── Navbar.tsx
│
└── shadcn-skill/                   # shadcn/ui Component System
    ├── SKILL.md                    # Skill definition
    ├── reference.md                # Technical reference
    ├── examples.md                 # Practical examples
    ├── scripts/                    # Utility scripts
    │   ├── generate-components.py
    │   └── validate-setup.py
    └── template/                   # Code templates
        ├── layout.tsx
        ├── components/
        │   ├── Button.tsx
        │   ├── Card.tsx
        │   ├── Input.tsx
        │   ├── Modal.tsx
        │   └── Navbar.tsx
        └── hooks/
            └── useModal.ts
```

**Consistent Structure Elements**:
- ✅ `SKILL.md` - Main skill definition with Claude Code metadata
- ✅ `reference.md` - Comprehensive technical documentation
- ✅ `examples.md` - Practical walkthroughs and usage examples
- ✅ `scripts/` - Automation and validation tools
- ✅ `template/` - Ready-to-use code templates

---

## Skill Format

All skills use the **Claude Code Skill Format**:

**Structure**: YAML metadata + Markdown content

**SKILL.md Format**:
```yaml
---
name: skill-name
description: What the skill does and when to use it
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# Skill Content

Your skill instructions here...
```

**Activation**: Automatic based on description matching in conversation context

**Best for**: Guidance, templates, documentation, automation

---

## Adding New Skills

To add a new skill to this project:

1. Create directory: `.claude/skills/my-skill/`

2. Create `SKILL.md` with metadata:
   ```yaml
   ---
   name: my-skill
   description: What the skill does and when to use it
   allowed-tools: Read, Write, Bash
   model: sonnet
   ---

   # Skill Content

   Your skill instructions here...
   ```

3. Create `reference.md` with comprehensive documentation

4. Create `examples.md` with practical walkthroughs

5. Add `scripts/` directory with utility scripts

6. Add `template/` directory with code templates

7. Skills load automatically on Claude Code restart

---

## Testing

### NeonPostgresSkill
```bash
# Create database and apply schema
python .claude/skills/neon-postgres-skill/scripts/create_db.py

# Validate Neon connection
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py --verbose

# Generate SQL queries
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py --output queries.sql
```

### NextJSSkill
```bash
# Validate Next.js project structure
python .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py phase-II/frontend

# Generate React component
python .claude/skills/nextjs-skill/scripts/generate-component.py MyComponent --client
```

### FastAPISkill
```bash
# Create new FastAPI project
python .claude/skills/fastapi-skill/scripts/create_project.py --name my_api --output ./backend

# Validate FastAPI project structure
python .claude/skills/fastapi-skill/scripts/validate_setup.py ./backend
```

### TailwindSkill
```bash
# Generate Tailwind configuration
python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir ./frontend

# Validate Tailwind setup
python .claude/skills/tailwind-skill/scripts/validate-setup.py ./frontend
```

---

## Documentation

- **NeonPostgresSkill**:
  - [SKILL.md](neon-postgres-skill/SKILL.md) - Skill definition
  - [reference.md](neon-postgres-skill/reference.md) - Technical reference
  - [examples.md](neon-postgres-skill/examples.md) - Practical examples

- **NextJSSkill**:
  - [SKILL.md](nextjs-skill/SKILL.md) - Skill definition
  - [reference.md](nextjs-skill/reference.md) - Technical reference
  - [examples.md](nextjs-skill/examples.md) - Practical examples

- **FastAPISkill**:
  - [SKILL.md](fastapi-skill/SKILL.md) - Skill definition
  - [reference.md](fastapi-skill/reference.md) - Technical reference
  - [examples.md](fastapi-skill/examples.md) - Practical examples

- **TailwindSkill**:
  - [SKILL.md](tailwind-skill/SKILL.md) - Skill definition
  - [reference.md](tailwind-skill/reference.md) - Technical reference
  - [examples.md](tailwind-skill/examples.md) - Practical examples

---

## Technology Stack

### Database (NeonPostgresSkill)
- Neon Postgres (Serverless PostgreSQL 15+)
- Python 3.11+
- psycopg2 (PostgreSQL adapter)
- SQLAlchemy / Prisma
- Connection pooling (PgBouncer)
- SSL/TLS encryption

### Frontend (NextJSSkill)
- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- Zod validation
- Axios for HTTP

### Styling (TailwindSkill)
- Tailwind CSS 3+
- PostCSS
- Autoprefixer
- Custom theme extensions
- Dark mode support
- Responsive utilities

### Backend (FastAPISkill)
- FastAPI 0.100+
- Python 3.11+
- SQLModel 0.0.14+
- Pydantic 2.0+
- Uvicorn (ASGI server)
- Alembic (migrations)
- PostgreSQL/MySQL/SQLite

---

## Version History

- **2025-12-31**: Skills restructured to standardized format
  - NeonPostgresSkill v1.0.0 - Created with comprehensive Neon Postgres support
  - NextJSSkill v1.0.0 - Standardized structure
  - FastAPISkill v1.0.0 - Converted to Claude Code format
  - TailwindSkill v1.0.0 - Created with comprehensive Tailwind CSS support
  - ShadcnSkill v1.0.0 - Created with shadcn/ui component support
  - All skills now follow identical organization

---

## License

All skills: MIT License

---

**Project**: Hackathon II Todo Application
**Branch**: 002-phase-ii-web-app
**Created**: 2025-12-31
**Skills Directory**: `.claude/skills/`
