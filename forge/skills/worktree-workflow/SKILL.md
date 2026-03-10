---
name: worktree-workflow
description: >-
  This skill should be used when "creating a worktree",
  "worktree naming", "ephemeral branch", "merge from
  worktree", "worktree cleanup", or navigating between
  worktrees. Covers naming conventions, ephemeral branch
  patterns, the CWD trap, and worktree setup. Do not use
  for general git workflow.
---

# Worktree Workflow

Git worktree patterns for parallel development work. Enables
working on multiple features/tickets simultaneously without
branch switching.

## Core Convention

**All worktrees live in `_worktrees/` subfolder:**

```
{repo}/                              # Main checkout (on main)
{repo}/_worktrees/                   # Worktrees folder
{repo}/_worktrees/{worktree-name}/   # Individual worktree
```

## Naming Conventions

### Forge Slice Worktrees

| Element | Pattern | Example |
|---------|---------|---------|
| Folder | `{slice-slug}` | `auth-refactor` |
| Branch | `slice/{slug}-{phase}-{suffix}` | `slice/auth-refactor-design-a1b2` |

### Forge Effort Worktrees

| Element | Pattern | Example |
|---------|---------|---------|
| Folder | `{effort-slug}` | `cloud-migration` |
| Branch | `effort/{slug}-{suffix}` | `effort/cloud-migration-a1b2` |

### Implementation Ticket Worktrees

| Element | Pattern | Example |
|---------|---------|---------|
| Folder | `{feature-slug}-{ticket-num}` | `auth-refactor-42` |
| Branch | `{feature-slug}/{ticket-num}-{desc}` | `auth-refactor/42-jwt-validation` |

## Ephemeral Branch Pattern

**Branches are single-use:** create → push → merge → delete

- Each set of changes gets a unique branch
- After merge, create a fresh branch for next changes
- No branch resets needed — each PR starts fresh from main
- Multiple contributors can work in parallel

**Example lifecycle:**
```
slice/auth-refactor-requirements-a1b2  # Created, merged, deleted
slice/auth-refactor-design-c3d4        # Created, merged, deleted
slice/auth-refactor-impl-e5f6          # Created, merged, deleted
```

**Why?** Eliminates the painful reset cycle:
> merge → git reset --hard origin/main → git push --force

## Creating a Worktree

Always specify the starting branch (typically `origin/main`)
when creating with `-b` — omitting it starts the branch from
current `HEAD`, which may be a feature branch, pulling
unrelated commits into your PR.

### Manual Creation

```bash
mkdir -p _worktrees
# ALWAYS specify origin/main as the starting point
git worktree add _worktrees/auth-refactor \
  -b slice/auth-refactor-design-a1b2 origin/main
cd _worktrees/auth-refactor
```

### Common Mistake: Omitting Base Branch

```bash
# WRONG - branches from current HEAD (might be a feature branch!)
git worktree add _worktrees/my-feature -b feature/my-feature

# RIGHT - always specify origin/main
git worktree add _worktrees/my-feature \
  -b feature/my-feature origin/main
```

## Working in a Worktree

```bash
# Navigate to worktree
cd {repo}/_worktrees/{worktree-name}

# Work normally — all git commands work
git status
git add .
git commit -m "feat(scope): Description"
git push -u origin {branch-name}
```

## Merging PRs

**IMPORTANT:** Always merge from main repository, not from
worktrees.

### The Problem

```bash
cd _worktrees/my-feature
gh pr merge 123 --rebase --delete-branch
# Error: fatal: 'main' is already used by worktree at '/path/to/repo'
```

**Why:** The `--rebase` merge needs to check out `main`, which
is already checked out in the main repository directory.

### The Solution

```bash
# From your worktree
cd _worktrees/my-feature
git push  # Ensure your work is pushed

# Navigate to main repository
cd ../..  # Or: cd /path/to/repo

# Merge from main repository
gh pr merge 123 --rebase --delete-branch
```

