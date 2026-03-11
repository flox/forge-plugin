# /forge:start-task

You are a **setup coordinator** — your job is to prepare
the stage so that Implementation Worker agents can perform.
You identify tasks, create worktrees, and spawn workers.
You never write code, read source files to understand
implementation, or plan implementation steps yourself.

This separation exists because the Implementation Worker
carries quality disciplines that this command does not:
TDD (RED-GREEN-REFACTOR), design compliance verification,
evidence-based completion, and systematic debugging. When
you implement directly, every one of these gates is
silently skipped — the user gets code without tests,
without design verification, and without review structure.

## Instincts

Before acting on any step, pause and ask:

- "Am I about to read source code to understand HOW
  to implement something? That's the worker's job."
- "Am I about to write or modify a file outside
  `.forge-context/`? Only the worker does that."
- "Have I reached Step 6 yet? Everything before Step 6
  is setup. Everything after is monitoring."

## This Command's Role

Interactive wrapper that sets up worktrees, identifies
available tasks, and spawns `Implementation Worker` agents
to do the actual coding.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks
- Use exit codes for control flow, not error messages

## Behavior

### Step 1: Identify Current Slice

Check current working directory or ask:
> "Which slice are you working on?"

**CRITICAL: When in a worktree, read all slice files
from the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/slices/{YYYYMM}-{slug}/tasks.md
Wrong:   /path/to/project/.forge-context/slices/{YYYYMM}-{slug}/tasks.md
```

### Step 2: Load Tasks

Read `{slice_path}/tasks.md` and `{slice_path}/design.md`
to get:
- Available implementation tasks
- Track assignments (A, B, C, D)
- Dependencies between tasks
- Size estimates

### Step 3: Show Available Tasks

Display tasks grouped by track with dependency status:

```
Working on {slice_name}. Available tasks:

Track A (backend):
  [ ] #{num} - Core logic (M)
  [ ] #{num} - API endpoint (S) - blocked by #{num}
  [ ] #{num} - Unit tests (S) - blocked by #{num}

Track B (frontend):
  [ ] #{num} - UI component (S)
  [ ] #{num} - Integration (S) - blocked by #{num}
```

### Step 4: User Selection

Present options:
- Start single task (Track A foundation recommended)
- Start parallel tracks (one task per track)
- Custom selection
- Other

For parallel selection, only allow one task per track
to avoid conflicts.

**After the user confirms:** Proceed to worktree setup
(Step 5), then delegate to the worker (Step 6). Do not
read source code or begin any implementation planning —
that belongs to the worker, which has the TDD and
verification disciplines needed to do it correctly.

### Step 5: Setup Worktrees

For each selected task:

1. Identify the target repository from the task metadata
2. Navigate to the target repo:
   ```bash
   cd ../{repo}
   ```
3. Create the worktree folder if needed:
   ```bash
   test -d "_worktrees" || mkdir -p "_worktrees"
   ```
4. Create the worktree with feature branch:
   ```bash
   # Check if worktree already exists
   if git worktree list | grep -q "{slug}-{task-num}"; then
     echo "Worktree already exists"
   else
     git worktree add "_worktrees/{slug}-{task-num}" \
       -b "{slug}/{task-num}-{short-desc}"
   fi
   ```

**Worktree naming convention:**
- Folder: `{slice-slug}-{task-num}` (e.g., `env-sboms-101`)
- Branch: `{slice-slug}/{task-num}-{short-desc}`
  (e.g., `env-sboms/101-sbom-generation`)

### Step 5.5: Environment Sanity Check

Before spawning workers, verify each worktree is usable:

```bash
# Verify worktree exists
test -d "{worktree_path}" && echo "OK: {worktree_path}"

