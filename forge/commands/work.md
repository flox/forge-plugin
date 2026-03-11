# /work

Work on slices — build and deliver focused work packages.

## This Command's Role

Interactive entry point for slice work. Detects context,
finds accepted slice candidates ready to spawn, and routes
to appropriate phase commands.

## Worktree-First Principle

All slice work happens in worktrees. Before any slice work,
verify or create a worktree. Slices use ephemeral branches:
`slice/{slug}-{phase}-{suffix}`.

See Skill: `worktree-workflow` for creation patterns,
ephemeral branch lifecycle, navigation, and troubleshooting.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Check branch existence before `git checkout`
- Use exit codes for control flow, not error messages

## Terminology Awareness

Before producing any user-facing output, read
`.forge-context/overrides/terminology.md`. If the user
has mapped Forge terms to their own vocabulary, use
their terms in all output — menus, status messages,
suggestions, and agent prompts. Pass the mapped terms
to any spawned agents so they also use the user's
language.

## Context Detection

Detect state using git commands and file reads:

```bash
# Current branch
git branch --show-current

# List worktrees (absolute paths — use these for navigation)
git worktree list

# List slice directories
ls -d .forge-context/slices/[0-9]*/ 2>/dev/null

# List effort candidate files
find .forge-context/efforts -name "slices.md" 2>/dev/null
```

**DO NOT check worktree status until user selects which
one to work on.**

**Context results (prioritized order):**
1. In worktree for slice: Continue that work
2. On `slice/*` branch NOT in worktree: Prompt to use
   worktree
3. On `main`: Present menu with slices, worktrees, and
   candidates

## Phase Derivation Logic

Determine the current phase from git artifacts. Read from
the WORKTREE path, not main branch.

```
1. Check for review summaries:
   - reviews/requirements-review.md exists → req done
   - reviews/design-review.md exists → design done

2. Check for document content:
   - requirements.md has content → requirements started
   - design.md has content → design started
   - tasks.md has content → implementation started

3. Derive current phase:
   - design-review exists → implementation (or complete)
   - req-review exists + design.md has content → design
   - req-review exists → requirements-approved
   - requirements.md has content → requirements
   - else → scaffolded
```

## Behavior

### On Main Branch

Build the menu from available data:

```
Agent: You're on main.

**Active slices (from index):**
- Catalog Outputs Deduplication (Design phase)
- Environment SBOMs (Implementation phase)

**Existing worktrees:**
- catalog-outputs-deduplication
- environment-sboms

**Accepted candidates (ready to spawn):**
- SL-001: SAML Integration (Enterprise Auth effort)

Would you like to:
1. Continue slice work (select from above)
2. Spawn accepted candidate
3. Start a new standalone slice
```

### User Selects Worktree

Navigate to the worktree using its absolute path from
`git worktree list`. Check local state:

```bash
# Get absolute path
WORKTREE_PATH=$(git worktree list | grep "${slug}" \
  | awk '{print $1}')

# Check branch status
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" log --oneline \
  origin/$(git -C "$WORKTREE_PATH" branch --show-current)..HEAD
```

**Present status with context:**

If behind remote, offer to pull. If ahead, note unpushed
work. If open review PR has discussions, offer to process
them.

If in sync, present phase-appropriate menu (see below).

### In Slice Context

When in a slice/feature worktree:

**CRITICAL: Read all slice files from the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/slices/{YYYYMM}-{slug}/requirements.md
Wrong:   /path/to/project/.forge-context/slices/{YYYYMM}-{slug}/requirements.md
```

Identify the current phase using the derivation logic above.

Present phase-appropriate menu:

**Requirements Phase:**
```
Agent: Working on **{slice_name}** (Requirements phase)
Worktree: _worktrees/{slug} (up to date)

Would you like to:
1. Continue requirements gathering (/requirements)
2. Review requirements via PR comments
3. Complete requirements phase (/phase-complete)
4. View current requirements
```

**Requirements Approved:**
```
Agent: Working on **{slice_name}** (Requirements approved)

Requirements are approved. Next step:
1. Start design phase (/design)
2. Wait — leave in "requirements approved" state
```

**Design Phase:**
```
Agent: Working on **{slice_name}** (Design phase)

Would you like to:
1. Continue design work (/design)
2. Run design review (Design Reviewer agent)
3. Review design via PR comments
4. Complete design phase (/phase-complete)
5. View current design
```

**Implementation Phase:**
```
Agent: Working on **{slice_name}** (Implementation phase)

Tasks:
- #{num}: {title} [status]
- #{num}: {title} [status]

