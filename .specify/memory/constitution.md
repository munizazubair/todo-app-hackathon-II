# Hackathon II – Todo Application Constitution

<!--
SYNC IMPACT REPORT:
Version Change: INITIAL → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections: All sections (initial constitution)
Removed Sections: N/A

Templates Requiring Updates:
✅ .specify/templates/spec-template.md - Reviewed, no updates needed (generic requirements align)
✅ .specify/templates/plan-template.md - Reviewed, Constitution Check section present
✅ .specify/templates/tasks-template.md - Reviewed, aligns with phase-based execution
✅ .specify/templates/phr-template.prompt.md - Reviewed, stage-based routing aligns
✅ .specify/templates/adr-template.md - Reviewed, architecture decisions align

Follow-up TODOs: None
-->

## 1. Authority & Scope

This constitution is the **highest governing document** for the Hackathon II – Todo Application project, subordinate only to the authoritative reference file `Hackathon-II-Todo-App.md`.

**Authority Hierarchy:**
1. `Hackathon-II-Todo-App.md` (authoritative project context)
2. `.specify/memory/constitution.md` (this document)
3. Phase-specific specifications, plans, and tasks
4. All other project documentation and artifacts

**Scope of Application:**
- ALL hackathon phases (Phase I through Phase V)
- ALL AI agents (Claude, subagents, specialized agents, tools)
- ALL human participants (developers, reviewers, evaluators)
- ALL project outputs (code, documentation, artifacts, decisions)

**Binding Nature:**
- NO phase-specific specification, plan, task, or agent instruction may override this constitution
- Violations of constitutional principles constitute project non-compliance
- Deviations require explicit documentation and approval (see Section 8)

---

## 2. Phase Discipline Rules

### 2.1 Phase Integrity

Agents and participants MUST:
- Respect the five official hackathon phases as defined in `Hackathon-II-Todo-App.md`
- Complete each phase fully before proceeding to the next
- NOT skip, combine, or reorder phases without explicit approval
- NOT generate artifacts, code, or outputs belonging to future phases

### 2.2 Phase Isolation

**Phase I – In-Memory Python Console App**
- Technology Stack: Python, Claude Code, Spec-Kit Plus
- Output Directory: `/phase-I/`
- Scope: Console application with in-memory data only
- Prohibitions: NO web interfaces, NO databases, NO persistence

**Phase II – Full-Stack Web Application**
- Technology Stack: Next.js, FastAPI, SQLModel, Neon DB
- Output Directory: `/phase-II/`
- Scope: Web frontend + backend API + database persistence
- Prerequisites: Phase I complete and validated

**Phase III – AI-Powered Todo Chatbot**
- Technology Stack: OpenAI ChatKit, Agents SDK, Official MCP SDK
- Output Directory: `/phase-III/`
- Scope: Natural language conversational interface
- Prerequisites: Phase II complete and validated

**Phase IV – Local Kubernetes Deployment**
- Technology Stack: Docker, Minikube, Helm, kubectl-ai, kagent
- Output Directory: `/phase-IV/`
- Scope: Containerization and local orchestration
- Prerequisites: Phase III complete and validated

**Phase V – Advanced Cloud Deployment**
- Technology Stack: Kafka, Dapr, DigitalOcean DOKS
- Output Directory: `/phase-V/`
- Scope: Cloud-native deployment with event-driven architecture
- Prerequisites: Phase IV complete and validated

### 2.3 Phase Transition Gates

Before transitioning to a new phase, ALL of the following MUST be satisfied:
- Current phase objectives achieved per `Hackathon-II-Todo-App.md`
- Phase outputs written to the correct `/phase-*/` directory
- Phase validation completed (testing, review, documentation)
- Phase completion documented and approved
- Constitution compliance verified

### 2.4 Output Directory Discipline

Agents MUST:
- Write implementation outputs ONLY to the matching `/phase-*/` directory
- Write planning artifacts to `/.specify/phase-*/` subdirectories
- NOT mix phase-specific code or artifacts across directories
- Maintain clear separation between phase implementations

