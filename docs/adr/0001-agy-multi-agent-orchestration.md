# 1. Antigravity Native Multi-Agent Orchestration with Computer-Use Seam

## Context

Generating academic engineering lab reports requires a delicate balance of reverse-engineering official Word templates, writing self-contained source code, measuring real execution metrics, and drafting technical reports devoid of AI jargon.

Historically, attempting to do all of this in a monolithic prompt or single agent led to context pollution, prompt leakage, hallucinated thinking questions, and broken Pandoc tables. Furthermore, university lab reports require actual hardware/terminal execution screenshots and official Word template assembly, which cannot be reliably hallucinated.

The repository is public on GitHub, meaning zero real student credentials can ever be tracked in Git.

## Decision

We orchestrate an automated workflow natively within Google Antigravity (`agy`), dividing the workload across **7 specialized subagents + 1 orchestrator** structured around a strict **Three-Phase Lifecycle**:

1. **Native `agy` Engine**: We orchestrate directly via Antigravity subagent skills rather than heavyweight external frameworks (MetaGPT, CrewAI, AutoGen), eliminating additional LLM token costs and leveraging built-in tool capabilities.
2. **Specialized Agent Separation**:
   - `Inspector`: Word template reverse-engineering & `guide.md` SSoT derivation.
   - `Engineer`: Minimal, standalone code implementation & line-level test sets.
   - `Tester`: Real command execution, runtime metric capture, and raw log recording.
   - `Writer`: Structural draft authoring with screenshot placeholders.
   - `Humanizer`: Dedicated stylistic rewriting into a natural student voice, eliminating academic AI jargon, and enforcing Pandoc AST table assertions.
   - `Assembler`: Dedicated Phase 2 interface (currently human-in-the-loop with strict docx validation; acts as the direct upgrade seam for future Computer-Use automation).
   - `Releaser`: Clean zip archiving (`-x __pycache__`), Git branch synchronization, and GitHub Release deployment with Chinese rename blocks.
3. **Phase Boundaries**: Phase 1 terminates unconditionally at `report.docx`. Phase 2 is handed off to Assembler (human/computer-use). Phase 3 executes only after valid final docx assertion.
4. **Configuration & Privacy**: System configuration uses YAML (`config.example.yaml` tracked with mock data like "张三" / "2024000001"; real student info isolated in `.gitignore`'d `config.local.yaml`). Supports `workspace_dir` to optionally decouple report storage from the generator engine.
5. **Deterministic Format & Verification State Machines**:
   - Table AST Normalization: Markdown tables are formatted by a state machine enforcing blank lines around the outer table boundary while keeping inner table rows strictly contiguous to prevent Pandoc silent degradation.
   - Multi-Factor Assembly Verification: Final docx validation asserts both file size (>100KB) and the physical presence of embedded images in `word/media/`.

## Consequences

- Intermediate artifacts (`guide.md`, `measurements.json`, `report.raw.md`, `report.docx`, `assembly_manifest.json`) are persisted to the experiment directory, making each stage 100% reproducible and debuggable.
- When Computer Use is ready, only the `Assembler` subagent implementation needs to be upgraded from "human prompt + wait" to "automated UI action", keeping all other 6 agents untouched.
- External dependencies are kept to a minimum (only Python and Pandoc), ensuring instant portability.
