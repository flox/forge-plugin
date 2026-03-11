# Slices: [EFFORT_NAME]

Slices of work identified from this effort. Candidates
are reviewed, then spawned as slices in
`.forge-context/slices/YYYYMM-{slug}/`.

---

## Summary

| Status | Count |
|--------|-------|
| Pending Review | 0 |
| Accepted | 0 |
| Spawned | 0 |
| Completed | 0 |
| **Total** | **0** |

---

## Pending Review

_Candidates under review. Once approved, move to
Accepted. From there, spawn via `/forge:work`._

### SL-001: [Slice Name]

**Status:** `draft` | `under-review`

**Summary:** [One-line description of this deliverable]

**Stories:** ST-001, ST-003

**Acceptance Criteria:**
- [ ] [Criterion]
- [ ] [Criterion]

**Approach:** [1-2 sentences on how this will be solved]

**Blockers:** None | [List blockers]

**Estimated Scope:** `Small` | `Medium` | `Large`
**Priority:** `High` | `Medium` | `Low`
**Depends on:** None | SL-NNN

---

## Accepted (Ready to Spawn)

_Reviewed and approved, ready to spawn via
`/forge:work new`._

<!--
### SL-NNN: [Slice Name]

**Status:** `accepted`

**Summary:** [One-line description]

**Stories:** ST-NNN, ST-NNN

**Acceptance Criteria:**
- [ ] [Criterion]

**Approach:** [How this will be solved]

**Estimated Scope:** `Medium`
**Priority:** `Medium`
**Depends on:** None
-->

---

## Direct Issues

_Items addressed directly without formal slices._

| Issue | Items | Status | Notes |
|-------|-------|--------|-------|
| [#NNN](link) | ST-003 | Closed | Quick fix |

**When to use direct issues:**
- Bug fixes, patches, quick enhancements
- Small, well-understood work (< 2 days)
- No requirements/design phase needed

---

## Spawned

_Slices created from this effort._

| ID | Slice | Spawned | Status | Items | Link |
|----|-------|---------|--------|-------|------|
| SL-002 | [Slice Name] | YYYY-MM-DD | In Progress | ST-002 | [link](..) |

---

## Slice Lifecycle

| Status | What Happens |
|--------|--------------|
| **Draft** | Candidate identified, preparing for review |
| **Under Review** | Being reviewed |
| **Accepted** | Approved, ready to spawn |
| **Spawned** | Slice directory created, work begins |
| **In Progress** | Design/implementation underway |
| **Completed** | Slice shipped |

---

<!--
SLICE TEMPLATE - Copy to Pending Review section:

### SL-NNN: [Slice Name]

**Status:** `draft`

**Summary:** [One-line description]

**Stories:** ST-NNN, ST-NNN

**Acceptance Criteria:**
- [ ] [Criterion]
- [ ] [Criterion]

**Approach:** [How this will be solved]

**Blockers:** None

**Estimated Scope:** `Medium`
**Priority:** `Medium`
**Depends on:** None

---
-->