---

## 3. SpecKitPlus Operational Rules

### 3.1 SpecKitPlus Role and Boundaries

**What SpecKitPlus IS:**
- A methodology for disciplined software development
- A framework for specification, planning, and task management
- A tool to enforce constitution, prevent scope drift, and ensure quality

**What SpecKitPlus IS NOT:**
- A replacement for hackathon phases
- An override for hackathon phase names, boundaries, or requirements
- A permission to skip or modify official phase structure

### 3.2 Mandatory Pre-Action Reading

Before taking ANY action, agents MUST read and understand:
1. `/.specify/memory/constitution.md` (this file)
2. `Hackathon-II-Todo-App.md` (authoritative reference)
3. `/.specify/phase-*/specification.md` (current phase requirements)
4. `/.specify/phase-*/plan.md` (current phase technical plan)
5. `/.specify/phase-*/tasks.md` (current phase task breakdown)
6. `/.specify/phase-*/implementation-guidelines.md` (current phase guidance)

### 3.3 Protected Artifacts

Agents MUST NOT modify the following files without explicit human approval:
- `/.specify/memory/constitution.md`
- `/.specify/templates/*.md`
- `/.specify/scripts/bash/*.sh`
- `Hackathon-II-Todo-App.md`
- `CLAUDE.md`

Agents MAY create and modify:
- Phase-specific specifications, plans, tasks under `/.specify/phase-*/`
- Implementation code under `/phase-*/`
- Prompt History Records under `/history/prompts/`
- Architecture Decision Records under `/history/adr/`

### 3.4 SpecKitPlus Workflow Compliance

Agents MUST follow this workflow for each phase:

1. **Constitution Review** → Verify compliance principles
2. **Specification** → Define WHAT to build (requirements, user stories)
3. **Planning** → Define HOW to build (architecture, technology, structure)
4. **Task Breakdown** → Define WHO/WHAT builds (atomic, testable tasks)
5. **Implementation** → Execute tasks with validation
6. **Documentation** → Record decisions, prompts, architectural choices

Skipping steps or working out of order violates constitutional discipline.

---

## 4. AI Agent Behavior Rules

### 4.1 Respect Phase Boundaries

Agents MUST:
- Work ONLY within the current active phase
- NOT reference, import, or utilize artifacts from future phases
- NOT generate code that assumes future-phase capabilities
- Clearly identify the current phase in all outputs

Agents MUST NOT:
- Implement Phase II web features while in Phase I
- Assume database persistence in Phase I (in-memory only)
- Skip ahead to Kubernetes deployment before completing web application

### 4.2 Ask Before Acting

Agents MUST seek human approval before:
- Making architectural decisions with multiple valid approaches
- Choosing between technology alternatives within the approved stack
- Modifying project structure or directory layout
- Creating new abstractions, patterns, or design approaches
- Deviating from specifications or plans

Agents MUST explain:
- The decision being made
- Available options and their tradeoffs
- Recommended approach with rationale
- Impact on current and future phases

### 4.3 Never Assume Missing Requirements

When requirements, specifications, or context are unclear or incomplete, agents MUST:
- STOP execution immediately
- Document the ambiguity or gap
- Ask targeted clarification questions (2-5 specific questions)
- Wait for human input before proceeding

Agents MUST NOT:
- Invent APIs, endpoints, or data structures not specified
- Assume business logic or validation rules
- Create features not requested in the specification
- Fill gaps with "reasonable defaults" without approval

### 4.4 Prohibition on Hallucination

Agents MUST NOT:
- Invent tools, libraries, or APIs that do not exist
- Claim capabilities not verified in documentation
- Generate fictional code examples or patterns
- Reference non-existent files, functions, or modules
- Make up technology stack components outside approved list

Agents MUST verify:
- Library existence and compatibility with project stack
- API availability and correct usage
- File paths and module imports
- Technology versions and platform support

