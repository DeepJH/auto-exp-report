# Auto Exp Report Domain Model

A multi-agent autonomous engineering workflow system for university engineering lab reports, executing a disciplined three-phase pipeline with strict verification gates.

## Language

### Core Lifecycle

**Single Source of Truth (SSoT)**:
The official course lab manual and official Word report template located in `<course>/resource/`. All report structure and task scope are strictly derived from this source.
_Avoid_: User prompts as spec, arbitrary requirements, hallucinated sections

**Exp Context**:
The isolated filesystem directory `<course>/exps/<N>/` where all inputs, intermediate artifacts, and outputs for a specific experiment reside.
_Avoid_: Global workspace, shared cache

**Three-Phase Collaboration Model**:
The strict lifecycle dividing autonomous code/draft generation (Phase 1), screenshot & assembly handoff (Phase 2), and clean package release (Phase 3).
_Avoid_: End-to-end unverified run, premature archiving

**Phase 1 (Autonomous Research & Drafting)**:
The fully automated phase where subagents reverse-engineer templates, implement code, measure real benchmarks, draft reports, and compile to `report.docx`.
_Avoid_: Full completion, auto-submitting

**Phase 2 (Screenshot & Assembly)**:
The human-in-the-loop stage where real screenshots are captured on target environments and assembled into the official Word template; designed for future Computer Use automation.
_Avoid_: Fake screenshots, synthetic image injection

**Phase 3 (Clean Delivery & Release)**:
The automated delivery stage verifying the completed docx, producing cache-free archive zip, syncing Git commits, and publishing a GitHub Release with assets.
_Avoid_: Dirty build, unpushed tag release

### Agents

**Orchestrator**:
The overarching state-machine coordinator that enforces phase gates, triggers subagents, and manages handoff checkpoints.
_Avoid_: Mega-prompt runner, monolithic agent

**Inspector**:
The subagent responsible for reverse-engineering the official Word template structure and extracting `guide.md`.
_Avoid_: Generic parser, template hallucinator

**Engineer**:
The subagent that writes minimal, self-contained implementation code and line-level I/O test cases in `src/`.
_Avoid_: Over-engineered framework, unrequested bonus implementations

**Tester & Measurer**:
The subagent that executes tests, measures real nanosecond/millisecond benchmarks, and records output into `measurements.json`.
_Avoid_: Synthetic metric faker, random number generator

**Writer**:
The subagent that authors the initial structured Markdown report draft (`report.raw.md`) strictly mirroring the template outline with screenshot placeholders.
_Avoid_: Creative embellisher, prompt-meta leaker

**Humanizer**:
The subagent dedicated to rewriting subjective reflection and debugging sections into a natural student voice, eliminating academic AI jargon, and validating Pandoc AST tables.
_Avoid_: Prompt polishing tool, robotic rephraser

**Assembler**:
The bridge agent managing the Phase 2 contract (providing test execution lists and template paths to the user; asserting final docx validity upon resume; future Computer Use host).
_Avoid_: Blind packager, Word bypasser

**Releaser**:
The subagent handling cache-free zip packaging, Git synchronisation, and GitHub Release asset creation with filename normalization hints.
_Avoid_: Manual uploader, local-only archiver

### Mechanics & Safety

**Table AST Assertion**:
A deterministic Python check validating that compiled `report.docx` files contain native Word tables (>= 2) and zero raw Markdown pipe characters (`|`).
_Avoid_: Visual check, trusting Pandoc exit code

**Clean Archive**:
A zip package containing only pure source code and the final Word report, explicitly excluding `__pycache__`, `.pyc`, and build caches.
_Avoid_: Dirty zip, raw directory dump

**Rename Notice Block**:
A prominent code-block warning placed at the very top of GitHub Release notes detailing the exact Chinese filenames for assets truncated by platform ASCII limits.
_Avoid_: Silent truncation, unnotified asset loss

**Privacy Guard**:
The zero-leakage security boundary enforcing dummy mock data in tracked repository files, isolating real student credentials in `*.local.*`, and blocking commits containing sensitive data.
_Avoid_: Hardcoded identity, trusting private repo privacy
