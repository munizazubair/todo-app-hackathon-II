---
id: 0001
title: Create Global Project Constitution
stage: constitution
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: MUNIZA
command: /sp.constitution
labels: ["constitution", "governance", "hackathon", "project-setup", "phase-discipline"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - No tests (governance document)
---

## Prompt

You are creating the **GLOBAL CONSTITUTION** for the project:

Hackathon II – Todo Application

You MUST use the following file as the **authoritative reference**:
- `Hackathon-II-Todo-App.md`

This constitution will be stored at:
- `/memory/constitution.md`

---

## PURPOSE

This document defines the **highest-level rules and constraints** for the entire project.

It applies to:
- ALL hackathon phases (Phase I – Phase V)
- ALL AI agents (Claude, sub-agents, tools)
- ALL human participants

NO phase-specific specification, plan, task, or agent instruction is allowed to override this constitution.

---

## SCOPE REQUIREMENTS

The constitution MUST:

- Be **global** (valid across all phases)
- Enforce **phase discipline**
- Prevent hallucination, scope drift, and premature execution
- Define how AI agents interact with SpecKitPlus
- Define how outputs are structured and validated
- Be readable and enforceable by both humans and AI agents

---

## REQUIRED SECTIONS (MANDATORY)

Generate the constitution with the following sections and rules:

### 1. Authority & Scope
- Declare this file as the **highest authority** after `Hackathon-II-Todo-App.md`
- State that all agents and participants must obey it

### 2. Phase Discipline Rules
- Agents MUST NOT skip phases
- Agents MUST NOT generate future-phase outputs
- Each phase MUST be completed and validated before moving forward
- Outputs must be written only to their matching `/phase-*` directory

### 3. SpecKitPlus Operational Rules
- Agents MUST read:
  - `/.specify/phase-*/specification.md`
  - `plan.md`
  - `tasks.md`
  - `implementation-guidelines.md`
  BEFORE acting
- Agents MUST NOT modify files in `/.specify/` or `/memory/` without approval
- SpecKitPlus is a methodology and MUST NOT rename or override hackathon phases

### 4. AI Agent Behavior Rules
- Agents MUST:
  - Respect phase boundaries
  - Ask before making architectural decisions
  - Never assume missing requirements
- Agents MUST:
  - Explain uncertainties
  - Request clarification when required
- Agents MUST NOT hallucinate tools, APIs, or requirements

### 5. Output & Implementation Discipline
- Generated code must:
  - Follow best practices for the defined tech stack
  - Be clean, readable, and documented
- Each phase output must:
  - Match its specification
  - Be isolated from other phases
- Bonus features MUST be optional and clearly separated

### 6. Agent Coordination & Safety
- Multiple agents MUST NOT overwrite each other's outputs
- Agents MUST log or explain their actions
- Errors must be reported clearly
- Unsafe or ambiguous actions MUST stop execution

### 7. Ethics, Security & Privacy
- No secrets, credentials, or API keys in outputs
- Use dummy or mock data when required
- No content outside hackathon scope

### 8. Version Control & Change Management
- Any change to:
  - `/memory/constitution.md`
  - `/.specify/`
  requires explicit approval
- Deviations must be documented

### 9. Documentation Requirements
- Each phase must include:
  - What was built
  - How agents were used
  - Any approved deviations

---

## FORMAT RULES

- Markdown format ONLY
- Clear headings and subheadings
- Bullet points for rules
- Concise, strict, and authoritative tone
- No assumptions beyond `Hackathon-II-Todo-App.md`

---

## FINAL GOAL

The generated `/memory/constitution.md` must function as:
- The **global rulebook**
- A **guardrail against AI misuse**
- A **single source of truth** for disciplined execution

Generate the full constitution now.

## Response snapshot

Created comprehensive global constitution for Hackathon II Todo Application project at `.specify/memory/constitution.md` (Version 1.0.0).

The constitution includes 9 major sections:

1. **Authority & Scope** - Establishes constitution as highest authority after Hackathon-II-Todo-App.md
2. **Phase Discipline Rules** - Enforces strict phase isolation and transition gates for all 5 phases
3. **SpecKitPlus Operational Rules** - Defines methodology boundaries and mandatory pre-action reading
4. **AI Agent Behavior Rules** - Prohibits hallucination, requires clarification, enforces transparency
5. **Output & Implementation Discipline** - Phase-specific requirements, code quality, bonus features
6. **Agent Coordination & Safety** - Multi-agent coordination, logging, error handling
7. **Ethics, Security & Privacy** - Secrets management, mock data, security best practices
8. **Version Control & Change Management** - Protected artifacts, semantic versioning, deviation documentation
9. **Documentation Requirements** - PHRs, ADRs, phase completion docs, technical standards

All sections are written as enforceable MUST/MUST NOT rules with clear consequences. The constitution prevents scope drift, phase jumping, and hallucination while enabling disciplined AI-assisted development.

Sync Impact Report included as HTML comment showing all templates reviewed and validated for consistency.

## Outcome

- ✅ Impact: Created foundational governance document that will control all AI agent behavior across 5 hackathon phases
- 🧪 Tests: No tests required (governance document, not executable code)
- 📁 Files: Created 1 file (.specify/memory/constitution.md, 635 lines)
- 🔁 Next prompts: Phase I specification creation (/sp.specify for Phase I requirements)
- 🧠 Reflection: Constitution successfully establishes clear authority hierarchy, prevents common AI failure modes (hallucination, scope drift, phase confusion), and provides enforceable rules for disciplined development

## Evaluation notes (flywheel)

- Failure modes observed: None (initial creation)
- Graders run and results (PASS/FAIL): Manual review - PASS (all sections complete, no placeholder tokens remaining)
- Prompt variant (if applicable): N/A (initial creation)
- Next experiment (smallest change to try): Monitor constitution effectiveness during Phase I spec/plan/tasks creation and adjust if ambiguities emerge
