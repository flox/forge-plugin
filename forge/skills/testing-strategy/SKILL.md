---
name: testing-strategy
description: >-
  This skill should be used when "planning tests",
  "testing strategy", "what tests do we need", or
  designing the testing section of a design document.
  Covers unit, integration, E2E, and performance testing
  levels. Do not use for writing actual test code
  (see tdd-discipline).
---

# Testing Strategy Pattern

Standard approach for planning tests across different levels.

## Test Levels

### Unit Tests

Questions to ask:
- What new modules/functions need unit tests?
- What existing tests need updates?
- Are there edge cases or error conditions to cover?

**Include in design:**
```markdown
### Unit Tests
- [New modules/functions needing tests]
- [Existing tests needing updates]
```

### Integration Tests (Per-Component)

Questions to ask:
- What component interactions need testing?
- Database or API integration tests needed?
- Are there service boundaries being crossed?

**Include in design:**
```markdown
### Integration Tests
- [Component interactions to verify]
```

### End-to-End Tests

Questions to ask:
- Does this feature add new user flows?
- Will it need new scenarios in the E2E test suite?

**Include in design:**
```markdown
### E2E Tests
- **Needs update:** Yes / No
- [New scenarios if applicable]
```

## API Compatibility

For features affecting API contracts:

| Question | Why It Matters |
|----------|---------------|
| Could this break existing clients? | Users may not update immediately |
| Is versioning needed? | Backward compatibility |
| What's the deprecation path? | How to phase out old behavior |

**Include in design:**
```markdown
### API Compatibility
- **Existing clients work:** Yes / No
- **Versioning needed:** Yes / No
- [Deprecation path if applicable]
```

## Performance Tests

For performance-sensitive features:

- Any performance-sensitive paths?
- Benchmarks to add or update?
- Are there latency or throughput requirements?

## Web UI Testing (if applicable)

For UI changes:

### Viewport Testing
- Test at common breakpoints: mobile, tablet, desktop
- Verify layout doesn't break at edge breakpoints
- Check that features work or are intentionally hidden across
  all sizes

### Authentication State Testing
- Test as authenticated user
- Test as unauthenticated user
- Verify feature visibility/behavior is consistent for each
  auth state

**Include in design:**
```markdown
### Web UI Testing
- **Affects authenticated users:** Yes / No
- **Affects unauthenticated users:** Yes / No
- **Responsive behavior:** Consistent / Intentionally different
- **Breakpoints tested:** Mobile / Tablet / Desktop
```

---

## Design-Integrated Testing

When a design includes Key Decisions (ADRs), each decision
should map to at least one test that validates correct
implementation:

| Decision | Test | Expected Outcome |
|----------|------|-----------------|
| {decision title} | {specific test} | {pass criteria} |

This ensures design decisions are not just documented but
verified during implementation. The implementation worker
should check this table when writing tests.

## Test Planning Template

```markdown
## Testing Strategy

### Unit Tests
- [New modules/functions needing tests]
- [Existing tests needing updates]

### Integration Tests
- [Component interactions to verify]

### E2E Tests
- **Needs update:** Yes / No
- [New scenarios if applicable]

### API Compatibility
- **Existing clients work:** Yes / No
- **Versioning needed:** Yes / No
- [Deprecation path if applicable]

### Web UI Testing (if applicable)
- **Affects authenticated users:** Yes / No
- **Affects unauthenticated users:** Yes / No
- **Responsive behavior:** Consistent / Intentionally different
- **Breakpoints tested:** Mobile / Tablet / Desktop

### Performance Tests
- [If applicable]
```
