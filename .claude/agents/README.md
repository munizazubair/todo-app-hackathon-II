# Claude Agents Registry

Custom agents for the Hackathon II Todo Application project.

---

## What are Claude Agents?

**Claude Agents** are specialized AI assistants that provide expert guidance and autonomous task execution for specific domains or workflows. Unlike skills (which are templates and tools), agents act as **intelligent assistants** that can:

- Understand complex requirements
- Generate complete solutions
- Provide expert advice and best practices
- Review and debug code
- Adapt to your project's specific needs

---

## Available Agents

### 1. Frontend Expert Agent
**Type**: Frontend Development Assistant
**Specialization**: Next.js 14+, React 18+, Tailwind CSS 3+, ShadCN/UI
**Location**: `.claude/agents/frontend-expert-agent.md`

**Purpose**:
Your personal frontend development assistant specializing in modern web development. Generates components, pages, and layouts while providing expert guidance on responsive design, accessibility, and performance optimization.

**Core Capabilities**:
- Component generation (TypeScript + Tailwind + ShadCN)
- Page and layout scaffolding
- API integration patterns
- State management solutions
- Responsive design (mobile-first)
- Accessibility compliance (WCAG AA)
- Performance optimization
- Code review and debugging

**Activation Triggers**: "Next.js", "React component", "Tailwind CSS", "ShadCN", "frontend", "responsive design"

**File**: `frontend-expert-agent.md`

---

### 2. Backend Expert Agent
**Type**: Backend Development Assistant
**Specialization**: FastAPI, PostgreSQL (Neon), Authentication, RESTful APIs
**Location**: `.claude/agents/backend-expert-agent.md`

**Purpose**:
Your senior backend architect for production-grade API development. Designs clean, scalable, secure backend systems with FastAPI and Neon PostgreSQL.

**Core Capabilities**:
- Backend architecture design
- FastAPI application development
- Neon PostgreSQL integration
- RESTful API endpoint creation
- Authentication & authorization (JWT, OAuth)
- Database schema design & migrations
- Error handling & logging
- Performance optimization & security

**Activation Triggers**: "FastAPI", "backend", "API", "PostgreSQL", "Neon", "authentication", "database"

**File**: `backend-expert-agent.md`

---

### 3. Database Expert Agent
**Type**: Database Architecture Assistant
**Specialization**: PostgreSQL (Neon Serverless), Database Design, Query Optimization
**Location**: `.claude/agents/database-expert-agent.md`

**Purpose**:
Your database architecture and optimization expert. Designs robust, scalable database schemas with PostgreSQL (Neon Serverless) and optimizes query performance for production workloads.

**Core Capabilities**:
- Database schema design & normalization
- Query optimization & indexing strategies
- Database migrations & schema versioning
- Connection pooling & performance tuning
- Row-level security & access control
- Materialized views & aggregations
- Soft deletes & audit trails
- Neon Serverless optimization

**Activation Triggers**: "PostgreSQL", "Neon", "database schema", "query optimization", "database migration", "indexing", "database design"

**File**: `database-expert-agent.md`

---

### 4. UI/UX Expert Agent
**Type**: UI/UX Design Assistant
**Specialization**: User-Centered Design, Design Systems, Accessibility, Framer Motion
**Location**: `.claude/agents/ui-ux-expert-agent.md`

**Purpose**:
Your UI/UX design and frontend experience expert. Creates beautiful, accessible, and intuitive interfaces with modern design systems, focusing on user experience excellence.

**Core Capabilities**:
- User-centered design & UX research
- Design systems & design tokens
- Accessibility compliance (WCAG AA/AAA)
- Micro-interactions & animations (Framer Motion)
- Responsive & mobile-first design
- Form validation UX patterns
- Dark mode theming
- Information architecture
- Loading states & empty states
- Visual hierarchy & typography

**Activation Triggers**: "UI/UX", "design system", "user experience", "accessibility", "responsive design", "micro-interactions", "animation", "dark mode", "design tokens"

**File**: `ui-ux-expert-agent.md`

---

### 5. Fullstack Architecture Expert
**Type**: System Architecture Assistant
**Specialization**: Full-Stack Architecture, API Design, Scalability, Cloud-Native Patterns
**Location**: `.claude/agents/fullstack-architecture-expert.md`

**Purpose**:
Your principal full-stack architect for designing scalable, secure, and maintainable application architectures. Provides strategic guidance on system design, API contracts, and deployment strategies.

**Core Capabilities**:
- Full-stack architecture design (Next.js + FastAPI + PostgreSQL)
- API design & contracts (REST, OpenAPI, type-safe)
- Authentication & authorization architecture
- Database architecture & migration strategies
- Scalability patterns & performance optimization
- Error handling & testing architecture
- Deployment strategies & CI/CD pipelines
- Architectural Decision Records (ADRs)
- Phase-aware guidance (MVP → Growth → Scale)
- Technical debt assessment & refactoring

