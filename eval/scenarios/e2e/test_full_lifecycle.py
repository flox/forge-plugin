"""Tier 3 end-to-end tests: full Forge lifecycle.

Runs the complete workflow from init through implementation planning:
  init → explore → identify slice → work → requirements → design

Uses scripted responses for interactive prompts. Verifies that:
- All phases produce non-empty artifacts
- No Flox-specific references leak into output
- Document quality scores are above thresholds

Budget: $15, 150 turns max.
These tests are expensive. Run selectively with:
    pytest -m e2e

Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from scorers.document import score_requirements, score_design, score_effort


pytestmark = pytest.mark.e2e

# Scripted scenario for the full lifecycle
LIFECYCLE_SCENARIO = (
    "Build a REST API rate limiter for a Python FastAPI service. "
    "Limit by API key, support configurable thresholds per endpoint, "
    "return 429 with retry-after header, and expose metrics for monitoring."
)

EXPLORE_PROMPT = (
    "We need to add rate limiting to our FastAPI app. "
    "Explore the problem space and help us understand the right approach."
)

# Substrings that should NOT appear in Forge plugin output.
# These are Flox-internal references that were not properly generalized.
FLOX_SPECIFIC_PATTERNS = [
    r"\bFloxHub\b",
    r"\bfloxhub\b",
    r"\bZenHub\b",
    r"\bzenhub\b",
    r"flox/flox\b",
    r"\btao\.md\b",
    r"\.context/team/tao",
    r"forge-detect\.py",
    r"\.forge/scripts/",
    # TAO registry is Flox-internal
    r"\bTAO registry\b",
    r"\bArea Owner\b",
]

QUALITY_THRESHOLD = 75.0  # Slightly lower for E2E (longer chain = more variance)


# ---------------------------------------------------------------------------
# Full lifecycle test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_full_lifecycle_produces_artifacts(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Full lifecycle should produce non-empty artifacts at every phase.

    Verifies that each major phase creates its artifact file and that
    none of the files are empty.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_PROMPT}",
            f"/forge-work new {LIFECYCLE_SCENARIO}",
            "/forge-requirements",
            "/forge-design",
        ],
        max_budget_usd=15.0,
        max_turns=150,
    )

    forge_ctx = disposable_repo / ".forge-context"
    assert forge_ctx.exists(), ".forge-context directory was not created"

    # Check for effort artifact
    effort_files = list(forge_ctx.rglob("effort.md"))
    assert effort_files, "No effort.md produced during explore phase"
    assert all(f.stat().st_size > 100 for f in effort_files), (
        "effort.md is empty or trivially small"
    )

    # Check for requirements artifact
    req_files = list(forge_ctx.rglob("requirements.md"))
    assert req_files, "No requirements.md produced during requirements phase"
    assert all(f.stat().st_size > 100 for f in req_files), (
        "requirements.md is empty or trivially small"
    )

    # Check for design artifact
    design_files = list(forge_ctx.rglob("design.md"))
    assert design_files, "No design.md produced during design phase"
    assert all(f.stat().st_size > 100 for f in design_files), (
        "design.md is empty or trivially small"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_full_lifecycle_no_flox_references(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Full lifecycle output must not contain Flox-specific references.

    The Forge plugin is a generalized tool. Flox-internal concepts
    (FloxHub, ZenHub, TAO registry, etc.) must not leak into user-
    facing artifacts. This test checks all generated markdown files.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_PROMPT}",
            f"/forge-work new {LIFECYCLE_SCENARIO}",
            "/forge-requirements",
            "/forge-design",
        ],
        max_budget_usd=15.0,
        max_turns=150,
    )

    forge_ctx = disposable_repo / ".forge-context"
    violations: list[str] = []

    for md_file in forge_ctx.rglob("*.md"):
        content = md_file.read_text()
        for pattern in FLOX_SPECIFIC_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                violations.append(
                    f"{md_file.relative_to(disposable_repo)}: "
                    f"found '{matches[0]}' (pattern: {pattern})"
                )

    assert not violations, (
        "Flox-specific references found in plugin output:\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_full_lifecycle_quality_scores(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """All lifecycle artifacts should meet quality score thresholds.

    Scores effort.md, requirements.md, and design.md against their
    respective rubrics. All must score >= 75% in the full E2E run.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_PROMPT}",
            f"/forge-work new {LIFECYCLE_SCENARIO}",
            "/forge-requirements",
            "/forge-design",
        ],
        max_budget_usd=15.0,
        max_turns=150,
    )

    forge_ctx = disposable_repo / ".forge-context"
    failures: list[str] = []

    # Score effort.md
    effort_files = list(forge_ctx.rglob("effort.md"))
    if effort_files:
        score = score_effort(effort_files[0].read_text())
        if score.percentage < QUALITY_THRESHOLD:
            failures.append(
                f"effort.md: {score.percentage}% < {QUALITY_THRESHOLD}%\n{score}"
            )

    # Score requirements.md
    req_files = list(forge_ctx.rglob("requirements.md"))
    if req_files:
        score = score_requirements(req_files[0].read_text())
        if score.percentage < QUALITY_THRESHOLD:
            failures.append(
                f"requirements.md: {score.percentage}% < {QUALITY_THRESHOLD}%\n{score}"
            )

    # Score design.md
    design_files = list(forge_ctx.rglob("design.md"))
    if design_files:
        score = score_design(design_files[0].read_text())
        if score.percentage < QUALITY_THRESHOLD:
            failures.append(
                f"design.md: {score.percentage}% < {QUALITY_THRESHOLD}%\n{score}"
            )

    assert not failures, (
        "Quality score failures in full lifecycle:\n"
        + "\n".join(f"  - {f}" for f in failures)
    )
