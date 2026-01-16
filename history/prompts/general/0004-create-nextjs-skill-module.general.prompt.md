---
id: 0004
title: create-nextjs-skill-module
stage: general
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-phase-ii-web-app
user: SIBGHAT
command: /sp.skills
labels: ["skills", "nextjs", "claude-code", "phase-ii", "scaffolding"]
links:
  spec: specs/002-phase-ii-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/nextjs-skill/SKILL.md
  - .claude/skills/nextjs-skill/SCAFFOLDING.md
  - .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py
  - .claude/skills/nextjs-skill/scripts/generate-component.py
tests:
  - Skill structure validated (SKILL.md with metadata exists)
  - Directory structure created successfully
  - Supporting documentation complete
  - Utility scripts functional
---

## Prompt

/sp.skills I want to create the NextJSSkill module directly (Option 2)

## Response snapshot

Created comprehensive NextJSSkill for Claude Code to assist with Phase II Next.js frontend development:

**Skill Structure**:

1. **SKILL.md** (682 lines):
   - Metadata: name, description, allowed-tools, model
   - Description triggers: "scaffold", "Next.js", "Phase II", "routing", "API routes"
   - Complete integration with Phase II specification
   - TypeScript interfaces matching backend schema (FR-026)
   - API client implementation for all 7 FastAPI endpoints
   - Client-side validation with Zod (mirrors Phase I rules)
   - Component templates: TodoList, TodoItem, TodoForm, FilterBar, SearchBar
   - Configuration examples: next.config.js, tailwind.config.ts, .env.local
   - Root layout and homepage implementations
   - Success criteria checklist from spec.md

2. **SCAFFOLDING.md** (518 lines):
   - Step-by-step project initialization guide
   - Prerequisites checklist (Node.js 18+, npm, git)
   - Complete setup commands with explanations
   - Dependency installation and justification
   - Directory structure creation
   - Configuration file templates
   - Verification steps and troubleshooting
   - Post-setup tasks and next steps

3. **Utility Scripts**:
   - `validate-nextjs-setup.py`: Validates Phase II compliance
     - Checks required files (package.json, next.config.js, tsconfig.json, tailwind.config.ts)
     - Validates directory structure (app/, components/, lib/, types/, public/)
     - Verifies component files (TodoList, TodoItem, TodoForm, FilterBar, SearchBar)
     - Checks dependencies (Next.js 14+, React 18+, TypeScript, Tailwind, axios)
     - Validates App Router structure (layout.tsx, page.tsx, dashboard/)
     - Checks environment variables (NEXT_PUBLIC_API_URL)
     - Color-coded output with errors, warnings, and success messages

   - `generate-component.py`: Generates React component boilerplate
     - Supports server and client components
     - TypeScript interfaces with props
     - Customizable target directory
     - Proper PascalCase validation
     - Interactive overwrite confirmation

**Skill Capabilities**:

- Automatic activation when discussing Next.js, Phase II, scaffolding, or routing
- Provides Phase II-specific guidance aligned with spec.md requirements
- Component mapping from Phase I to Phase II (CLI → React components)
- API integration patterns for FastAPI backend
- Validation that mirrors Phase I business logic
- Responsive design guidance (mobile 320px to desktop 1920px)
- Error handling with toast notifications
- Loading states and user feedback
- Dashboard with statistics (FR-012)

**Constitutional Compliance**:

- Enforces Phase II boundaries (no Phase III+ features)
- Technology stack matches Hackathon-II-Todo-App.md specification
- Output directory: `/phase-II/frontend/`
- Security: client-side validation, environment variables, CORS awareness
- PHR creation workflow followed

## Outcome

- ✅ Impact: NextJSSkill created and ready for activation. Will guide Phase II frontend implementation with spec-aligned scaffolding, component generation, and validation.
- 🧪 Tests: Skill structure validated (SKILL.md format correct, metadata complete, supporting files functional)
- 📁 Files: Created 4 files (SKILL.md: 682 lines, SCAFFOLDING.md: 518 lines, 2 Python scripts)
- 🔁 Next prompts: Test skill activation by asking "How do I scaffold the Phase II Next.js frontend?" or proceed with `/sp.tasks` to generate Phase II task breakdown
- 🧠 Reflection: Skill successfully created with comprehensive Phase II context, component templates, and validation scripts. Ready to accelerate frontend development while maintaining spec compliance.

## Evaluation notes (flywheel)

- Failure modes observed: None - clean skill creation following Claude Code documentation
- Graders run and results (PASS/FAIL): Manual validation - PASS (SKILL.md structure correct, scripts functional, documentation complete)
- Prompt variant (if applicable): Direct skill creation request via `/sp.skills` command
- Next experiment (smallest change to try): Test skill activation in new session or proceed to Phase II implementation with skill assistance
