# /forge-explore

Work on efforts — discover and understand problem spaces.

## This Command's Role

Interactive entry point for effort work. Detects context,
offers relevant actions, and spawns appropriate agents for
discovery activities.

## Worktree-First Principle

All effort work happens in worktrees. Before any effort
work, verify or create a worktree. Efforts use ephemeral
branches: `effort/{slug}-{suffix}`.

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

Detect current state using git commands and file reads:

```bash
# Current branch
git branch --show-current

# List worktrees
git worktree list

# Check if on main
git rev-parse --abbrev-ref HEAD

# List effort directories
ls -d .forge-context/efforts/[0-9]*/ 2>/dev/null
```

**Context results:**
- On `main`: Offer effort selection or new effort
- On `effort/*` branch in worktree: Working on that effort
- In effort directory: Working on that effort

## Behavior

### On Main Branch

Read `.forge-context/efforts/` and `git worktree list` to
build the menu.

```
Agent: You're on main.

**Existing effort worktrees:**
- cuda-build → _worktrees/cuda-build (up to date)

**Active efforts (no worktree):**
- Package Conflicts (.forge-context/efforts/202601-package-conflicts)

Would you like to:
1. Continue in existing worktree (enter name)
2. Create worktree for existing effort
3. Start a new effort
```

**If user selects existing worktree:**
1. Navigate to the worktree (use absolute path from
   `git worktree list`)
2. If behind origin: offer `git pull --rebase` or warn
3. Present effort menu

**If user selects "create worktree for existing effort":**
1. Show efforts without worktrees
2. Create worktree:
   ```bash
   REPO_ROOT=$(git rev-parse --show-toplevel)
   git worktree add "${REPO_ROOT}/_worktrees/${slug}" \
     effort/${slug}-work
   ```
3. Provide path and present effort menu

**IMPORTANT:** After creating the worktree, read all effort
files from the worktree path (`_worktrees/{slug}/
.forge-context/efforts/...`), NOT from the main branch path.

