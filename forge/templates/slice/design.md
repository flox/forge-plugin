# Design: [SLICE_NAME]

_Run `/forge:design` to populate this document._

## Summary

[One paragraph overview of the technical approach]

## Requirements Reference

**Requirements document:** [Link to requirements.md]

### Key Constraints
- [Must-have behavior from requirements]
- [Performance or compatibility requirement]

## Architecture Overview

[High-level description of how this slice fits into
the system]

### Component Dependencies

| Component | Depends On | Type | Notes |
|-----------|-----------|------|-------|
| [Component A] | [Component B] | Runtime / Build | [Why] |

## Detailed Design

### Component: [Name]

**Current behavior:**
[What this component does today]

**New/modified behavior:**
[What changes with this slice]

**Key files:**
- `path/to/file` - [Purpose]

**Interface changes:**
```
// Example signature change
function newFunction(param: Type): Output
```

## Data Model

### New Data Structures

```
struct NewType {
    field: Type,
}
```

### Schema Changes

[If applicable, describe schema changes]

## API Changes

### New Endpoints/Commands

```
/new-command [options]
```

| Option | Required | Description |
|--------|----------|-------------|
| `--flag` | No | Description |

### Backward Compatibility

[How backward compatibility is maintained]

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [What this approach would involve]

**Pros:**
- [Advantage]

**Cons:**
- [Disadvantage]

**Why not chosen:** [Reason]

## Security Considerations

### Input Validation

[Validation approach for user-provided inputs]

### Data Sensitivity

[Sensitive data handling if applicable]

## Testing Strategy

### Unit Tests
- [What will be unit tested]

### Integration Tests
- [What integration scenarios will be tested]

### Manual Testing
- [Manual verification steps needed]

## Implementation Plan

### Task Breakdown

Use prefixed task IDs (T1, T2) for clear dependency
tracking.

| ID | Task | Estimate | Dependencies |
|----|------|----------|--------------|
| T1 | [Task] | S/M/L | None |
| T2 | [Task] | S/M/L | T1 |

### Suggested Order
1. [First task and why]
2. [Second task and why]

## Open Questions

1. [Technical question needing input]
2. [Unknown requiring investigation]