Would you like to:
1. Start/continue a task (/start-task)
2. Complete implementation phase (/phase-complete)
```

### Spawn Slice from Candidate

When user selects a candidate to spawn:

1. Ask who will own this slice
2. Generate slug from candidate name
3. Confirm directory and worktree location
4. Initialize slice structure (see Start Standalone Slice)
5. Seed from effort (read accepted candidate details
   and populate requirements.md, tasks.md)
6. Report results

### Start Standalone Slice

First, help user decide if slice is the right choice.
Apply diagnostic questions:

1. Is there a specific deliverable?
2. Are the key decisions already made?
3. Is there a reference implementation or clear pattern?
4. Could an engineer start with just a design doc?
5. Are the unknowns about "how" (not "what")?

If 3+ answers are "yes" — slice is appropriate. Proceed.
If 3+ answers are "no" — suggest `/explore init`.

If user confirms slice:

1. Gather description (2-4 words)
2. Generate slug, confirm location:
   > "I'll create the slice at
   > `.forge-context/slices/{YYYYMM}-{slug}/`"
3. Ask for slice owner

**Create worktree and structure:**

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)

# Generate ephemeral suffix
SUFFIX=$(head /dev/urandom | tr -dc 'a-z0-9' | head -c 4)
BRANCH="slice/${slug}-requirements-${SUFFIX}"

# Create worktree with new branch from main (single command)
mkdir -p "${REPO_ROOT}/_worktrees"
git worktree add "${REPO_ROOT}/_worktrees/${slug}" \
  -b "$BRANCH" origin/main

# Create slice directory
SLICE_DIR="${REPO_ROOT}/_worktrees/${slug}/.forge-context/slices/${YYYYMM}-${slug}"
mkdir -p "${SLICE_DIR}/reviews"
mkdir -p "${SLICE_DIR}/artifacts"
```

Copy templates from `.forge-context/templates/slice/`
to the slice directory.

Commit and push scaffolding. Report results and offer to
start requirements.

---

## Route to Existing Commands

| Action | Route To |
|--------|----------|
| Requirements gathering | `/requirements` |
| Design work | `/design` |
| Phase completion | `/phase-complete` |
| Task work | `/start-task` |

**Design Review:**
Spawn `Design Reviewer` agent:
```
Use Task tool with:
- subagent_type: "Design Reviewer"
- prompt: |
    ## Inputs
    - slice_path: {ABSOLUTE path to slice dir in worktree}
    - slice_name: {name}
    - effort_path: {effort path if from effort, else empty}
```

**CRITICAL:** Always use absolute paths from the worktree.

---

## Action: Review via PR

Creates a lightweight PR for reviewing slice content using
GitHub's inline comment features.

1. Create review branch from main in the worktree
2. Copy the file(s) to review into the branch (touching
   them so they appear in "Files changed")
3. Create a `REVIEWING.md` with instructions for reviewers
4. Create PR and direct reviewers to it
5. Use `/process-pr-discussions` to apply feedback

---

## Subcommands (Direct Access)

| Invocation | Action |
|------------|--------|
| `/work` | Full menu |
| `/work status` | Show slice status |
| `/work spawn` | Jump to spawn candidate |
| `/work new` | Jump to new standalone slice |
| `/work requirements` | Route to `/requirements` |
| `/work design` | Route to `/design` |
| `/work task` | Route to `/start-task` |
| `/work review` | Run design review (agent) |
| `/work review-pr` | Create review PR for feedback |
| `/work complete` | Route to `/phase-complete` |

---

## Status Derivation

Use the phase derivation logic above. Phase completion is
determined by review summary files:

| Phase | Complete When |
|-------|---------------|
| Requirements | `reviews/requirements-review.md` exists |
| Design | `reviews/design-review.md` exists |
| Implementation | All tasks closed |

---

## Context Files to Read

- `.forge-context/slices/README.md` — Active slices
- `{slice_path}/checklist.md` — Current phase
- `{slice_path}/tasks.md` — Implementation tasks
- `{slice_path}/requirements.md` — Requirements
- `.forge-context/context/team.md` — Owner validation

**Note:** When working in a worktree, `{slice_path}` refers
to the worktree location, not the main branch location.

---

## Example Interactions

### Spawn from Candidate
```
User: /work

Agent: You're on main.

**Accepted candidates (ready to spawn):**
- SL-001: CUDA Build Support — accepted 2026-01-15

Would you like to:
1. Continue slice work
2. Spawn accepted candidate
3. Start a new standalone slice

User: 2

Agent: Creating slice for CUDA Build Support...
       Worktree: _worktrees/cuda-build-support/
       Directory: .forge-context/slices/202601-cuda-build-support/

       Seeding from effort...

       Ready! Switch to worktree:
         cd _worktrees/cuda-build-support
```

### Continue Slice Work
```
User: /work

Agent: You're on main.

**Existing slice worktrees:**
- environment-sboms → _worktrees/env-sboms (up to date)

User: env-sboms

Agent: Working on **Environment SBOMs** (Design phase)

Would you like to:
1. Continue design work (/design)
2. Run design review
3. Complete design phase (/phase-complete)
4. View current design
```