**If user selects "new effort":** Jump to
[Init New Effort](#init-new-effort)

### In Effort Context

When on an effort branch or in effort directory:

**CRITICAL: Read all effort files from the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/efforts/{YYYYMM}-{slug}/effort.md
Wrong:   /path/to/project/.forge-context/efforts/{YYYYMM}-{slug}/effort.md
```

The worktree contains the current work-in-progress. Main
branch may have stale or empty templates.

```
Agent: Working on **{effort_name}**

Current state:
- Stories: {X} (Y ready, Z draft)
- Requirements: {W} (V ready, U draft)
- Threads: {N} open
- Candidates: {M} pending, {P} accepted

{Suggestions based on current state}

What would you like to do?
1. Frame/refine problem space
2. Add or refine a story
3. Add or refine a requirement
4. Open or resolve a thread
5. Plan user research
6. Synthesize research findings
7. Identify a slice candidate
8. Create candidate PR for review
9. Record a decision (ADR)
10. View effort health
11. Review effort via PR comments
12. Score/rescore effort (RICE)
```

**Suggestions to surface based on state:**
- Problem framing exists but no research: suggest option 5
  (plan research)
- Draft stories exist: suggest option 2 (refine stories)
- Ready stories/requirements but no candidates: suggest
  scope-identifier (option 7)
- Problem framing complete but no score: suggest option 12
  (score effort)

**Route based on selection:**

| Selection | Action |
|-----------|--------|
| 1 | Spawn `Effort Framer` agent |
| 2 | Add or refine a story (guided conversation) |
| 3 | Spawn `Requirements Gatherer` agent |
| 4 | Gather thread info, add to effort.md |
| 5 | Plan user research (guided conversation) |
| 6 | Synthesize research findings (guided conversation) |
| 7 | Spawn `Scope Identifier` agent |
| 8 | Create PR for pending candidates |
| 9 | Gather decision, add to decisions.md |
| 10 | Show health summary |
| 11 | Create review PR for inline feedback |
| 12 | Score/rescore effort (guided conversation) |

---

## Init New Effort

### Step 1: Gather Description

> "What problem space are you exploring?
> Brief description (2-4 words):"

Example: "CUDA support", "enterprise authentication",
"package conflicts"

If too long, suggest a shorter version.

### Step 1.5: Scope Appropriateness Check

Before creating scaffolding, help the user verify this
work needs effort-level discovery. Ask conversationally:

> "Before we set up the effort, a few quick questions:
>
> 1. Is there a specific deliverable you can name?
> 2. Are the key approach decisions already made?
> 3. Is there a reference implementation or proven pattern?
> 4. Could an engineer start with just a design doc?
> 5. Are the unknowns about *what* to build or *how*?"

**If 3+ answers suggest the approach is known:**

> "This work seems well-understood with a known approach.
> It might be better as a slice rather than an effort.
>
> Would you like to:
> 1. Create as a slice instead (`/forge-work new`)
> 2. Create as an effort anyway
> 3. Let me ask more to help decide"

If the user chooses slice, redirect to `/forge-work new`
and stop. If the user chooses effort or answers show
genuine unknowns, proceed to Step 2.

### Step 2: Generate and Confirm

- Convert to kebab-case slug
- Get current year+month (YYYYMM format)
- Show:
> "I'll create the effort **{description}** at
> `.forge-context/efforts/{YYYYMM}-{slug}/`"
> "Does this look correct?"

### Step 3: Identify Initial Contributors

> "Who are the initial contributors?
> (comma-separated names or GitHub handles)"

### Step 4: Create Worktree with Ephemeral Branch

All effort work happens in isolated worktrees.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)

# Generate random suffix
SUFFIX=$(head /dev/urandom | tr -dc 'a-z0-9' | head -c 4)
BRANCH="effort/${slug}-${SUFFIX}"

# Create worktree with new branch from main (single command)
mkdir -p "${REPO_ROOT}/_worktrees"
git worktree add "${REPO_ROOT}/_worktrees/${slug}" \
  -b "$BRANCH" origin/main
```

Report:
> "Created worktree at `_worktrees/{slug}/`"
> "Using branch: `effort/{slug}-{suffix}`"

### Step 5: Create Effort Structure

Navigate to the worktree and create the effort directory:

```bash
WORKTREE="${REPO_ROOT}/_worktrees/${slug}"
EFFORT_DIR="${WORKTREE}/.forge-context/efforts/${YYYYMM}-${slug}"
mkdir -p "${EFFORT_DIR}/artifacts"
```

Copy templates from `.forge-context/templates/effort/`
to the new effort directory, replacing placeholders:
- `[EFFORT_NAME]` → actual name
- `@CONTRIBUTOR` → contributor handles

Update `.forge-context/efforts/README.md` with the new
effort entry (create if it doesn't exist).

Commit and push:
```bash
cd "${REPO_ROOT}/_worktrees/${slug}"
git add .forge-context/
git commit -m "feat(effort): Initialize ${effort_name} effort"
git push -u origin "${BRANCH}"
```

### Step 6: Offer Problem Framing

> "Would you like to start framing the problem space now?"
> 1. Yes — start with Effort Framer agent
> 2. No — I'll add content manually

If yes, spawn the Effort Framer agent:

```
Use Task tool with:
- subagent_type: "Effort Framer"
- prompt: |
    ## Inputs
    - effort_path: {absolute path to effort directory}
    - effort_name: {effort name}
```

---

## Action: Open/Resolve Thread

**Open thread:**
> "What question or topic needs investigation?"
> "What type? (Clarification / Decision / Research /
> Dependency)"
> "What context should be included?"

Assign next TH-NNN ID and add to effort.md.

**Resolve thread:**
> "Which thread to resolve?"
> [list open threads]
> "What was the resolution?"
> "What's the impact on scope/stories?"

Move to Resolved Threads section with resolution details.

---

## Action: Record Decision

Gather ADR information:
> "What is the decision title?"
> "What is the context/problem?"
> "What is the decision?"
> "What are the consequences?"
> "Who were the deciders?"

Assign next ADR-NNN ID and add to decisions.md.

---

## Action: View Health

Parse checklist.md and effort.md to show health summary.

---

## Subcommands (Direct Access)

| Invocation | Action |
|------------|--------|
| `/forge-explore` | Full menu |
| `/forge-explore init` | Jump to new effort |
| `/forge-explore story` | Jump to add story |
| `/forge-explore requirement` | Jump to add requirement |
| `/forge-explore thread` | Jump to open thread |
| `/forge-explore research` | Jump to plan user research |
| `/forge-explore candidate` | Jump to identify candidate |
| `/forge-explore pr` | Jump to create candidate PR |
| `/forge-explore decision` | Jump to record decision |
| `/forge-explore health` | Jump to health view |
| `/forge-explore review-pr` | Create review PR for feedback |
| `/forge-explore score` | Score/rescore effort |

Parse arguments to skip the menu when provided.

---

## Context Files to Read

- `.forge-context/efforts/README.md` — Active efforts list
- `{effort_path}/effort.md` — Stories, requirements, threads
- `{effort_path}/slices.md` — Slice candidates
- `{effort_path}/checklist.md` — Progress tracking
- `.forge-context/context/team.md` — Contributor info

**Note:** When working in a worktree, `{effort_path}` refers
to the worktree location, not the main branch location.

---

## Example Interactions

### Starting Fresh
```
User: /forge-explore

Agent: You're on main.

**Active efforts (no worktree):**
- Package Conflicts
  (.forge-context/efforts/202601-package-conflicts)

Would you like to:
1. Continue in existing worktree
2. Create worktree for existing effort
3. Start a new effort

User: 3

Agent: What problem space are you exploring?

User: package conflicts

Agent: I'll create the effort "Package Conflicts" at
       `.forge-context/efforts/202601-package-conflicts/`
       Does this look correct?

User: yes

Agent: Created worktree at `_worktrees/package-conflicts/`
       Effort initialized.

       Would you like to start framing the problem space?
       1. Yes — start with Effort Framer agent
       2. No — I'll add content manually
```
