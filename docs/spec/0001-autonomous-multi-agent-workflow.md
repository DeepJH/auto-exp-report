# Spec: Autonomous Multi-Agent Lab Report Workflow (auto-exp-report)

## Problem Statement

University engineering students spend excessive time and effort manually formatting, reverse-engineering, and generating academic lab reports from official Word templates and course manuals. 

When attempting to automate this process using LLMs, students encounter recurrent pain points:
1. **Context and Instruction Leaks**: Prompts and meta-instructions (e.g. `[code placeholder]`) inadvertently leak into final academic report sections.
2. **Template Misalignment & Hallucinated Sections**: Monolithic prompts hallucinate extraneous thinking questions or omit mandatory template sections.
3. **Broken Formatting & False Pass Assertions**: Markdown pipe tables silently degrade into plain text paragraphs during Pandoc Word export when blank lines are missing, leading to broken formatting that requires manual fixing.
4. **Fictitious Data**: Language models fabricate benchmark numbers rather than measuring actual runtime performance.
5. **Inability to Automate Real Screenshots**: Models cannot reliably screenshot physical development boards (like ESP32) or local interactive terminal runs without human intervention, leading to awkward, broken automation.
6. **Privacy Risk in Public Repositories**: Automations frequently lead students to commit real personal credentials (student ID, real name) to public git repositories.
7. **Environment & Shell Discrepancies**: While Linux shell environments are unified and ergonomic, PowerShell carries historical baggage with syntax that is idiosyncratic and verbose. Furthermore, modern Linux distributions enforce PEP 668 (`externally-managed-environment`), causing raw `pip install` commands to fail without a virtual environment.

## Solution

An autonomous multi-agent engineering workflow powered natively by Google Antigravity (`agy`) that executes a disciplined three-phase collaboration lifecycle:

### Tech Stack
- **Core Automation & Inspection Utilities**: Python 3.10+ (`python-docx` for template parsing & validation, `pyyaml` for configuration).
- **Environment & Lifecycle Management**: POSIX Bash Shell (Linux-native only; Windows users run via WSL2 Ubuntu).
- **Compilation Engine**: Pandoc (Markdown to `.docx`).
- **Orchestration Layer**: Antigravity (`agy`) Subagent Skills & Workflows.
- **VCS & Delivery**: Git + GitHub CLI (`gh`).

### Three-Phase Lifecycle
1. **Phase 1 (Autonomous Research & Drafting)**: 
   - An Inspector Agent parses the official Word template and course manual into a `guide.md` Single Source of Truth (SSoT) and copies a blank template.
   - An Engineer Agent implements standalone code and deterministic line-level I/O test cases.
   - A Tester Agent executes tests against the local host environment and records real nanosecond/millisecond execution data and raw stdout logs.
   - A Writer Agent authors the initial structured Markdown draft strictly mirroring the template outline, with explicit screenshot placeholders and factual component explanations.
   - A dedicated Humanizer Agent rewrites subjective reflections, debugging takeaways, and summaries into a genuine, unpretentious undergraduate voice (eliminating robotic AI jargon), compiles the draft to Word, and validates table AST integrity.
   - Phase 1 terminates unconditionally at `report.docx`, preventing premature packaging.
2. **Phase 2 (Screenshot & Assembly Handoff)**:
   - An Assembler Agent generates an execution manifest instructing the student which commands to run and where to paste screenshots into the official template.
   - The workflow halts safely and yields control to the student.
   - Upon resumption, the Assembler verifies final report file existence and size (>100KB) to confirm embedded imagery before advancing.
   - This phase is explicitly designed with a clean contract to be seamlessly automated by a Computer Use Agent in the future.
3. **Phase 3 (Clean Delivery & Release)**:
   - A Releaser Agent packages the source code and final docx into a clean zip archive (strictly excluding build and Python bytecode caches).
   - The agent synchronizes git branches and publishes a GitHub Release with dual asset attachments and a prominent Chinese filename rename warning block.
4. **Linux-Only Platform Boundary & PEP 668 Compliant Setup**:
   - Includes a deterministic `scripts/setup.sh` that checks/installs dependencies (`pandoc`, `python3`, `gh`).
   - Automatically initializes a standard Python virtual environment (`.venv/`) to comply with PEP 668 (preventing `externally-managed-environment` errors on modern Ubuntu/Debian).
   - Accurately guides Windows users to WSL2:
     *"💡 检测到 Windows 原生环境：Linux 的 Shell 统一简洁好用，而 PowerShell 带有历史包袱，语法相对诡异冗杂。用 PowerShell 只会害了你 [doge]，强烈推荐移步 WSL2 (Ubuntu)！"*
5. **Privacy Isolation**:
   - Repository-tracked configuration uses YAML populated exclusively with mock dummy data. Real personal credentials are isolated locally via `.gitignore`.

## User Stories

