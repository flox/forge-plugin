# /forge:investigate

Ad-hoc issue triage and investigation.

## This Command's Role

Entry point for investigating reported issues, regressions,
and unexpected behavior. Guides the user through structured
triage before spawning an investigation agent.

**Key principle: Understand before acting.** This command
ensures proper triage happens before investigation begins,
and that investigation completes before any external
artifacts (issues, PRs, comments) are created.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks
- Use exit codes for control flow, not error messages

## Workflow

### Step 1: Capture Report

If the user provided an issue description with the command,
use it. Otherwise ask:

> "What issue are you investigating? Describe what you're
> seeing, including any error messages, affected
> components, or user reports."

Accept free-form input. Don't interrupt — let the user
describe the full situation.

### Step 2: Triage Questions

Ask structured clarifying questions. Do NOT skip this step.

**Batch 1 — Reproduction and behavior:**
- Can you reproduce the issue?
  (Yes / Sometimes / No / Haven't tried)
- What is the expected vs. actual behavior?

**Batch 2 — Timeline and scope:**
- When did this last work correctly?
  (Recently / Never worked / Not sure / New functionality)
- Which parts of the project are affected?
  (Free-form, or suggest based on report)

**Batch 3 — Urgency:**
- Is this blocking anyone right now?
  (Yes — production / Yes — development / No)

Adapt questions based on earlier answers. Skip questions
the report already answers clearly.

### Step 3: Classify

Based on the report and triage answers, classify the issue:

| Classification | Criteria |
|----------------|----------|
| **Confirmed regression** | Previously worked, now broken, reproducible |
| **Suspected regression** | Previously worked, now broken, not yet reproduced |
| **Incomplete work** | Feature never fully worked; new functionality |
| **Config issue** | Likely deployment or configuration problem |
| **Unclear** | Not enough information to classify |

Present the classification:

> "Based on your answers, this looks like **{classification}**."
>
> "{1-2 sentence reasoning}"

### Step 4: Confirm Scope

Present the planned investigation scope:

> **Investigation plan:**
> - Classification: {classification}
> - Parts to investigate: {list}
> - Investigation depth: {light | standard | deep}
> - Estimated scope: {brief description}
>
> **This is READ-ONLY investigation.** No issues, PRs,
> or comments will be created without your explicit
> approval.
>
> Proceed with investigation?

Wait for user confirmation before proceeding.

**Investigation depth by classification:**
- Confirmed/suspected regression: **deep** — git log,
  blame, related issues/PRs, code analysis
- Incomplete work: **light** — feature status, current
  implementation state
- Config issue: **standard** — configuration analysis,
  environment comparison
- Unclear: **standard** — broad survey, then narrow

### Step 5: Spawn Investigation Agent

```
Use Task tool with:
- subagent_type: "Issue Investigator"
- prompt: |
    ## Inputs
    - classification: {determined classification}
    - description: {original issue report}
    - triage_answers: {summary of triage Q&A}
    - repos: {list of repos to investigate}
    - depth: {investigation depth level}
```

The agent handles the investigation and returns structured
findings. Display the findings to the user.

### Step 6: Post-Investigation Actions

After the agent returns findings, present options:

> **What would you like to do?**
> 1. Create a GitHub issue with these findings
> 2. Add a comment to an existing issue
> 3. Save findings as an artifact
> 4. Take no action (investigation complete)

Each external action gets **separate confirmation** before
execution. See Skill: `forge-signature` for all GitHub
posts.

## Example Interactions

```
User: /forge:investigate

Agent: What issue are you investigating?

User: Users are getting 401 errors after we deployed
      the new auth changes last week.

Agent: [Batch 1 questions]

User: [answers]

Agent: Based on your answers, this looks like a
       **suspected regression** — the auth changes
       introduced a regression for existing sessions.

Agent: Investigation plan:
       - Classification: suspected regression
       - Parts: auth module, session handling
       - Depth: deep

       This is READ-ONLY investigation. Proceed?

User: Yes, proceed.

Agent: [spawns issue-investigator, displays findings]

Agent: What would you like to do with these findings?

User: Create a GitHub issue.

Agent: [confirms details, creates issue]
```

## Subcommands

None — this command enters interactive mode directly.