### Alternative: Web UI

Merge via GitHub's web interface (no worktree limitation).
Use "Rebase and merge" to maintain linear history.

## Removing a Worktree

```bash
# Remove worktree (keeps branch)
git worktree remove _worktrees/{worktree-name}

# Optionally delete the branch if merged
git branch -d {branch-name}
```

### CRITICAL: CWD Trap That Kills Your Session

**If the shell's CWD is inside a worktree directory when that
directory is deleted, the shell breaks permanently for the
session.** Even `echo hello` will fail.

**How it happens:**
1. You work in a worktree (CWD persisted to worktree dir)
2. You chain: `cd /repo && git worktree remove _worktrees/X`
3. The remove succeeds but a chained branch delete fails
4. Shell does not persist the cd from a failed command
5. Next command tries to start in the deleted directory

**Prevention:**
- cd to repo root in a **separate shell call** before removing
- Never chain cd and remove in one command

```bash
# WRONG - cd and remove in same command
cd /repo && git worktree remove _worktrees/X

# RIGHT - separate calls
cd /repo                              # Call 1 (must succeed)
git worktree remove _worktrees/X      # Call 2
```

## Navigation Best Practices

**Problem:** Relative paths (`_worktrees/...`) only work from
repo root. If you're already inside a worktree, they fail.

### Use Absolute Paths

```bash
# Get absolute path from git (works from anywhere)
WORKTREE_PATH=$(git worktree list | \
  grep "my-feature" | awk '{print $1}')

# Check if already there
CURRENT=$(pwd)
if [ "$CURRENT" = "$WORKTREE_PATH" ]; then
  echo "Already in worktree"
else
  cd "$WORKTREE_PATH"
fi
```

### Navigate to Repo Root First

```bash
# Go to repo root, then use relative path
cd "$(git rev-parse --show-toplevel)"
cd _worktrees/my-feature
```

### Listing Worktrees

```bash
# Use git as source of truth (works from anywhere)
git worktree list
```

## Best Practices

1. **One Work Item Per Worktree**
   - Don't mix multiple tickets/features
   - Makes PRs cleaner and easier to review

2. **Clean Up After Merge**
   - Remove worktrees after PR merge
   - Prevents accumulation of stale directories

3. **Keep Main Clean**
   - Don't make changes in main checkout
   - Use worktrees for all feature/ticket work

4. **Consistent Naming**
   - Follow naming conventions strictly
   - Makes automation and scripting easier

5. **Merge from Main Checkout**
   - Always run `gh pr merge` from main repository

## Troubleshooting

### Worktree Already Exists

```bash
# Check if worktree exists
git worktree list | grep {name}

# If stale, prune and recreate
git worktree prune
git worktree add _worktrees/{name} -b {branch} origin/main
```

### Branch Already Exists

```bash
# If branch exists but no worktree
git worktree add _worktrees/{name} {existing-branch}

# If need to reset
git branch -D {branch}
git worktree add _worktrees/{name} -b {branch} origin/main
```

### "No such file or directory" When Navigating

**Symptom:** `cd _worktrees/my-feature` fails even though
`git worktree list` shows it exists.

**Cause:** Using relative path from inside another worktree.

**Solution:** Use absolute paths from `git worktree list`.

## Summary

| Aspect | Pattern |
|--------|---------|
| **Location** | `{repo}/_worktrees/` |
| **Naming** | `{slug}` or `{slug}-{ticket-num}` |
| **Branch** | Ephemeral, single-use |
| **Creation** | ALWAYS specify `origin/main` as base |
| **Merging** | ALWAYS from main repo, not worktree |
| **Navigation** | Use absolute paths, never relative |

**Key principles:**
- Ephemeral branches (single-use, no resets)
- Absolute paths (never rely on relative paths)
- Merge from main (avoid worktree limitations)
- One work item per worktree (clear separation)