1. As an engineering student on Linux or WSL2, I want to run a single setup command `bash scripts/setup.sh`, so that all necessary system tools (`pandoc`, `gh`) and a PEP 668-compliant Python virtual environment (`.venv/`) are configured automatically without breaking system packages.
2. As a Windows user, I want the setup script to detect native Windows/PowerShell and guide me to install WSL2 Ubuntu, explaining factually that Linux shell is unified and ergonomic whereas PowerShell carries historical baggage with idiosyncratic and verbose syntax ("用 PowerShell 只会害了你 [doge]").
3. As an engineering student, I want to initiate a complete lab workflow using a single command `/auto-exp <course> <exp_num>`, so that I do not need to manually configure separate agent prompts for each task.
4. As a student, I want the system to parse my course lab manual and official Word template into a single authoritative guide, so that the report structure strictly matches the teacher's grading expectations.
5. As a student, I want the system to ignore unrequested sections (like thinking questions when absent from the template), so that my submission does not contain extraneous or unauthorized content.
6. As a student, I want the engineer agent to write minimal, self-contained code in a dedicated source directory, so that my implementation is modular and easy to debug.
7. As a student, I want deterministic line-level input and output test cases, so that my algorithm can be verified with standard I/O redirection without manual intervention.
8. As a student, I want the tester agent to execute the implementation on my host machine and record real benchmark measurements, so that my report contains genuine experimental timing and terminal output rather than fabricated numbers.
9. As a student, I want the writer agent to mirror the template's exact heading hierarchy, so that the generated report aligns perfectly with the grading rubric.
10. As a student, I want the writer agent to insert explicit, standardized screenshot placeholders, so that I immediately know where to paste terminal or hardware images during assembly.
11. As a student, I want the writer agent to describe hardware component substitutions factually, so that the report accurately reflects my bench setup without inventing subjective student attitudes.
12. As a student, I want the writer agent to be strictly barred from leaking prompt meta-instructions into the text, so that the report appears professional and ready for grading.
13. As a student, I want a dedicated humanizer agent to review and rewrite subjective reflection and debugging sections, so that the tone sounds like a genuine, hardworking undergraduate student rather than generic AI slop.
14. As a student, I want the humanizer agent to compile the report to Word using Pandoc and execute an automated Python AST assertion, so that silent table formatting degradation is detected and resolved immediately.
15. As a student, I want the workflow to unconditionally halt after compiling `report.docx` in Phase 1, so that unverified draft code is never prematurely packaged or submitted.
16. As a student in Phase 2, I want the assembler agent to output a structured execution checklist detailing the exact commands to run and screenshots to capture, so that I can complete physical bench work efficiently.
17. As a student, I want the assembler agent to validate that my assembled Word report exists and exceeds the minimum size threshold before moving forward, so that I do not accidentally publish an incomplete report lacking screenshots.
18. As an agent developer, I want the assembler agent to expose a standardized JSON contract for Phase 2 tasks, so that I can later replace the human step with a Computer Use Agent without modifying any other part of the pipeline.
19. As a student in Phase 3, I want the releaser agent to package my verified source code and final Word report into a zip archive that explicitly excludes Python bytecode and temporary caches, so that my submission remains clean and professional.
20. As a student, I want the releaser agent to verify that the local git repository is clean and pushed to the remote repository before creating a release, so that the release tag points to the exact commit containing my code.
21. As a student, I want the releaser agent to create a GitHub Release with both the pure zip archive and standalone Word report attached, so that my instructor or classmates can easily download either asset.
22. As a student, I want the GitHub Release notes to feature a prominent code block with full Chinese filenames, so that I can quickly restore ASCII-truncated download names.
23. As an open-source contributor, I want all configuration files tracked in git to use mock dummy data, so that cloning the public repository never exposes private personal credentials.
24. As an open-source contributor, I want `.gitignore` to automatically ignore local configuration files, so that my real student identity remains physically isolated on my machine.
25. As a repository maintainer, I want a pre-commit verification check, so that any accidental inclusion of real student credentials halts the git commit or push immediately.
26. As an orchestrator, I want a state-tracking JSON artifact in the experiment directory, so that the workflow can safely pause, inspect progress, and resume across session boundaries.

## Implementation Decisions

1. **Target Runtime & Language Stack**:
   - Python 3.10+ serves as the execution backbone for all deterministic AST assertions, Word inspections, and packaging scripts.
   - POSIX Bash is used exclusively for environment bootstrapping (`scripts/setup.sh`) and command coordination.
   - Native Antigravity (`agy`) Markdown skill definitions coordinate the multi-agent choreography without incurring external LLM API costs.
2. **Platform Guard & PEP 668 Automation**:
   - A dedicated `scripts/setup.sh` script is provided for Linux (including WSL2).
   - In accordance with Python PEP 668 (preventing system package manager collisions), the script automatically creates and configures a `.venv` directory for python dependencies (`python-docx`, `pyyaml`).
   - If executed on Windows native shell (PowerShell / CMD), the script halts with an accurate explanation:
     *"💡 检测到 Windows 原生环境：Linux 的 Shell 统一简洁好用，而 PowerShell 带有历史包袱，语法相对诡异冗杂。用 PowerShell 只会害了你 [doge]，强烈推荐移步 WSL2 (Ubuntu)！"*