### 4.5 Transparency and Explanation

Agents MUST:
- Explain the purpose and impact of each action
- Provide rationale for technical decisions
- Document uncertainties and assumptions
- Report errors, blockers, and risks clearly
- Log significant actions in Prompt History Records (PHRs)

---

## 5. Output & Implementation Discipline

### 5.1 Code Quality Standards

Generated code MUST:
- Follow best practices for the defined technology stack
- Be readable, maintainable, and well-structured
- Include appropriate error handling for the complexity level
- Use clear, descriptive naming for functions, variables, classes
- Be documented where logic is non-obvious

Generated code MUST NOT:
- Include over-engineering or premature abstraction
- Add features or capabilities beyond requirements
- Implement patterns inappropriate for the current phase
- Contain hardcoded secrets, credentials, or sensitive data

### 5.2 Phase-Specific Output Requirements

**Phase I Outputs:**
- Python source files implementing console Todo application
- In-memory data structures (no files, no database)
- Clear command-line interface
- Input validation and error messages
- Documentation of usage and commands

**Phase II Outputs:**
- Next.js frontend application
- FastAPI backend with REST endpoints
- SQLModel database models
- Neon DB schema and migrations
- Integration between frontend and backend
- Deployment configuration

**Phase III Outputs:**
- OpenAI ChatKit integration
- Natural language processing for Todo commands
- Conversational interface implementation
- MCP SDK integration where applicable
- Chatbot testing and validation

**Phase IV Outputs:**
- Dockerfiles for all services
- Kubernetes manifests (deployments, services, configs)
- Helm charts for deployment
- Minikube setup and configuration
- Local cluster validation scripts

**Phase V Outputs:**
- Kafka event streaming configuration
- Dapr service-to-service communication
- DigitalOcean DOKS deployment manifests
- Cloud-native architecture implementation
- Production-ready operational configuration

### 5.3 Test and Validation Requirements

Each phase implementation MUST include:
- Validation that core requirements are met
- Testing appropriate to the phase complexity
- Error case handling and validation
- Documentation of testing approach
- Demonstration or proof of functionality

Tests MUST:
- Be written ONLY if explicitly requested in specifications
- Follow Test-Driven Development (TDD) if constitution or plan requires it
- Cover acceptance scenarios from user stories
- Be organized by user story for independent validation

### 5.4 Bonus Features Discipline

Bonus features (as defined in `Hackathon-II-Todo-App.md`) MUST be:
- Clearly identified as bonus/optional
- Implemented ONLY after core phase requirements complete
- Separated from core functionality (feature flags, separate modules)
- Documented with bonus designation
- Independently testable and removable

Bonus features MUST NOT:
- Block or delay core phase completion
- Create dependencies in core functionality
- Be intermingled with required features
- Compromise core feature stability

---

## 6. Agent Coordination & Safety

### 6.1 Multi-Agent Coordination

When multiple agents or subagents are active:
- Each agent MUST identify its scope and responsibilities
- Agents MUST NOT overwrite or conflict with each other's outputs
- Agents MUST coordinate on shared files through locking or sequencing
- Agents MUST log their actions for visibility and traceability

### 6.2 Action Logging and Transparency

Agents MUST log or explain:
- Files created, modified, or deleted
- Commands executed (with purpose)
- Decisions made (with rationale)
- Errors encountered (with context)
- Blockers or uncertainties (with recommendations)

Logs MUST be:
- Clear and human-readable
- Timestamped where appropriate
- Organized by phase and feature
- Accessible for review and audit

### 6.3 Error Handling and Reporting

When errors occur, agents MUST:
- Report the error clearly with context
- Explain the impact and severity
- Propose remediation options
- NOT silently fail or hide errors
- NOT make assumptions about recovery

Agents MUST stop execution when:
- Critical errors occur that block progress
- Requirements are fundamentally unclear
- Actions would violate constitution or specifications
- Risk of data loss or corruption exists

### 6.4 Unsafe Action Prevention

