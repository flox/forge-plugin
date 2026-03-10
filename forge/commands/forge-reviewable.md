# /forge-reviewable

Transform messy commits into atomic, reviewable units
organized by review concern.

## This Command's Role

Entry point for restructuring commits — either uncommitted
changes (Mode A) or existing commit history (Mode B).
Guides the user through analysis, plan approval, and
execution using specialized agents.

**Key principle: Organize by review concern, not file
proximity.** Changes requiring different review thinking
belong in different commits, even within the same file.

**Safety model: Non-destructive dual-branch.** The original
branch and working directory are never modified. Restructured
commits are created on a new ephemeral branch in an isolated
worktree. A parity check proves the restructured branch
produces the same final tree as the original.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks

## Usage

```
/forge-reviewable [options] [target]
```

**Options:**
- `-i`, `--interactive` — per-commit approval with preview

**Targets:**
- *(none)* — auto-detect from `git status`
- `<folder>` — Mode A on uncommitted changes in folder
- `<folder> <hash>` — Mode B from commit hash in folder
- `<PR-number>` — Mode B on PR commits
- `<PR-URL>` — Mode B on PR commits via GitHub URL
- `<commit-hash>` — Mode B from commit in current directory

## Workflow

### Step 1: Parse Arguments

Extract the interactive flag and identify the target:

```bash
INTERACTIVE=false
for arg in "$@"; do
  case "$arg" in
    -i|--interactive) INTERACTIVE=true ;;
  esac
done
```

**Identify target type:**

| Input Pattern | Detection | Mode |
|---------------|-----------|------|
| No args | Check `git status` | A if changes, else ask |
| Path exists as directory | `test -d <arg>` | A |
| Directory + hex string | dir + `git rev-parse` | B |
| Number only (1-6 digits) | PR number | B |
| `https://github.com/*/pull/*` | PR URL | B |
| 7-40 hex chars | `git rev-parse <arg>` | B |

### Step 2: Determine Mode and Capture Original State

- **Mode A** — uncommitted/untracked changes to organize
  into atomic commits
- **Mode B** — existing commit range to restructure

For **PR targets**:
```bash
gh pr checkout <number>
BASE_COMMIT=$(git merge-base origin/<base-branch> HEAD)
```

**Record the original state** (never modify it):
```bash
ORIGINAL_TIP=$(git rev-parse HEAD)
```

If no changes exist and no base commit is specified,
inform the user there's nothing to restructure.

### Step 3: Create Ephemeral Worktree

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
SUFFIX=$(head /dev/urandom | tr -dc 'a-z0-9' | head -c 4)
BRANCH="reviewable/${SLUG}-${SUFFIX}"
RESTRUCTURE_DIR="${REPO_ROOT}/_worktrees/reviewable-${SLUG}"

git worktree add "$RESTRUCTURE_DIR" \
  -b "$BRANCH" "$BASE_COMMIT"
```

**Mode A — apply uncommitted changes to the worktree:**

```bash
git diff > /tmp/reviewable-tracked.patch
UNTRACKED=$(git ls-files --others --exclude-standard)

if [ -s /tmp/reviewable-tracked.patch ]; then
  git -C "$RESTRUCTURE_DIR" apply \
    /tmp/reviewable-tracked.patch
fi

for f in $UNTRACKED; do
  mkdir -p "$RESTRUCTURE_DIR/$(dirname "$f")"
  cp "$f" "$RESTRUCTURE_DIR/$f"
done
```

**Mode B — apply the full diff to the worktree:**

```bash
git diff "$BASE_COMMIT" "$ORIGINAL_TIP" \
  > /tmp/reviewable-full.patch
git -C "$RESTRUCTURE_DIR" apply /tmp/reviewable-full.patch
```

### Step 4: Analyze Changes — Spawn Story Architect

Gather inputs and spawn the agent:

```
Use Task tool with:
- subagent_type: "Commit Story Architect"
- prompt: |
    ## Inputs
    - mode: {A or B}
    - diff_output: {diff}
    - commit_log: {log, Mode B only}
    - pr_metadata: {PR metadata if applicable}
    - working_directory: {path}
    - restructure_worktree: {restructure dir path}

    Analyze these changes and produce a structured commit
    plan following the Story Architect process.
