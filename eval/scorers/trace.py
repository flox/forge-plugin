"""Tool call analysis utilities for session trace inspection.

Provides assertion helpers that inspect claude-agent-sdk session
traces to verify Forge commands triggered the expected skills,
agents, and file creation operations.

Usage:
    from scorers.trace import (
        assert_tool_called,
        assert_agent_spawned,
        assert_file_exists,
        assert_skill_triggered,
        extract_tool_calls,
    )
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ToolCall:
    """A single tool call extracted from a session trace."""

    name: str
    args: dict[str, Any]
    # Raw event from the trace, kept for debugging
    raw: dict[str, Any] = field(default_factory=dict, repr=False)


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------


def extract_tool_calls(trace: Any) -> list[ToolCall]:
    """Extract all tool calls from a session trace object.

    Handles both the claude-agent-sdk trace format and plain
    dicts/lists for testing without a live SDK.

    Args:
        trace: Session result or raw event list from claude-agent-sdk.

    Returns:
        List of ToolCall objects in invocation order.
    """
    calls: list[ToolCall] = []

    # Normalise to a list of events
    events: list[Any] = []
    if hasattr(trace, "events"):
        events = trace.events
    elif hasattr(trace, "messages"):
        events = trace.messages
    elif isinstance(trace, list):
        events = trace
    else:
        return calls

    for event in events:
        # Handle dict-style events (test fixtures)
        if isinstance(event, dict):
            if event.get("type") == "tool_use":
                calls.append(
                    ToolCall(
                        name=event.get("name", ""),
                        args=event.get("input", {}),
                        raw=event,
                    )
                )
            content = event.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        calls.append(
                            ToolCall(
                                name=block.get("name", ""),
                                args=block.get("input", {}),
                                raw=block,
                            )
                        )
        # Handle SDK message objects (AssistantMessage, etc.)
        elif hasattr(event, "content"):
            content = event.content
            if isinstance(content, list):
                for block in content:
                    if hasattr(block, "name") and hasattr(block, "input"):
                        calls.append(
                            ToolCall(
                                name=block.name,
                                args=block.input,
                            )
                        )
        # Handle bare ToolUseBlock objects
        elif hasattr(event, "name") and hasattr(event, "input"):
            calls.append(
                ToolCall(
                    name=event.name,
                    args=event.input,
                )
            )

    return calls


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------


def assert_tool_called(
    trace: Any,
    tool_name: str,
    args: dict[str, Any] | None = None,
) -> ToolCall:
    """Assert that a named tool was called, optionally matching args.

    Args:
        trace: Session trace from claude-agent-sdk.
        tool_name: Exact tool name to find (e.g. "Read", "Write", "Task").
        args: Optional dict of arg key→value pairs that must be present.
              Values are matched as substrings for string args.

    Returns:
        The matching ToolCall.

    Raises:
        AssertionError: If the tool was not called or args don't match.
    """
    calls = extract_tool_calls(trace)
    matching = [c for c in calls if c.name == tool_name]

    assert matching, (
        f"Tool '{tool_name}' was not called. "
        f"Tools called: {[c.name for c in calls]}"
    )

    if args is None:
        return matching[0]

    # Check each provided arg against the call args
    for call in matching:
        if _args_match(call.args, args):
            return call

    # No matching call found — produce a helpful error
    arg_strs = [f"{k}={v!r}" for k, v in args.items()]
    raise AssertionError(
        f"Tool '{tool_name}' was called {len(matching)} time(s) "
        f"but none matched args: {', '.join(arg_strs)}. "
        f"Actual args seen: {[c.args for c in matching]}"
    )


def assert_agent_spawned(trace: Any, agent_type: str) -> ToolCall:
    """Assert that a Task tool call was made with the given subagent_type.

    Args:
        trace: Session trace from claude-agent-sdk.
        agent_type: The subagent_type string (e.g. "implementation-worker").

    Returns:
        The matching Task ToolCall.

    Raises:
        AssertionError: If no matching Task call is found.
    """
    calls = extract_tool_calls(trace)
    task_calls = [c for c in calls if c.name == "Task"]

    assert task_calls, (
        f"No Task tool calls found. "
        f"Tools called: {[c.name for c in calls]}"
    )

    matching = [
        c
        for c in task_calls
        if c.args.get("subagent_type") == agent_type
    ]

    assert matching, (
        f"Task was called but not with subagent_type='{agent_type}'. "
        f"Subagent types used: "
        f"{[c.args.get('subagent_type') for c in task_calls]}"
    )

    return matching[0]


def assert_file_exists(trace: Any, path_pattern: str) -> ToolCall:
    """Assert that a Write or Edit call created a file matching a pattern.

    The pattern is matched as a substring (case-insensitive) against
    the file_path argument of Write and Edit calls.

    Args:
        trace: Session trace from claude-agent-sdk.
        path_pattern: Substring or glob-like fragment to match file paths.

    Returns:
        The matching Write/Edit ToolCall.

    Raises:
        AssertionError: If no matching file creation is found.
    """
    calls = extract_tool_calls(trace)
    write_calls = [c for c in calls if c.name in ("Write", "Edit")]

    assert write_calls, (
        f"No Write or Edit tool calls found. "
        f"Tools called: {[c.name for c in calls]}"
    )

    pattern_lower = path_pattern.lower()

    for call in write_calls:
        file_path: str = call.args.get("file_path", "")
        if pattern_lower in file_path.lower():
            return call

    paths = [c.args.get("file_path", "") for c in write_calls]
    raise AssertionError(
        f"No Write/Edit call matched path pattern '{path_pattern}'. "
        f"File paths seen: {paths}"
    )


def assert_skill_triggered(trace: Any, skill_name: str) -> ToolCall:
    """Assert that a Skill tool call was made with the given skill name.

    Skill tool calls reference skills by name (e.g. "forge-requirements",
    "tdd-discipline"). This assertion checks that the skill was loaded
    at least once during the session.

    Args:
        trace: Session trace from claude-agent-sdk.
        skill_name: Skill identifier (e.g. "forge-design").

    Returns:
        The matching Skill ToolCall.

    Raises:
        AssertionError: If the skill was not triggered.
    """
    calls = extract_tool_calls(trace)
    skill_calls = [c for c in calls if c.name == "Skill"]

    assert skill_calls, (
        f"No Skill tool calls found. "
        f"Tools called: {[c.name for c in calls]}"
    )

    matching = [
        c
        for c in skill_calls
        if c.args.get("skill") == skill_name
        or skill_name in str(c.args.get("skill", ""))
    ]

    assert matching, (
        f"Skill '{skill_name}' was not triggered. "
        f"Skills triggered: "
        f"{[c.args.get('skill') for c in skill_calls]}"
    )

    return matching[0]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _args_match(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    """Check that all expected key→value pairs are present in actual.

    String values are matched as substrings. Non-string values use
    equality.
    """
    for key, expected_value in expected.items():
        if key not in actual:
            return False
        actual_value = actual[key]
        if isinstance(expected_value, str) and isinstance(actual_value, str):
            if expected_value.lower() not in actual_value.lower():
                return False
        else:
            if actual_value != expected_value:
                return False
    return True