Agents MUST refuse to:
- Execute destructive operations without confirmation
- Modify protected files without approval
- Skip validation or safety checks
- Proceed with ambiguous or risky actions
- Override human decisions or instructions

---

## 7. Ethics, Security & Privacy

### 7.1 Secrets and Credentials Management

Agents MUST:
- Use environment variables (`.env` files) for all secrets
- Document required environment variables clearly
- Provide `.env.example` templates with dummy values
- NEVER commit `.env` files to version control

Agents MUST NOT:
- Hardcode API keys, passwords, or tokens in source code
- Log or display secrets in output or error messages
- Store credentials in configuration files committed to git
- Expose sensitive data in documentation or examples

### 7.2 Data Privacy and Mock Data

For development and testing, agents MUST:
- Use dummy, mock, or synthetic data
- NOT use real user data or personal information
- Generate realistic but fictional test datasets
- Document data generation approach

Agents MUST NOT:
- Request, store, or process real personal information
- Create realistic-looking data that could be confused with production data
- Include sensitive business logic or proprietary information

### 7.3 Scope Boundaries and Content Restrictions

Agents MUST:
- Work ONLY within hackathon project scope
- Focus on Todo application domain
- Respect project boundaries and phase limitations

Agents MUST NOT:
- Generate content unrelated to hackathon objectives
- Implement features outside project scope
- Introduce dependencies or technologies not in approved stack
- Create functionality that violates ethical guidelines

### 7.4 Security Best Practices

Implementations MUST:
- Validate and sanitize all user inputs
- Implement appropriate authentication/authorization for phase
- Use secure communication (HTTPS in web phases)
- Follow OWASP security guidelines for the technology stack
- Handle errors without exposing sensitive system information

Implementations MUST NOT:
- Allow SQL injection, XSS, or other injection attacks
- Expose internal system details in error messages
- Use deprecated or insecure libraries
- Implement weak or broken authentication mechanisms

---

## 8. Version Control & Change Management

### 8.1 Protected Artifacts Amendment Process

Changes to the following files require explicit human approval:
- `.specify/memory/constitution.md` (this document)
- `Hackathon-II-Todo-App.md`
- `CLAUDE.md`
- Any file in `/.specify/templates/`
- Any file in `/.specify/scripts/bash/`

Amendment process:
1. Agent proposes change with rationale and impact analysis
2. Human reviews and approves or rejects
3. If approved, agent creates ADR documenting the decision
4. Agent updates the artifact with version increment
5. Agent validates consistency across dependent artifacts
6. Agent creates PHR documenting the change

### 8.2 Constitution Versioning

This constitution follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Backward-incompatible changes (principle removal/redefinition)
- **MINOR**: New principles, sections, or material expansions
- **PATCH**: Clarifications, wording improvements, non-semantic fixes

Version changes MUST:
- Increment version number appropriately
- Update `LAST_AMENDED_DATE` to current date (YYYY-MM-DD format)
- Include Sync Impact Report as HTML comment
- Document rationale for version bump
- List all modified, added, or removed sections

### 8.3 Deviation Documentation

Any deviation from constitutional principles MUST be documented with:
- **Deviation Description**: What rule is being violated
- **Justification**: Why the deviation is necessary
- **Impact Analysis**: What risks or consequences exist
- **Mitigation Plan**: How risks will be managed
- **Approval**: Explicit human authorization
- **Expiration**: When deviation ends or is re-evaluated

Deviations MUST be recorded in:
- Architecture Decision Record (ADR) if architecturally significant
- Prompt History Record (PHR) for the action
- Phase-specific documentation

### 8.4 Git Workflow Discipline

Version control MUST follow these practices:
- Commit after each completed task or logical unit of work
- Use clear, descriptive commit messages
- Reference task IDs in commit messages
- Create branches per phase or feature as appropriate
- NEVER commit secrets, credentials, or `.env` files
- Tag phase completions for traceability

---

## 9. Documentation Requirements

