# /forge-phase-complete

Complete the current phase by capturing a review summary
before merge.

## This Command's Role

Interactive wrapper that identifies the PR and phase, then
delegates to the `Phase Completer` agent to capture the
review and finalize.

## Behavior

### Step 1: Identify Current Slice

Check current working directory or ask which slice.

**CRITICAL: When in a worktree, read all slice files
from the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/slices/{YYYYMM}-{slug}/checklist.md
Wrong:   /path/to/project/.forge-context/slices/{YYYYMM}-{slug}/checklist.md
```

### Step 2: Determine Current Phase

Use the phase derivation logic to identify which phase
is in progress.

**Phase derivation:**
1. Check for review summaries:
   - `reviews/requirements-review.md` exists → req done
   - `reviews/design-review.md` exists → design done
2. Check for document content:
   - `requirements.md` has content → requirements started
   - `design.md` has content → design started
   - `tasks.md` has content → implementation started
3. Derive current phase from the signals above

### Step 3: Find or Confirm PR

Search for the relevant PR:
```bash
git branch --show-current
gh pr list --head $(git branch --show-current)
```

If found:
> "Found PR #{number}: {title}"
> "Is this the PR to complete? (yes/no)"

If not found or multiple:
> "Which PR number should I capture the review from?"

### Step 4: Spawn Subagent

Spawn the `Phase Completer` agent:

```
Use Task tool with:
- subagent_type: "Phase Completer"
- prompt: |
    ## Inputs
    - feature_path: {slice_path}
    - feature_name: {slice_name}
    - phase: {requirements | design | implementation}
    - pr_number: {pr_number}
```

The subagent will:
- Fetch PR reviews and comments via GitHub API
- Generate review summary document
- Update checklist
- Commit changes

### Step 5: Report Completion

Display the subagent's output:
- Review summary created
- Key discussions captured
- Ready to merge status
- Next phase guidance

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Auto-detect slice and PR |
| `{pr_number}` | Use specific PR number |

## Example Interaction

```
User: /forge-phase-complete

Agent: Working on **CUDA Build Support**,
       requirements phase.

       Searching for PR...
       Found PR #42: Requirements: CUDA Build Support

       Is this the PR to complete? (yes/no)

User: yes

Agent: Capturing review... [spawns Phase Completer]

Agent: Phase completion for CUDA Build Support:

PR: #42 — Requirements: CUDA Build Support
Status: Approved

Reviewers:
- @alice - Approved
- @bob - Approved

Key discussions captured: 3
Changes during review: 2

Review summary created: reviews/requirements-review.md

The PR is ready to merge. After merging:
- Run `/forge-design` to start the design phase
```

## With PR Number

```
User: /forge-phase-complete 55

Agent: Capturing review for PR #55...
       [spawns Phase Completer]
```

## Error Cases

### No PR Found
```
Agent: Could not find an open PR for the
       requirements phase.

Options:
1. Enter PR number manually
2. Check that PR exists and try again

PR number?
```

### Not Yet Approved
```
Agent: PR #42 does not have required approvals yet.

Current reviews:
- @alice - Approved
- @bob - Changes Requested (pending)

Wait for all reviews to be resolved before completing
the phase.
```