**Activation Triggers**: "architecture", "system design", "full-stack", "API design", "scalability", "authentication flow", "database architecture", "deployment strategy"

**File**: `fullstack-architecture-expert.md`

---

## Agent vs Skill: What's the Difference?

### Skills (`.claude/skills/`)
**Purpose**: Provide templates, tools, and scripts

**Characteristics**:
- Static templates and code snippets
- Utility scripts for automation
- Documentation and references
- Follow predefined patterns

**Examples**:
- NextJSSkill - Next.js templates
- TailwindSkill - Tailwind configuration
- NeonPostgresSkill - Database setup scripts

### Agents (`.claude/agents/`)
**Purpose**: Provide intelligent assistance and guidance

**Characteristics**:
- Understand context and requirements
- Generate custom solutions
- Provide expert advice
- Review and optimize code
- Adapt to project needs

**Examples**:
- Frontend Expert Agent - Complete frontend assistant
- Backend Expert Agent - Backend API development
- Database Expert Agent - Database architecture and optimization
- UI/UX Expert Agent - User experience and design systems
- Fullstack Architecture Expert - System architecture and scalability
- (Future) DevOps Agent - Deployment and infrastructure

---

## How to Use Agents

### Activation

Agents activate automatically based on conversation context. Simply mention topics related to the agent's specialization:

**Frontend Expert Agent**:
```
"Create a component..."
"Build a page..."
"Make this responsive..."
"Review my code..."
```

### Interaction Patterns

**1. Ask for Components**
```
User: "Create a TodoCard component with title, description, priority badge, and complete button"
Agent: [Generates complete component with TypeScript, Tailwind, ShadCN, accessibility]
```

**2. Request Pages**
```
User: "Create a todo list page with filtering and search"
Agent: [Scaffolds complete page with state management, API integration, responsive design]
```

**3. Seek Guidance**
```
User: "What's the best way to handle form state in Next.js?"
Agent: [Explains options, provides examples, suggests best practices]
```

**4. Debug Issues**
```
User: "Why is this component re-rendering unnecessarily?"
Agent: [Analyzes code, identifies issue, provides fix with explanation]
```

**5. Review Code**
```
User: "Review this component for best practices and accessibility"
Agent: [Provides detailed review with suggestions and improvements]
```

---

## Directory Structure

```
.claude/agents/
├── README.md                          # This file (Agents registry)
├── frontend-expert-agent.md           # Frontend Expert Agent
├── backend-expert-agent.md            # Backend Expert Agent
├── database-expert-agent.md           # Database Expert Agent
├── ui-ux-expert-agent.md              # UI/UX Expert Agent
└── fullstack-architecture-expert.md   # Fullstack Architecture Expert
```

---

## Adding New Agents

To create a new agent:

1. **Create File**: `.claude/agents/my-agent.md`

2. **Add Content**:
   - Agent overview and capabilities
   - What the agent can do
   - Common patterns and solutions
   - Quick reference
   - Usage examples
   - Best practices

3. **Update this README** with agent information

---

## Best Practices for Working with Agents

### 1. Be Specific
```
❌ "Create a component"
✅ "Create a TodoCard component with title, description, priority badge, and complete button"
```

### 2. Provide Context
```
❌ "Fix this bug"
✅ "This component is re-rendering too often. Here's the code: [code]. How can I fix it?"
```

### 3. Ask for Explanations
```
✅ "Why is this the best approach?"
✅ "What are the trade-offs of this solution?"
✅ "Can you explain how this works?"
```

### 4. Request Reviews
```
✅ "Review this component for accessibility"
✅ "Is this code following Next.js best practices?"
✅ "Can this be optimized for performance?"
```

### 5. Iterate and Refine
```
✅ "This is good, but can you make it more accessible?"
✅ "Can we add error handling to this?"
✅ "How would this look on mobile?"
```

---

## Roadmap

**Planned Agents**:
- **DevOps Agent**: Deployment, CI/CD, monitoring
- **Testing Agent**: Unit tests, integration tests, E2E
- **Security Agent**: Security audit, best practices, vulnerability fixes

---

## Version History

- **2025-12-31**: Agents directory created
  - Frontend Expert Agent v1.0.0 - Full-stack frontend development assistant
  - Backend Expert Agent v1.0.0 - Production-grade backend development assistant
  - Database Expert Agent v1.0.0 - Database architecture and optimization expert
  - UI/UX Expert Agent v1.0.0 - User experience and design systems expert
  - Fullstack Architecture Expert v1.0.0 - System architecture and scalability expert

---

## License

All agents: MIT License

---

**Project**: Hackathon II Todo Application
**Branch**: 002-phase-ii-web-app
**Created**: 2025-12-31
**Agents Directory**: `.claude/agents/`
