# /forge-init

Set up Forge planning in a project by scaffolding
`.forge-context/` and capturing project context.

## This Command's Role

This is the entry point for new Forge users. It creates the
`.forge-context/` directory structure, captures project context
(auto-detected or manual), and appends a `CLAUDE.md` section
with command references.

The first impression matters. Default to auto-detection to show
the user that Forge already understands their project.

## Behavior

### Step 1: Check Existing Scaffold

Check if `.forge-context/` already exists:

```bash
test -d ".forge-context"
```

If it exists:
> "Forge planning is already set up in this project."
> ".forge-context/ found with existing configuration."
>
> "What would you like to do?"
> 1. Re-run context detection (update context files)
> 2. Re-run specific section (choose which)
> 3. Exit — setup is already complete

If the user chooses option 2, present the section list and
jump to the appropriate step. If exit, stop.

If `.forge-context/` does not exist, proceed to Step 2.

### Step 2: Choose Onboarding Mode

> "I'll set up Forge planning for this project. I can
> analyze your codebase and suggest context automatically,
> or you can provide it manually."
>
> 1. Auto-detect (Recommended) — I'll scan the project
>    and confirm findings with you
> 2. Manual — answer a few questions
> 3. Selective — choose which areas to auto-detect

Default to option 1. The first wow moment is showing the
user we already understand their project.

### Step 3: Create Directory Structure

Create the following structure:

```
.forge-context/
  context/
  efforts/
  slices/
  artifacts/
  overrides/
    terminology.md
  templates/
    effort/
      effort.md
      decisions.md
      slices.md
      checklist.md
    slice/
      requirements.md
      design.md
      tasks.md
      checklist.md
      decisions.md
    starter-principles.md
```

### Step 4: Copy Templates

Copy templates from the plugin templates directory using
`${CLAUDE_PLUGIN_ROOT}/templates/` as the source path.

Create the directories:
```bash
mkdir -p .forge-context/context
mkdir -p .forge-context/efforts
mkdir -p .forge-context/slices
mkdir -p .forge-context/artifacts
mkdir -p .forge-context/overrides
mkdir -p .forge-context/templates/effort
mkdir -p .forge-context/templates/slice
```

Copy each template file from
`${CLAUDE_PLUGIN_ROOT}/templates/` to the corresponding
location under `.forge-context/templates/`.

Create `.forge-context/overrides/terminology.md` from the
plugin's overrides template if it exists, or create a
minimal file:

```markdown
# Terminology Overrides

Map Forge terms to your team's preferred vocabulary.
When the user uses a team term, understand it as the
Forge term. When producing output, use the team term.

| Forge Term | What It Means | Your Term |
|------------|---------------|-----------|
| effort | Discovery process — exploring and understanding | |
| slice | Delivery process — building a shippable piece | |
| task | A unit of implementation work | |
| area owner | Person who reviews and approves for a domain | |

Empty "Your Term" cells mean the default is used.
Fill in only the terms you want to rename.
```

### Step 5: Quick Scan (Auto-detect Mode)

Run a quick scan to understand the project shape. This
informs the deep discovery outline in Step 5b.

**Run detection (single call to avoid parallel failures):**

```bash
echo "=== PRODUCT FILES ===" && \
ls README.md package.json pyproject.toml Cargo.toml \
  go.mod flake.nix setup.py setup.cfg 2>/dev/null; \
echo "=== DIRECTORY STRUCTURE ===" && \
find . -maxdepth 2 -type d \
  ! -path './.git*' ! -path './node_modules*' \
  ! -path './.venv*' ! -path './target*' \
  ! -path './__pycache__*' | sort; \
echo "=== RECENT CONTRIBUTORS ===" && \
git shortlog -sn --since="90 days ago" 2>/dev/null \
  | head -10; \
echo "=== BRANCH PATTERNS ===" && \
git branch -r 2>/dev/null | head -20; \
echo "=== CONTRIBUTION GUIDELINES ===" && \
ls CONTRIBUTING.md .eslintrc* .rustfmt.toml \
  .prettierrc* tsconfig.json Makefile 2>/dev/null; \
echo "=== DONE ==="
```

**Important:** Run as a single Bash call, not parallel.
Parallel Bash calls cascade-fail if any one is denied.

Read the project's README and any manifest files found
(package.json, pyproject.toml, Cargo.toml, go.mod) to
understand the project description, dependencies, and
structure.

### Step 5b: Present Outline and Confirm

Present what context files will be created and what deep
discovery will cover. Get user confirmation before
investing time in the deep scan.

> "I've done a quick scan. Here's what I'll create:"
>
> **Context files I'll populate:**
>
> | File | What It Captures |
> |------|-----------------|
> | `context/product.md` | What this project does, its architecture, key dependencies |
> | `context/components.md` | Modules, their responsibilities, entry points, API surfaces, key data structures |
> | `context/team.md` | Active contributors and their areas |
> | `context/principles.md` | Engineering principles (starter set + any found in your configs) |
> | `context/git-workflow.md` | Branch strategy, merge approach, CI patterns |
>
> **Deep discovery will examine:**
> - Module boundaries and public interfaces
> - API endpoints, routes, or CLI commands
> - Key data structures, models, and schemas
> - Configuration patterns and environment variables
> - Test structure and testing patterns
> - Error handling conventions
>
> "This takes a few minutes. Proceed with deep
> discovery?"
>
> 1. Yes — full deep discovery (Recommended)
> 2. Quick only — use what we have, skip deep scan
> 3. Selective — choose which areas to deep-scan