### 9.1 Phase Completion Documentation

At the end of each phase, documentation MUST include:

**What Was Built:**
- Summary of implemented features and capabilities
- List of files and artifacts created
- Architecture and design decisions made
- Deviations from original plan (if any)

**How AI Agents Were Used:**
- Which agents/subagents were utilized
- What tasks each agent performed
- Prompts and interactions that shaped outcomes
- PHRs documenting significant exchanges

**Testing and Validation:**
- Test results and validation evidence
- Issues encountered and resolutions
- Performance or quality metrics (if applicable)

**Approved Deviations:**
- Any constitutional or specification deviations
- Rationale and approval documentation
- Impact assessment and mitigation

### 9.2 Prompt History Records (PHRs)

Agents MUST create PHRs for:
- Implementation work (code changes, new features)
- Planning and architecture discussions
- Debugging and problem-solving sessions
- Specification, task, or plan creation
- Multi-step workflows
- Significant decisions or clarifications

PHR Routing (all under `history/prompts/`):
- **Constitution-related** → `history/prompts/constitution/`
- **Feature-specific** → `history/prompts/<feature-name>/` (for spec, plan, tasks, implementation stages)
- **General/miscellaneous** → `history/prompts/general/`

PHRs MUST include:
- Full user input (verbatim, not truncated)
- Representative agent response
- Stage, title, date, and metadata
- Links to related specs, tasks, ADRs, or PRs
- Files created or modified
- Tests run or added

### 9.3 Architecture Decision Records (ADRs)

Agents MUST suggest ADR creation when:
- **Impact**: Decision has long-term consequences (framework, data model, API, security, platform)
- **Alternatives**: Multiple viable options were considered
- **Scope**: Decision is cross-cutting and influences system design

ADR suggestion format:
```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

Agents MUST:
- Wait for human consent before creating ADRs
- NEVER auto-create ADRs without approval
- Group related decisions into one ADR when appropriate
- Link ADRs from plans, tasks, and PHRs

ADRs MUST include:
- Context and problem statement
- Options considered with tradeoffs
- Decision made and rationale
- Consequences (positive and negative)
- Status (proposed, accepted, deprecated, superseded)

### 9.4 Technical Documentation Standards

All technical documentation MUST:
- Use Markdown format with clear headings and structure
- Include code examples where appropriate
- Provide setup and usage instructions
- Document dependencies and prerequisites
- Explain configuration and environment variables
- Be kept up-to-date with implementation changes

Documentation MUST be:
- Accurate and consistent with implementation
- Clear and accessible to target audience
- Organized logically by phase and feature
- Version-controlled alongside code

---

## Governance

### Compliance Verification

Constitution compliance MUST be verified:
- Before each phase transition
- During planning and task generation
- In code reviews and pull requests
- At project milestones and deliveries

Compliance verification includes:
- Phase discipline adherence
- Output directory correctness
- Security and privacy requirements
- Documentation completeness
- Quality standards fulfillment

### Amendment Authority

Only authorized humans may approve amendments to:
- This constitution
- Authoritative reference document (`Hackathon-II-Todo-App.md`)
- SpecKitPlus templates and workflows

Agents may propose amendments but MUST NOT implement without approval.

### Conflict Resolution

In case of conflicts or ambiguities:
1. `Hackathon-II-Todo-App.md` has ultimate authority
2. This constitution takes precedence over all other project documents
3. Explicit human decisions override all automated processes
4. When in doubt, ask for clarification rather than assume

### Enforcement

Violations of this constitution:
- MUST be documented and reported
- May result in work being rejected or redone
- Could impact hackathon evaluation and scoring
- Require corrective action and compliance verification

### Success Criteria

The project succeeds when:
- All five hackathon phases meet their technical goals
- Technology stack requirements are fully respected
- Architecture evolves cleanly and coherently across phases
- AI agent usage is disciplined, documented, and effective
- Bonus features (if implemented) are correctly integrated
- Constitutional principles are consistently upheld

---

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
