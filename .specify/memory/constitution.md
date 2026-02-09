<!--
Sync Impact Report:
Version change: N/A → 1.0.0 (initial version based on user input)
Modified principles: None (new constitution)
Added sections: Core Principles, Phase-Specific Standards, Documentation Standards, Code Quality Rules, Security Rules, Evaluation Criteria, Non-Negotiables
Removed sections: None (new constitution)
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
  - README.md ⚠ pending
Follow-up TODOs: None
-->
# End-to-End AI-Native Application Development Constitution

## Core Principles

### Correctness Over Speed
All implementations must work as specified. No placeholder logic in final submissions. Errors must be handled explicitly.
<!-- Rationale: Ensuring high-quality deliverables that meet specifications rather than rushing to completion -->

### Phase Isolation
Each phase must be independently runnable. Later phases may extend earlier ones, but must not break them. Clear documentation of phase boundaries.
<!-- Rationale: Maintaining modularity and allowing for incremental development and testing -->

### Reproducibility
Anyone should be able to run the project by following README steps. Environment variables, dependencies, and setup must be documented. No hidden configuration.
<!-- Rationale: Ensuring that the project can be consistently reproduced by others -->

### AI-Assisted, Human-Verified Development
AI tools (Claude, OpenAI, MCP, Agents SDK) may assist. All generated code must be reviewed, understood, and validated. No blind copy-paste without comprehension.
<!-- Rationale: Leveraging AI assistance while maintaining human oversight and understanding -->

### Production Mindset
Clean folder structure. Clear naming conventions. Secure handling of secrets. Scalable design where applicable.
<!-- Rationale: Building applications with production readiness in mind from the start -->

## Phase-Specific Standards

### Phase I: In-Memory Python Console App
**Tech Stack**: Python, Claude Code, Spec-Kit Plus

**Standards**:
- Pure in-memory data structures (no DB)
- Clear CLI-based interaction
- Modular Python files (no monolith scripts)
- Type hints preferred
- Input validation required

**Success Criteria**:
- App runs from terminal without errors
- Core logic works correctly
- Code is readable and documented

### Phase II: Full-Stack Web Application
**Tech Stack**: Next.js, FastAPI, SQLModel, Neon DB (PostgreSQL)

**Standards**:
- Proper REST or API-layer separation
- Backend handles all business logic
- Frontend is UI-only (no DB logic)
- SQLModel models must match DB schema
- Environment variables stored in `.env` (never committed)

**Success Criteria**:
- Frontend and backend communicate correctly
- Data persists in Neon DB
- API endpoints documented
- App runs locally and in production mode

### Phase III: AI-Powered Todo Chatbot
**Tech Stack**: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK

**Standards**:
- Agent logic separated from UI
- Tools must have clear input/output contracts
- Prompt engineering documented
- Context handling must be explicit (no hidden state)

**AI Ethics & Safety**:
- No hallucinated responses for system data
- Agent must admit uncertainty when unsure
- User data must not be leaked across sessions

**Success Criteria**:
- Chatbot performs task-oriented actions correctly
- Tools are invoked intentionally
- Agent behavior is predictable and explainable

### Phase IV: Local Kubernetes Deployment
**Tech Stack**: Docker, Minikube, Helm, kubectl-ai, kagent

**Standards**:
- Each service has its own Dockerfile
- Kubernetes manifests are valid and minimal
- Helm charts parameterized (values.yaml)
- No hardcoded ports or secrets

**Success Criteria**:
- App runs fully on Minikube
- Services communicate inside the cluster
- Logs are accessible
- Pods restart correctly without failure

### Phase V: Advanced Cloud Deployment
**Tech Stack**: Kafka, Dapr, DigitalOcean Kubernetes (DOKS)

**Standards**:
- Event-driven communication via Kafka
- Dapr used for:
  - Service discovery
  - State management
  - Pub/Sub
- Cloud resources documented with costs in mind

**Success Criteria**:
- App successfully deployed on DOKS
- Kafka events flow correctly
- Dapr sidecars function as intended
- System is scalable and observable

## Documentation Standards

- Each phase must include a README section
- Architecture diagrams encouraged
- API contracts documented
- Commands must be copy-paste runnable
- Errors and limitations clearly stated

## Code Quality Rules

- No commented-out dead code
- No unused dependencies
- Consistent formatting
- Meaningful commit messages
- Clear folder structure

## Security Rules

- Secrets must never be committed
- `.env.example` required
- Production configs separated from local configs
- Basic input sanitization required

## Evaluation Criteria

A phase is considered **complete** only if:
- It runs without errors
- It meets all phase-specific standards
- It is documented clearly
- The developer can explain **why** each major decision was made

## Final Success Definition

The project is successful if:
- All 5 phases are completed
- The system evolves logically across phases
- AI is used responsibly and transparently
- The final system demonstrates real-world engineering maturity

## Non-Negotiables

- ❌ No fake implementations
- ❌ No skipped phases
- ❌ No undocumented shortcuts
- ❌ No unverified AI output

## Governance

This constitution serves as the governing document for the hackathon project. All development activities must comply with these principles and standards. Any deviations must be documented and justified. The constitution may be amended through a formal process that includes community review and approval.

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15
