# /forge:process-pr-discussions

Process unresolved PR discussions by applying conclusions
and recording decisions.

## This Command's Role

Identifies the PR, then follows Skill:
`pr-discussion-orchestration` to execute the three-phase
processing pattern. Orchestration happens here — in the
calling context that has Task access — not inside the
`PR Discussion Processor` agent.

## Behavior

### Step 1: Identify PR

Check for argument or prompt:
- If PR number/URL provided as argument, use it
- Otherwise, search for PRs on current branch:
  ```bash
  git branch --show-current
  gh pr list --head $(git branch --show-current)
  ```
- If multiple found, ask which one

### Step 2: Confirm Scope

> "Found PR #{number}: {title}"
> "This PR has {n} unresolved discussion threads."
>
> "Process all discussions?
> (yes / specific threads / cancel)"

### Step 3: Follow PR Discussion Orchestration

Load Skill: `pr-discussion-orchestration` and execute the
three-phase pattern.

**Phase 1: Analyze (spawn PR Discussion Processor)**

```
Use Task tool with:
- subagent_type: "PR Discussion Processor"
- prompt: |
    ## Inputs
    - pr_number: {pr_number}
    - owner: {owner}
    - repo: {repo}
    - feature_path: {feature_path if available}
    - mode: "analyze-only"

    Execute Steps 1-3 to classify threads and extract
    conclusions. Produce a DELEGATION_PLAN in your output.
    Do NOT apply changes or spawn agents.
```

Read the `DELEGATION_PLAN` from Phase 1 output.

**Phase 2: Delegate (this command)**

If `needs_delegation: true` in the plan:

```
Use Task tool with:
- subagent_type: {plan.agent in title case}
- prompt: |
    Apply PR discussion conclusions.

    ## Context
    PR: {owner}/{repo}#{pr_number}
    Branch: {headRefName}
    Slice path: {slice_path for doc PRs}
    Repository path: {repo_path for code PRs}

    ## Changes to apply
    {plan.thread_conclusions formatted as structured list}

    ## After applying
    Commit changes and report: what changed, commit SHA.
    Do NOT reply to or resolve PR threads.
```

Wait for the sibling agent to complete. Capture the
commit SHA and summary.

If `needs_delegation: false`: skip Phase 2.

**Phase 3: Resolve (spawn PR Discussion Processor again)**

```
Use Task tool with:
- subagent_type: "PR Discussion Processor"
- prompt: |
    ## Inputs
    - pr_number: {pr_number}
    - owner: {owner}
    - repo: {repo}
    - feature_path: {feature_path if available}
    - mode: "resolve"
    - prior_conclusions: {Phase 1 DELEGATION_PLAN}
    - delegation_result: {Phase 2 outcome or null}

    Execute Steps 5-9: apply any direct threads,
    reply to processed threads, resolve threads,
    assess discussion health, report final counts.
```

### Step 4: Report Results

Display the Phase 3 agent's output:
- Total unresolved threads found
- Number processed and resolved
- Number remaining open
- Actions taken (code changes, decisions recorded)
- List of threads left open with reasons

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Search for PR on current branch |
| `{pr_number}` | Use specific PR number |
| `{pr_url}` | Use PR from URL |

## Example Interaction

```
User: /forge:process-pr-discussions

Agent: Searching for PR on current branch...
       Found PR #42: Design Review: CUDA Build Support

       This PR has 4 unresolved discussion threads.

       Process all discussions? (yes/specific/cancel)

User: yes

Agent: Processing discussions...
       [spawns PR Discussion Processor]

Agent: PR Discussion Processing Complete

PR: #42 — Design Review: CUDA Build Support
Total unresolved threads: 4
Processed and resolved: 2
Remaining open: 2

Actions taken:
1. Thread on design.md line 45
   - Applied: Updated error handling approach
   - Commit: abc1234
   - Replied and resolved

2. Thread on design.md line 102
   - Recorded decision: "Use async API for queries"
   - Added to decisions.md
   - Replied and resolved

Threads left open (need human review):
- design.md:156: Unanswered performance question
- requirements.md:23: Ongoing discussion
```

## Error Cases

### No PR Found
```
Agent: Could not find an open PR for the current branch.

Options:
1. Enter PR number manually
2. Enter PR URL

PR number or URL?
```

### No Unresolved Discussions
```
Agent: PR #42 has no unresolved discussion threads.

Nothing to process.
```
