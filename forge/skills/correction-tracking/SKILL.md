---
name: correction-tracking
description: >-
  This skill should be used when the user redirects,
  corrects, or refines agent output — "no, actually",
  "that's not right", "you missed something". Captures
  correction moments to improve Forge workflows over time.
  Always active during feature work; log corrections as
  they occur.
---

# Correction Tracking Pattern

All Forge agents should track "correction moments" — instances
where the user redirects, corrects, or refines the agent's
output. These are valuable signals for workflow improvement.

## Note Format with Status Tracking

Each note includes a status marker for incremental processing
by `/forge-improve`.

```markdown
## YYYY-MM-DD: {Phase}

### Note {N}: {Brief Title}
<!-- STATUS: UNPROCESSED -->

**Context:** ...
**What happened:** ...
**Recommendation:** ...

---
```

**Status values:**
- `UNPROCESSED` — New note, not yet reviewed by audit
- `PROCESSED: {date} | Applied: {file} | PR: #{pr}` —
  Change was made
- `PROCESSED: {date} | Skipped: {reason}` — Decided not to
  act
- `PROCESSED: {date} | Deferred: #{issue}` — Created ticket
  for later

Notes without any status marker are treated as `UNPROCESSED`
(for backwards compatibility with existing notes).

## What is a Correction?

A correction occurs when the user:
- Says "no, actually..." or "that's not right..."
- Provides significantly different input than what was
  suggested
- Asks the agent to redo or revise work
- Points out something the agent missed or assumed
  incorrectly
- Manually edits agent-generated content substantially

## When to Track

Track corrections when they indicate:
- **Template gaps**: Agent didn't have the right starting
  structure
- **Context gaps**: Agent didn't have information it needed
- **Assumption errors**: Agent assumed something that wasn't
  true
- **Process gaps**: A step was missing from the workflow
- **Checklist gaps**: Something important wasn't being tracked

**Don't track** minor stylistic preferences or typo fixes.

## How to Track

When you detect a correction, append to
`{feature_path}/artifacts/retrospective-notes.md`:

```markdown
## {date}: {Phase}

### Note {N}: {Brief Title}
<!-- STATUS: UNPROCESSED -->

**Agent:** {agent name}

**What happened:**
{Brief description of what the agent did or suggested}

**User correction:**
{What the user said or did to correct it}

**Root cause:**
{Why did the agent get it wrong? Missing context? Bad
assumption? Template gap?}

**Recommendation:**
{What change might prevent this in the future?}

---
```

## Creating the File

If `artifacts/retrospective-notes.md` doesn't exist, create
it with this header:

```markdown
# Retrospective Notes: {feature_name}

Correction moments captured during feature development.
These inform workflow improvements.

---

```

## Example Corrections

### Template Gap
```markdown
## 2026-01-09: Requirements

### Note 1: Missing infrastructure dependencies section
<!-- STATUS: UNPROCESSED -->

**Agent:** requirements-gatherer

**What happened:**
Generated requirements without an "Infrastructure
Dependencies" section.

**User correction:**
"We need a section for infrastructure dependencies —
this feature requires specific server capabilities."

**Root cause:**
Requirements template doesn't have an infrastructure
dependencies section.

**Recommendation:**
Add "Infrastructure Dependencies" section to requirements
template.

---
```

### Context Gap
```markdown
## 2026-01-09: Design

### Note 2: Incorrect component placement in architecture
<!-- STATUS: PROCESSED: 2026-01-15 | Applied: context/product.md | PR: #42 -->

**Agent:** designer

**What happened:**
Suggested adding feature support directly to the wrong
component.

**User correction:**
"This should go through the data layer, not the API layer."

**Root cause:**
Agent didn't understand the separation between API and
data layer responsibilities.

**Recommendation:**
Add data layer vs API layer responsibility breakdown to
context/product.md.

---
```

### Assumption Error
```markdown
## 2026-01-09: Design

### Note 3: Incorrect project impact assessment
<!-- STATUS: PROCESSED: 2026-01-16 | Deferred: #55 -->

**Agent:** designer

**What happened:**
Listed a service as affected for a client-only change.

**User correction:**
"This doesn't touch that service at all, it's entirely
client-side."

**Root cause:**
Agent assumed all environment changes require service
updates.

**Recommendation:**
Update designer to distinguish client-only vs
service-affecting changes.

---
```

## Integration with Agent Workflow

Agents should:

1. **Watch for correction signals** in user messages
2. **Acknowledge the correction** to the user
3. **Log the correction** to retrospective-notes.md
4. **Learn in-session** — don't repeat the same mistake
5. **Continue with corrected approach**

Example response when detecting a correction:

> "Got it, I'll update my approach. [Noting this for
> the retrospective — the {X} assumption wasn't correct
> for this case.]"

The bracketed note signals transparency without being
disruptive.
