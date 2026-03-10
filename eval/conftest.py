"""Pytest fixtures for the Forge plugin evaluation harness.

Provides disposable repositories, plugin path resolution, and
async session runners for use across all test tiers.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Callable

import pytest


# ---------------------------------------------------------------------------
# Disposable repository fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def disposable_repo(tmp_path: Path) -> Path:
    """Create a temp directory with git init and sample project files.

    Copies the sample_project fixture files into the temp directory,
    initializes git, and returns the path. Cleaned up after the test.
    """
    sample_src = Path(__file__).parent / "fixtures" / "sample_project"

    # Copy sample project files to temp directory
    import shutil

    for item in sample_src.iterdir():
        dest = tmp_path / item.name
        if item.is_file():
            shutil.copy2(item, dest)
        else:
            shutil.copytree(item, dest)

    # Initialize git repository
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "eval@forge-plugin.test"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Forge Eval"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "add", "."],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial sample project"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    return tmp_path


# ---------------------------------------------------------------------------
# Plugin path fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def plugin_path() -> Path:
    """Return the absolute path to the forge plugin directory.

    This is the parent of the eval/ directory — the root of the
    forge-plugin repository checkout.
    """
    # eval/ is one level below the plugin root
    return Path(__file__).parent.parent.resolve()


# ---------------------------------------------------------------------------
# Session runner fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def run_session(plugin_path: Path) -> Callable:
    """Async function that runs a Claude Code session with scripted prompts.

    Returns a callable that accepts:
      - repo_path: Path to the disposable test repo
      - prompts: list[str] of scripted user messages to send
      - max_budget_usd: float (default per tier)
      - max_turns: int (default per tier)

    Returns the session result object with .messages and .trace attributes.

    Note: Requires ANTHROPIC_API_KEY to be set in the environment.
    The claude-agent-sdk API may evolve — verify SDK compatibility
    before running. See README.md for SDK version notes.
    """

    async def _run(
        repo_path: Path,
        prompts: list[str],
        max_budget_usd: float = 1.0,
        max_turns: int = 20,
    ) -> object:
        # Import here so tests that don't call run_session don't fail
        # if the SDK isn't installed.
        try:
            import anthropic  # type: ignore[import]
        except ImportError as e:
            raise ImportError(
                "claude-agent-sdk is required to run sessions. "
                "Install with: pip install claude-agent-sdk"
            ) from e

        # Build the system prompt pointing at the plugin
        plugin_manifest = plugin_path / "forge" / "commands"
        system_context = (
            f"You are Claude Code running in a project at {repo_path}. "
            f"The Forge plugin is installed from {plugin_path}. "
            "Follow all Forge workflow conventions."
        )

        # Use the claude-agent-sdk query() API
        # See: https://github.com/anthropics/claude-agent-sdk
        from anthropic.claude_agent_sdk import ClaudeAgentOptions, query  # type: ignore[import]

        options = ClaudeAgentOptions(
            max_budget_usd=max_budget_usd,
            max_turns=max_turns,
            system_prompt=system_context,
            working_directory=str(repo_path),
        )

        results = []
        for prompt in prompts:
            result = await query(prompt=prompt, options=options)
            results.append(result)

        # Return the last result (contains the full trace)
        return results[-1] if results else None

    return _run


# ---------------------------------------------------------------------------
# API key guard
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "requires_api: mark test as requiring ANTHROPIC_API_KEY",
    )


def pytest_collection_modifyitems(
    items: list[pytest.Item],
) -> None:
    """Skip API-dependent tests when ANTHROPIC_API_KEY is not set."""
    api_key_missing = not os.environ.get("ANTHROPIC_API_KEY")

    skip_no_key = pytest.mark.skip(reason="ANTHROPIC_API_KEY not set")

    for item in items:
        # All smoke, integration, and e2e tests require the API key
        has_tier_mark = any(
            item.get_closest_marker(m) for m in ("smoke", "integration", "e2e")
        )
        if has_tier_mark and api_key_missing:
            item.add_marker(skip_no_key)
