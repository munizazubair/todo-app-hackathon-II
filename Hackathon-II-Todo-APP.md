# Hackathon II – Todo Application  
Authoritative Project Context (Claude + SpecKitPlus Reference)

---

## 1. Purpose of This Document

This file (`Hackathon-II-Todo-App.md`) is the **single source of truth** for the
Hackathon II Todo Application project.

It exists to:
- Provide **official hackathon context**
- Define **phases, timelines, and expectations**
- Guide **AI-assisted development** using Claude + SpecKitPlus
- Prevent hallucination, scope drift, and phase confusion

Any AI agent or tool must **read and follow this file before acting**.

---

## 2. Hackathon Overview

Hackathon II is a **multi-phase, progressively complex project**
focused on building a Todo system from a simple console app to a
cloud-native, AI-powered platform.

Evaluation is based on:
- Correct implementation per phase
- Technical depth
- Architecture decisions
- Proper use of AI tooling
- Clean execution and documentation

---

## 3. OFFICIAL Hackathon Phases (Authoritative)

> ⚠️ These phases are fixed, graded, and must NOT be altered or renamed.

### Phase I — In-Memory Python Console App
- **Technology Stack:** Python, Claude Code, Spec-Kit Plus
- **Description:**  
  Build a basic Todo application running in the console using in-memory data.
  Focus is on logic, structure, and clarity — not persistence or UI.
- **Points:** 100
- **Due Date:** Dec 7, 2025

---

### Phase II — Full-Stack Web Application
- **Technology Stack:** Next.js, FastAPI, SQLModel, Neon DB
- **Description:**  
  Convert the Todo system into a full-stack web application with:
  - Frontend UI
  - Backend API
  - Database persistence
- **Points:** 150
- **Due Date:** Dec 14, 2025

---

### Phase III — AI-Powered Todo Chatbot
- **Technology Stack:** OpenAI ChatKit, Agents SDK, Official MCP SDK
- **Description:**  
  Add conversational interaction to the Todo system.
  Users should be able to manage todos using natural language.
- **Points:** 200
- **Due Date:** Dec 21, 2025

---

### Phase IV — Local Kubernetes Deployment
- **Technology Stack:** Docker, Minikube, Helm, kubectl-ai, kagent
- **Description:**  
  Containerize and deploy the system locally using Kubernetes.
  Focus is on orchestration, service separation, and operational readiness.
- **Points:** 250
- **Due Date:** Jan 4, 2026

---

### Phase V — Advanced Cloud Deployment
- **Technology Stack:** Kafka, Dapr, DigitalOcean DOKS
- **Description:**  
  Deploy the system to the cloud with:
  - Event-driven architecture
  - Service communication via Dapr
  - Managed Kubernetes
- **Points:** 300
- **Due Date:** Jan 18, 2026

---

### Total Base Points: **1000**

---

## 4. Bonus Points (Optional)

Participants may earn additional points by implementing advanced features.

| Bonus Feature | Points |
|---------------|--------|
| Reusable Intelligence using Claude Code Subagents & Agent Skills | +200 |
| Cloud-Native Blueprints via Agent Skills | +200 |
| Multi-language Support (Urdu chatbot support) | +100 |
| Voice Commands for Todo operations | +200 |
| **Total Possible Bonus** | **+600** |

---

## 5. Role of SpecKitPlus (IMPORTANT)

SpecKitPlus is a **methodology**, not a replacement for hackathon phases.

It is used **inside each Hackathon phase** to enforce:
- Constitution (rules & constraints)
- Specification (what must be built)
- Planning (how it will be built)
- Tasks & agents (who/what builds it)
- Implementation discipline

SpecKitPlus **must not rename or override** Hackathon phases.

---

## 6. Expected Project Directory Structure

High-level structure:

/Hackathon-II-Todo-App/
│
│
├─ /.claude/
│   └─ agents-and-skills.md      # Define all agents and skills Claude can use
│
├─ /.specify/
│   ├─ /memory/
│   │  └─ constitution.md           # Global constitution for all phases
│   ├─ /phase-I/
│   │   ├─ specification.md
│   │   ├─ plan.md
│   │   ├─ tasks.md
│   │   └─ implementation-guidelines.md
│   ├─ /phase-II/
│   │   ├─ specification.md
│   │   ├─ plan.md
│   │   ├─ tasks.md
│   │   └─ implementation-guidelines.md
│   ├─ /phase-III/
│   │   └─ ... same structure
│   ├─ /phase-IV/
│   │   └─ ... same structure
│   └─ /phase-V/
│       └─ ... same structure
│
├─ /phase-I/                     # Output/implementation for Phase I
│   └─ ... generated code/files
├─ /phase-II/                    # Output/implementation for Phase II
│   └─ ...
├─ /phase-III/
│   └─ ...
├─ /phase-IV/
│   └─ ...
├─ /phase-V/
│   └─ ...
│
├─ CLAUDE.md                     # Main instructions for Claude
└─ hackathon-II-todo-app.md      # Authoritative hackathon context


Each `/phase-*` directory corresponds **exactly** to the official Hackathon phase.

SpecKitPlus artifacts (constitution, specs, plans, tasks) may live inside
or be referenced by these phase directories.

---

## 7. AI Usage Rules (Claude / Agents)

AI tools must:
- Treat this file as **authoritative**
- Respect hackathon phase boundaries
- Never jump ahead to future phases
- Never assume missing requirements
- Ask before making architectural decisions
- Use SpecKitPlus to **control**, not accelerate blindly

Violation of these rules risks **point loss**.

---

## 8. Success Criteria

The project is successful if:
- Each phase meets its technical goals
- Stack requirements are respected
- Architecture evolves cleanly phase-to-phase
- AI usage is disciplined and documented
- Bonus features (if any) are correctly integrated

---

## 9. Authority Clause

If there is any conflict between:
- AI output
- Generated plans
- Agent behavior
- Other documents

👉 **This file (`Hackathon-II-Todo-App.md`) takes priority.**
