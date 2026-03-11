---
name: effort-lifecycle
description: >-
  This skill should be used when the user asks "what is
  an effort", "effort phases", "how do efforts work",
  "effort vs slice", or needs to understand the effort
  lifecycle. Covers the five phases: initialize, story
  capture, requirements, slice identification, and slice
  spawning.
---

# Effort Lifecycle

Overview of Forge effort lifecycle. Efforts are the **discovery
phase** — exploring problem spaces, gathering requirements, and
identifying slice candidates before delivery work begins.

## What is an Effort?

**Effort:** Discovery and exploration work for a problem space.
**Output:** Requirements, user stories, and identified slice
candidates.
**Duration:** Weeks to months (ongoing discovery).
**Location:** `.forge-context/efforts/YYYYMM-{slug}/`

**Example efforts:**
- Explore user authentication options
- Investigate cloud deployment strategies
- Research API versioning approaches

## Effort vs Slice

| Aspect | Effort | Slice |
|--------|--------|-------|
| **Purpose** | Discover + explore | Design + deliver |
| **Output** | Stories, requirements, candidates | Working software |
| **Timeline** | Ongoing (weeks/months) | Time-boxed (days/weeks) |
| **Scope** | Broad problem space | Focused deliverable |
| **State** | Living document | Complete when shipped |

**Flow:** Effort → identifies candidates → spawns Slices →
delivers features

## Effort Phases

### Phase 1: Initialize Effort

**Command:** `/explore init`

**Actions:**
- Create effort directory structure
- Write initial problem framing
- Set up README, effort.md, slices.md, decisions.md

**Output:**
- `.forge-context/efforts/YYYYMM-{slug}/` created
- effort.md with problem context
- slices.md (empty, ready for candidates)

### Phase 2: Story Capture

**Command:** `/explore stories`

**Actions:**
- Capture user stories from stakeholders
- Document user needs and pain points

**Format:**
```markdown
### ST-001: {Story Title}

**As a** {persona}
**I want** {capability}
**So that** {benefit}

**Acceptance Criteria:**
- {criterion 1}
- {criterion 2}
```

### Phase 3: Requirements Gathering

**Command:** `/explore requirements`

**Actions:**
- Extract requirements from stories
- Identify technical constraints
- Map affected components and area owners

**Format:**
```markdown
### REQ-001: {Requirement Title}

**Source:** ST-001, ST-003
**Priority:** High / Medium / Low
**Components:** {list}
```

### Phase 4: Slice Identification

**Command:** `/explore slices`

**Actions:**
- Group related stories/requirements
- Identify shippable increments
- Create slice candidates

**Format:**
```markdown
### SL-001: {Slice Title}

**Stories:** ST-001, ST-002
**Requirements:** REQ-001, REQ-003
**Scope:** {Brief description of deliverable}
**Status:** Candidate / Spawned / Complete
```

### Phase 5: Slice Spawning

**Command:** `/work new` (from slice candidate)

**Actions:**
- Create slice directory
- Copy requirements seed
- Initialize slice workflow

**Output:**
- `.forge-context/slices/YYYYMM-{slug}/` created
- Slice enters delivery lifecycle (see `slice-lifecycle` skill)

## Effort File Structure

```
.forge-context/efforts/YYYYMM-{slug}/
  effort.md               # Living discovery document
  slices.md               # Slice candidate tracking
  decisions.md            # ADRs for effort-level decisions
  checklist.md            # Health tracking
  artifacts/              # Supporting materials
    requirements-seed.md  # Initial requirements analysis
```

## When to Create an Effort

**Create effort when:**
- Problem space is large and unclear
- Multiple deliverables needed
- Discovery work required before design
- Customer research or validation needed

**Skip effort, go straight to slice when:**
- Problem is well-understood
- Single deliverable
- Clear requirements already exist
- Small enhancement to existing feature

## Effort Completion

**Effort completes when:**
- All identified slices are spawned or completed
- No more discovery work needed
- Problem space is exhausted

**Note:** Most efforts are **living documents** — discovery
continues as new needs arise. "Complete" is rare.

## Common Patterns

### Pattern 1: Customer-Driven Effort

1. Create customer/user profiles
2. Extract requirements from user needs
3. Identify user workflows
4. Create slice candidates per workflow

### Pattern 2: Technology Exploration Effort

1. Research current state (what exists?)
2. Identify gaps (what's missing?)
3. Capture user stories (what do users need?)
4. Create slice candidates (feature by feature)

### Pattern 3: Infrastructure Effort

1. Document problem (operational pain)
2. Research solutions (automation patterns)
3. Design architecture (high-level)
4. Create slice candidates (component by component)

## Integration with Forge Workflows

### Discovery → Delivery Flow

```
Effort (Discovery)
  ├─ Stories captured
  ├─ Requirements identified
  ├─ Slice candidates defined
  └─> Slice spawned (Delivery)
        ├─ Requirements refined
        ├─ Design created
        ├─ Implementation planned
        └─> Feature shipped
```

### Effort Commands

- `/explore init` — Initialize effort
- `/explore stories` — Capture user stories
- `/explore requirements` — Extract requirements
- `/explore slices` — Identify candidates
- `/explore review-pr` — Create PR for feedback

## Summary

| Phase | Command | Output |
|-------|---------|--------|
| **Initialize** | `/explore init` | effort.md |
| **Stories** | `/explore stories` | ST-NNN stories |
| **Requirements** | `/explore requirements` | REQ-NNN reqs |
| **Slices** | `/explore slices` | SL-NNN candidates |
| **Spawn** | `/work new` | Slice created |

**Key principles:**
- Discovery before delivery
- Living documents (evolve over time)
- Slice candidates (shippable increments)
- Parallel exploration (multiple efforts active)
