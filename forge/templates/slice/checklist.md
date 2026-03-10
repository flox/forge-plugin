# Slice Checklist: [SLICE_NAME]

Track items requiring human judgment. Phase completion
is derived from review artifacts, not checkbox state.

---

## Phase 1: Requirements

### Human Judgment Items

- [ ] **Open questions resolved** (or deferred with
      documented reason)
- [ ] Approach section included (if scope is non-trivial)

### Guidance (not checkboxes)

Requirements document should include: summary, user
stories with acceptance criteria, success criteria,
scope boundaries, affected components.

**Phase complete when:**
`reviews/requirements-review.md` exists.

---

## Phase 2: Design (Conditional)

_Skip for engineer handoffs with clear approach in
requirements._

### Human Judgment Items

- [ ] **Open questions resolved** (or deferred with
      documented reason)
- [ ] Complexity acceptable (tasks <= 10)

### Guidance (not checkboxes)

Design document should include: architecture overview,
component changes, API changes, alternatives considered,
testing strategy, task breakdown.

**Phase complete when:**
`reviews/design-review.md` exists.

---

## Phase 3: Implementation

### Human Judgment Items

- [ ] End-to-end verification done
- [ ] Context docs reviewed for updates

### Guidance (not checkboxes)

Track tasks in `tasks.md`. Implementation PRs go to
target repos.

**Phase complete when:** All tasks done.

---

## Slice Complete

**Complete when:** All phases done.