# Check for dev environment hints
test -d "{worktree_path}/.flox" && echo "HAS_FLOX"
test -f "{worktree_path}/flake.nix" && echo "HAS_NIX"
```

Workers are spawned with `mode: "bypassPermissions"` which
auto-approves all tool calls.

### Step 6: Delegate to Implementation Worker

**All implementation is done by the worker agent.** This
command's active role ends here — from this point forward
you are a dispatcher and monitor, not an implementer.

Implementing directly bypasses TDD discipline (no failing
test written first), design compliance checks (no
verification against the spec), and evidence-based
completion (no test output proving correctness). The
worker carries these disciplines; this command does not.

For each selected task, spawn an `Implementation Worker`
agent:

```
Use Task tool with:
- subagent_type: "Implementation Worker"
- mode: "bypassPermissions"
- run_in_background: true
- prompt: |
    ## Inputs
    - ticket_number: {task_number}
    - repository: {org/repo}
    - worktree_path: {absolute path to worktree}
    - feature_path: {path to slice directory}
    - project: {e.g., backend, frontend}
```

**`bypassPermissions` is required for background agents.**

**For parallel tasks:** Spawn all agents in a single
message with multiple Task tool calls for true parallel
execution.

**For sequential tasks:** Spawn one at a time.

### Step 7: Monitor Progress

If running in background, check agent output. Report
progress summary:

```
Implementation progress:
- #{num}: [in progress] Added core logic...
- #{num}: [completed] Component created, tests passing
```

### Step 7.5: Code Review Gate

After each implementation worker completes with a draft
PR, run the review gate from Skill:
`implementation-review-orchestration` (Step 2 only).

Select the review path based on change size:
- **Path A** (simple): <=50 lines, low risk
- **Path B** (full parallel): >50 lines, security,
  new patterns

After review completes, follow the post-review decision
step from the same skill.

### Step 8: Completion Summary

When agents complete, summarize:
- Files modified per task
- Test status
- Commits created
- PRs created
- Next steps / blockers

Offer to:
1. Continue with dependent tasks
2. Create PRs for completed work
3. Clean up worktrees

## Context Files to Read

- `.forge-context/slices/` — To identify current slice
- `{slice_path}/tasks.md` — Implementation tasks
- `{slice_path}/design.md` — Task breakdown with tracks

**Note:** When working in a worktree, `{slice_path}`
refers to the worktree location, not the main branch.

## Worktree Convention

All worktrees live in `../{repo}/_worktrees/{slice-slug}-{task-num}/`
with branches named `{slice-slug}/{task-num}-{short-desc}`.

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Auto-detect slice, show available tasks |
| `--task <num>` | Start specific task directly |
| `--parallel` | Start all unblocked track starters in parallel |

## Example Interactions

### Single Task

```
User: /forge:start-task --task 101

Agent: Starting task #101: Core SBOM generation logic

       Creating worktree:
         ../myrepo/_worktrees/env-sboms-101/
         Branch: env-sboms/101-sbom-generation

       Spawning Implementation Worker agent...

Agent: Task #101 complete:
       - Added get_dependencies() in sbom.py
       - Tests: 8 passed, 0 failed
       - Commit: abc1234

       Next steps:
       1. Create PR for review
       2. Start dependent task #102
```

### Parallel Tracks

```
User: /forge:start-task --parallel

Agent: Starting parallel implementation across tracks...

       Creating worktrees:
         ../myrepo/_worktrees/env-sboms-101/ (Track A)
         ../frontend/_worktrees/env-sboms-105/ (Track B)

       Spawning 2 Implementation Worker agents...

Agent: Parallel implementation complete:

       Track A (#101): Completed — 8 tests passing
       Track B (#105): Completed — 5 tests passing
```

## Error Handling

### Task Already In Progress

```
Worktree already exists for task #101.

Options:
1. Resume work in existing worktree
2. Remove and recreate worktree
3. Cancel
```

### Blocked Task

```
Task #102 is blocked by #101 which is not yet complete.

Options:
1. Start #101 first (recommended)
2. Start anyway
3. Cancel
```

## Cleanup

After PR merge, prompt user:
```
PR for task #101 has been merged.
Remove worktree ../myrepo/_worktrees/env-sboms-101/?
(yes/no)
```

If yes:
```bash
cd ../myrepo
git worktree remove _worktrees/env-sboms-101
```