If user selects 2, write context files from the quick
scan data only and proceed to Step 7.

If user selects 3, present the area list and deep-scan
only selected areas.

### Step 5c: Deep Discovery

Use Skill: `code-discovery` patterns to deeply explore
the codebase. Read actual source files, not just
directory listings.

**For each major component identified in Step 5:**

1. **Entry points:** Find main files, CLI definitions,
   API route registrations, or app bootstrapping
2. **Public interfaces:** Read exported functions,
   classes, traits, types. Note key signatures.
3. **Data structures:** Find models, schemas, database
   tables, config types, serialization formats
4. **API surface:** Find endpoints, routes, commands,
   public methods. Note request/response shapes.
5. **Dependencies:** Read manifest for key dependencies
   and their roles (framework, database, auth, etc.)
6. **Test patterns:** Find test directories, test
   naming conventions, fixture patterns
7. **Error handling:** Find error types, error response
   patterns, logging conventions

**Discovery approach per language:**

For **Rust** projects:
```bash
# Find public types and traits
grep -rn "^pub struct\|^pub enum\|^pub trait\|^pub fn" \
  src/ --include="*.rs" | head -40; \
# Find CLI commands or API routes
grep -rn "command\|route\|handler\|endpoint" \
  src/ --include="*.rs" | head -20
```

For **Python** projects:
```bash
# Find class definitions and key functions
grep -rn "^class \|^def \|^async def " \
  src/ --include="*.py" | head -40; \
# Find API routes
grep -rn "router\.\|@app\.\|@router\." \
  src/ --include="*.py" | head -20
```

For **TypeScript/JavaScript** projects:
```bash
# Find exports and interfaces
grep -rn "^export \|^interface \|^type " \
  src/ --include="*.ts" --include="*.tsx" | head -40; \
# Find route handlers
grep -rn "router\.\|app\.\|@Controller\|@Get\|@Post" \
  src/ --include="*.ts" | head -20
```

For **Go** projects:
```bash
# Find exported types and functions
grep -rn "^type \|^func " --include="*.go" | head -40; \
# Find HTTP handlers
grep -rn "HandleFunc\|Handle\|http\." \
  --include="*.go" | head -20
```

Read the key files found to understand signatures,
data flow, and patterns. Use the Read tool to examine
important files in detail — don't just grep.

**Write `context/components.md` with depth:**

For each component, document:
- Purpose (one line)
- Key files and entry points (with file:line refs)
- Public API surface (endpoints, commands, exports)
- Key data structures (with field names)
- Dependencies on other components
- Test location and approach

**Example depth (components.md):**

```markdown
## API Server (`src/server/`)

REST API for task management.

### Entry Point
- `src/server/main.py:12` — FastAPI app creation
- `src/server/routes/` — Route definitions

### API Surface

| Endpoint | Handler | Purpose |
|----------|---------|---------|
| `GET /tasks` | `routes/tasks.py:15` | List tasks |
| `POST /tasks` | `routes/tasks.py:42` | Create task |
| `GET /tasks/{id}` | `routes/tasks.py:68` | Get task |

### Key Data Structures

```python
class Task(BaseModel):
    id: UUID
    title: str
    status: TaskStatus  # enum: pending, active, done
    assignee: Optional[str]
    created_at: datetime
```

### Dependencies
- FastAPI (framework)
- SQLAlchemy (ORM)
- Pydantic (validation)

### Tests
- `tests/test_tasks.py` — unit tests
- `tests/integration/` — API integration tests
```

**Write `context/product.md` with depth:**

Include not just what the project does, but:
- Architecture style (monolith, microservices, CLI, library)
- Key dependencies and why they're used
- Configuration approach (env vars, config files, etc.)
- Deployment model if detectable (Docker, serverless, etc.)

### Step 5d: Present Deep Discovery Results

Present the populated context files for confirmation:

> "Deep discovery complete. Here's what I found:"
>
> **Product:** [summary]
> **Architecture:** [monolith/services/CLI/library]
> **Components:** [N] modules identified
>   - [component] — [purpose] ([M] endpoints/exports)
>   - ...
> **Team:** [N] active contributors
> **Git workflow:** [description]
>
> "Review the full context files?"
>
> 1. Accept all — write and continue
> 2. Review each file before writing
> 3. Edit specific sections

Write confirmed context to `.forge-context/context/`.

### Step 6: Context Capture (Manual Mode)

Use interactive questions when user chooses manual mode
or when auto-detection cannot determine a section with
reasonable confidence.

| # | Question | Target File |
|---|----------|------------|
| 1 | "What does this project do?" | `context/product.md` |
| 2 | "Main components or modules?" | `context/components.md` |
| 3 | "Who works on this? (names, areas)" | `context/team.md` |
| 4 | "Engineering principles?" | `context/principles.md` |
| 5 | "Git workflow? (trunk, gitflow, etc.)" | `context/git-workflow.md` |