3. **Strict Separation of Drafting and Humanizing**:
   The authoring process is partitioned into two distinct subagents: a Writer Agent that establishes structural and technical accuracy, followed by an independent Humanizer Agent that refines subjective sections, eliminates AI cliches, and manages Pandoc table assertions.
4. **Decoupled Assembler Interface for Computer Use**:
   Phase 2 is encapsulated inside a dedicated Assembler Agent that exchanges a structured JSON manifest (`assembly_manifest.json`) and validates file completeness. While initially pausing for manual human execution, this design acts as a plug-and-play seam for a future Computer Use Agent.
5. **Three-Phase State Machine Lifecycle**:
   The workflow lifecycle is modeled as a deterministic state machine:
   ```text
   [INIT]
     │
     ▼ (Phase 1)
   [INSPECTED] ──► [IMPLEMENTED] ──► [MEASURED] ──► [DRAFTED] ──► [HUMANIZED & COMPILED]
     │
     ▼ (Phase 1 Gate: Halt)
   [AWAITING_ASSEMBLY]
     │
     ▼ (Phase 2: Human / Future Computer Use)
   [ASSEMBLED & VALIDATED]
     │
     ▼ (Phase 3: Triggered upon user confirmation)
   [PACKAGED] ──► [GIT_SYNCED] ──► [RELEASED]
   ```
6. **Configuration and Privacy Architecture**:
   Configuration is standardized on YAML. Publicly tracked examples (`config.example.yaml`) contain mock dummy data. Local runtime overrides (`config.local.yaml` or `~/.config/auto-exp/config.yaml`) are physically isolated and blocked by `.gitignore`.
7. **Deterministic Helper Tooling**:
   Critical validation and inspection logic (Word table extraction, Pandoc AST table checking, clean zip compression, docx image presence verification) is implemented as standalone, deterministic Python utilities rather than ad-hoc inline bash snippets.

## Testing Decisions

### What Makes a Good Test
Tests for this workflow must exercise observable external behavior, state machine transitions, and filesystem artifacts rather than internal subagent prompt wording. A test passes if the expected physical files (`guide.md`, `measurements.json`, `report.docx`, `release/*.zip`) are produced, conform to schemas, and pass strict format assertions.

### Seams to Test
The primary test seam is the **Workflow State & Artifact Pipeline Seam (High-Level Black-Box Integration Seam)**:
1. **Platform & Setup Seam**: Test that `scripts/setup.sh` sets up a valid `.venv` complying with PEP 668, verifies package availability on Linux, and gracefully asserts non-Linux guidance.
2. **Phase 1 Pipeline Seam**: Executed with sample course input materials (lab manual + Word template). The test verifies:
   - `guide.md` is extracted and matches template headings.
   - `src/` contains code and tests that execute successfully.
   - `measurements.json` contains valid numeric benchmarks.
   - Pandoc AST table assertion passes (tables >= 2, unrendered pipe characters == 0).
   - Execution stops without creating `release/`.
3. **Phase 2 Assembler Seam**: The test supplies a mock final report (>100KB with embedded media) and verifies that the Assembler validation script succeeds, while failing when supplied with an incomplete or small (<100KB) draft.
4. **Phase 3 Release Seam**: The test invokes packaging on mock artifacts and inspects the resulting zip to verify that zero `__pycache__` or `.pyc` files exist in the archive.
5. **Privacy Seam**: A test scans simulated git commit diffs to assert that mock data passes and realistic sensitive credentials trigger immediate process termination.

### Prior Art
The test patterns are directly derived from the AST table assertion script and clean zip packaging assertions documented in `writing-lab-reports/SKILL.md`.

## Out of Scope

1. **Native Windows Support**: Windows CMD / PowerShell environments are strictly unsupported; users must run in WSL2.
2. **Autonomous GUI/OS Automation via Computer Use**: Real-time automated mouse/keyboard GUI screenshot capture is reserved for a future release; Phase 2 is currently human-in-the-loop.
3. **Non-Word Academic Report Formats**: Formatting engines for LaTeX or Typst are excluded; the system targets standard Microsoft Word (`.docx`) university templates.
4. **Automated Submission to University Grading Portals**: Uploading to university intranets (Canvas, Blackboard, Xuexitong) is out of scope.
5. **Multi-tenant Cloud Web Service**: The project is strictly designed for local workstation use via CLI and Antigravity.

## Further Notes

- All implementations must strictly respect the repository's public status and ensure zero private data is checked into source control.
- All vocabulary used throughout this specification strictly aligns with `GLOSSARY.md` and ADR `0001-agy-multi-agent-orchestration.md`.