```

### Step 5: Present Plan for Approval

Display the plan to the user. For each commit show:
- Commit type, scope, and subject line
- **Review depth** marker (high/medium/low) with reason
- Files affected
- Why this commit exists in the narrative

Lead with the review depth summary:

> **Proposed commit structure** — {N} commits in
> {M} phases.
>
> **Review depth summary:**
> - {X} high — need deep focus
> - {Y} medium — normal review
> - {Z} low — quick scan
>
> {plan details}

Ask for approval:
- "Yes, execute the plan"
- "Revise — I have feedback"
- "Abort — cancel restructuring"

If the user wants changes, relay feedback to the Story
Architect and present the revised plan. If aborted, clean
up the worktree and exit.

### Step 6: Execute the Plan

**Standard mode** — spawn the Commit Builder:

```
Use Task tool with:
- subagent_type: "Commit Builder"
- prompt: |
    ## Inputs
    - story_plan: {the approved plan}
    - restructure_worktree: {restructure dir path}
    - original_branch_tip: {ORIGINAL_TIP hash}
    - repo_root: {REPO_ROOT path}

    Execute the commit plan. Create all commits and
    run the parity check.
```

**Interactive mode** — iterate through the plan
with user control. For each commit:

1. Show the proposed commit (type, scope, subject, files)
2. Stage the files in the restructure worktree
3. Show the staged diff:
   `git -C "$RESTRUCTURE_DIR" diff --cached`
4. Ask: "Accept this commit? (Yes / Edit / Skip / Quit)"

- **Yes** — create commit, continue
- **Edit** — ask for new message, create commit, continue
- **Skip** — unstage, record as skipped, continue
- **Quit** — unstage all remaining, inform about worktree
  preservation, exit

### Step 7: Verification

Display the parity check results.

**If passed:**
> "Parity check passed — zero code loss confirmed."
> "{N} commits created across {M} phases."

**If failed unexpectedly:**
> "Parity check FAILED — unexpected differences detected."
> "The restructured worktree at {RESTRUCTURE_DIR} is
> preserved for investigation."
> "Your original branch is untouched."

### Step 8: Completion and Cleanup

After successful verification, present options:

> "Restructured commits ready on branch `{BRANCH}`."
>
> "Your original branch is completely untouched. Options:
>
> 1. Push the restructured branch and open a new PR
> 2. Keep locally — I'll handle it
> 3. Discard — clean up everything"

**If pushing:**
```bash
git -C "$RESTRUCTURE_DIR" push -u origin "$BRANCH"
echo "Create a PR with: gh pr create --head $BRANCH"
```

**Cleanup:**
```bash
git worktree remove "$RESTRUCTURE_DIR"
# Delete ephemeral branch if not pushed
git branch -D "$BRANCH" 2>/dev/null || true
```

Mention that `/forge-retro-note` can capture feedback.

## Context Files to Read

- `.forge-context/context/principles.md` — Engineering
  principles for commit organization guidance

## Example Interactions

### Mode A: Uncommitted Changes

```
User: /forge-reviewable
Agent: Analyzing git status...
       Found 12 modified files with uncommitted changes.
       Mode A: organizing uncommitted changes.

       [spawns Story Architect]

Agent: Proposed commit structure — 5 commits in 2 phases.

       Review depth: 1 high, 2 medium, 2 low

       Phase 1: Configuration (2 commits)
         1. [low] chore(config): add feature flag
         2. [low] chore(deps): update dependency

       Phase 2: Implementation (3 commits)
         3. [high] feat(auth): add JWT verification
         4. [medium] chore(observability): add metrics
         5. [medium] test(auth): add JWT tests

       Proceed with this plan?

User: Yes
Agent: [spawns Commit Builder]
       Parity check passed — zero code loss confirmed.
       5 commits created on branch reviewable/auth-a3k9.
```

### Mode B: PR Restructuring

```
User: /forge-reviewable 3957
Agent: Fetching PR #3957...
       "Refactor manifest system" — 18 commits
       Mode B: restructuring commit range.

       [spawns Story Architect, presents plan]

User: Yes
Agent: Parity check passed.

       Restructured branch: reviewable/pr-3957-x7m2
       Original PR branch: untouched

       Push restructured branch and open new PR?
```

## Subcommands

None — this command enters interactive mode based on
arguments.
