# Command Reference

All Forge commands are slash commands in Claude Code.
Run any command without arguments to see its options
and current context.

---

## Primary Commands

These are the commands you'll use most often.

### `/forge-init`

Initialize Forge in your project.

Creates `.forge-context/` with starter templates and
context files. Analyzes your project to pre-populate
context, then asks you to confirm before writing.

**Run when:** Starting Forge in a new project.

---

### `/forge-explore`

Start or continue an effort.

Creates a new effort directory under
`.forge-context/efforts/YYYYMM-{slug}/` or resumes
work on an existing effort. Helps you explore a
problem space, capture user stories, and identify
slice candidates.

**Subcommands:**
- `new` — Create a new effort
- `score` — Calculate or update the RICE score

**Run when:** Exploring a problem before committing
to a solution.

---

### `/forge-work`

Start or continue a slice.

Creates a new slice directory under
`.forge-context/slices/YYYYMM-{slug}/` or resumes
work on an existing slice. Routes to the right phase
based on what's already been done.

**Subcommands:**
- `new` — Create a new slice
- `status` — Show current phase and progress

**Run when:** Building and delivering focused work.

---

### `/forge-implement`

Ad-hoc changes without slice ceremony.

For quick improvements, fixes, and enhancements that
don't need a full slice. Creates a worktree and
helps you make and commit a change.

**Run when:** Making a targeted change that doesn't
need requirements or design phases.

---

### `/forge-investigate`

Investigate a bug or issue.

Systematically explores a problem, identifies root
cause, and produces an investigation report.

**Run when:** Debugging an issue before deciding how
to fix it.

---

### `/forge-digest`

Summarize recent planning activity.

Produces a human-readable summary of recent effort
and slice work. Useful for standups, status updates,
or just catching up after time away.

**Key arguments:**
- `--days N` — Summarize last N days (default: 7)
- `--scope effort|slice|all` — Limit scope

---

### `/forge-reviewable`

Restructure commits into atomic, reviewable units.

Takes a messy commit history and reorganizes it into
logical, well-described commits that tell a coherent
story.

---

## Workflow Commands

Commands for specific phases and workflow steps.

### `/forge-requirements`

Run the requirements gathering phase.

Guides an AI-assisted conversation to draft a
requirements document. Covers summary, success
criteria, scope boundaries, and open questions.

**Run when:** Starting Phase 1 of a slice.

---

### `/forge-design`

Run the design phase.

Guides an AI-assisted conversation to draft a design
document. Covers architecture, component changes,
alternatives, testing strategy, and task breakdown.

**Run when:** Starting Phase 2 of a slice.

---

### `/forge-start-task`

Start work on an implementation task.

Sets up working context for a specific task from
`tasks.md`. Helps track progress and follows
implementation disciplines (TDD, systematic
debugging, verification before complete).

**Run when:** Starting Phase 3 of a slice.

---

### `/forge-retro-note`

Capture a process observation.

Records a correction, gap, or improvement idea to
a retro notes file. Applied later by `/forge-improve`.

**Run when:** Noticing something about the workflow
that could be better.

---

### `/forge-improve`

Apply retro notes as improvements.

Reviews accumulated retro notes and applies them
to the relevant files (templates, context files,
guidelines). Each note is presented for review
before applying.

**Run when:** Periodically, to act on retro notes.

---

### `/forge-phase-complete`

Complete a slice phase with a review summary.

Marks a phase as complete by creating a review
document and committing it. This is how Forge
derives phase state — from git artifacts, not
checkbox state.

**Run when:** Finishing requirements or design
and moving to the next phase.

---

### `/forge-process-pr-discussions`

Process PR discussions.

Reads open discussions on a PR and routes them to
the right place: applies code changes, updates
documents, or marks discussions as resolved.

**Run when:** Addressing reviewer feedback on a PR.

---

## Maintenance Commands

Commands for health checks and upkeep.

### `/forge-audit`

Health checks on work and context.

**Audit types:**
- `work` — Check slice and effort health
- `context` — Check if context files are current
- `all` — Both

**Key flags:**
- `--deep` — More thorough analysis

**Run when:** Checking if your Forge setup is healthy,
especially after extended time away.