Keep questions brief. Accept free-form answers and format
them into the appropriate file.

### Step 7: Engineering Principles

Seed `context/principles.md` with a starter set and
guide the user to customize it.

**Always start with the starter principles** from the
template (`templates/starter-principles.md`). These are
universal engineering principles that apply broadly:

- **KISS** — Prefer the simplest solution
- **Do one thing well** — Limited scope, modular design
- **Less is more** — Do the least to get the job done
- **Consistency** — Reuse established idioms
- **Good enough is not good enough** — Take pride in
  optimal solutions
- **Inform intrinsically** — Surface knowledge in context

**Present them to the user:**

> "I've seeded your engineering principles with a
> starter set of 6 universal principles:"
>
> 1. KISS — keep it simple
> 2. Do one thing and do it well
> 3. Less is more
> 4. Consistency is key
> 5. Good enough is not good enough
> 6. Inform intrinsically
>
> "These are starting points, not gospel. You should
> customize this file with principles your team
> actually follows. Good additions might include:"
>
> - Testing philosophy (TDD, test pyramid, coverage)
> - Code review expectations
> - Performance and scalability priorities
> - Security posture (input validation, auth patterns)
> - API design conventions (REST, versioning, errors)
> - Documentation requirements
>
> "Would you like to add any principles now?"
>
> 1. Yes — let me describe our principles
> 2. No — I'll update `.forge-context/context/principles.md`
>    later

If yes, capture the user's principles and append them
to the file below the starter set, under a section
header like `## Team Principles`.

**When CONTRIBUTING.md or linter configs exist,** also
extract project-specific conventions found in those
files and add them as a `## Detected Conventions`
section. Examples:
- "Line length limit: 80 chars (from .eslintrc)"
- "Commit format: conventional commits (from CONTRIBUTING.md)"
- "Formatting: rustfmt with default settings"

The principles file should always note that users can
refine it over time via `/forge-retro-note`.

### Step 8: Append CLAUDE.md Section

Check if `CLAUDE.md` exists:

```bash
test -f "CLAUDE.md"
```

If it exists, append to it. If not, create it.

Append the following section:

```markdown
## Forge Planning Context

This project uses Forge for structured planning.
Planning artifacts live in `.forge-context/`.

- `/forge-explore` - Discover and frame problems
- `/forge-work` - Build and deliver solutions
- `/forge-retro-note` - Capture process observations
- `/forge-improve` - Apply notes as improvements
- `/forge-audit` - Verify context accuracy
- `/forge-digest` - Summarize recent planning activity
- `/forge-reviewable` - Restructure commits for review

Context files in `.forge-context/context/` describe
the project, team, and guidelines. Keep these updated
as the project evolves, or run `/forge-audit` to
check for drift.

If `.forge-context/overrides/terminology.md` exists
and has non-empty mappings, use the team's preferred
terms in all output. When the user says their term,
understand it as the Forge term. When producing
output, use their term instead.
```

### Step 9: Suggest First Retro Note for Terminology

> "Forge separates planning into two processes:
>
> - **Effort** — discovery: exploring a problem space,
>   gathering context, identifying what to build
> - **Slice** — delivery: building a focused, shippable
>   piece of work with requirements, design, and
>   implementation
>
> Your team may use different names for these processes.
> If so, you can capture your preferred terms now with
> `/forge-retro-note` and they'll appear in
> `.forge-context/overrides/terminology.md`.
>
> Would you like to set up terminology overrides now?"
> 1. Yes — run `/forge-retro-note` to capture terms
> 2. No — I'll use the default Forge terms

If yes, jump to `/forge-retro-note`.

### Step 10: Offer First Action

> "Forge is ready! What would you like to do?"
>
> 1. Explore a problem space (`/forge-explore`)
> 2. Start building something (`/forge-work new`)
> 3. Investigate an issue (`/forge-investigate`)
> 4. Just commit the scaffold — I'll come back later

Route to the chosen command, or proceed to commit.

### Step 11: Commit Scaffold

**`.forge-context/` should be tracked in git.** Planning
artifacts — context files, requirements, designs, decision
logs — are part of the project's knowledge base. Tracking
them in version control means every team member gets the
same context, planning decisions are reviewable in PRs,
and nothing is lost when sessions end.

Commit the scaffold to git:

```bash
git add .forge-context/ CLAUDE.md
git commit -m "chore: Initialize Forge planning scaffold

Sets up .forge-context/ with project context and
planning structure.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Report results:

> "Forge planning is set up and committed to git."
>
> Created:
> - `.forge-context/context/` — 5 context files
> - `.forge-context/templates/` — effort and slice templates
> - `.forge-context/overrides/terminology.md`
> - Updated `CLAUDE.md` with Forge command reference
>
> `.forge-context/` is tracked in git so your planning
> artifacts travel with the code. All team members will
> share the same context, and changes are reviewable
> in PRs just like code.

## Subcommands

None — this command enters interactive mode directly.
