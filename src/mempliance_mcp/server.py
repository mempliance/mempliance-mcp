"""Mempliance MCP server.

Exposes store / recall / forget / estimate as MCP tools so any MCP-compatible
agent (Claude Code, Cline, Goose, Claude Desktop) gets persistent user memory
with zero custom integration code.

Usage:
    MEMPLIANCE_API_KEY=sk-... uvx mempliance-mcp

Environment variables:
    MEMPLIANCE_API_KEY   Required. Your Mempliance API key.
    MEMPLIANCE_BASE_URL  Optional. Defaults to https://api.mempliance.ai.
    MEMPLIANCE_TIMEOUT   Optional. HTTP timeout in seconds. Defaults to 15.
"""
import os
import math

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Mempliance Memory",
    instructions=(
        "You have access to a persistent memory layer via Mempliance. "
        "Call mempliance_recall at the start of every conversation turn to load relevant context. "
        "Call mempliance_store after any turn where the user reveals a preference, decision, "
        "or factual statement about themselves. "
        "Never store questions, greetings, or filler text. "
        "Use the end_user_id consistently — it must be an opaque identifier (UUID or internal ID), "
        "never an email address or phone number."
    ),
)

_API_KEY = os.environ.get("MEMPLIANCE_API_KEY", "")
_BASE_URL = os.environ.get("MEMPLIANCE_BASE_URL", "https://api.mempliance.ai").rstrip("/")
_TIMEOUT = float(os.environ.get("MEMPLIANCE_TIMEOUT", "15"))


def _client() -> httpx.Client:
    if not _API_KEY:
        raise RuntimeError(
            "MEMPLIANCE_API_KEY environment variable is not set. "
            "Set it in your MCP server configuration."
        )
    return httpx.Client(
        base_url=_BASE_URL,
        headers={"Authorization": f"Bearer {_API_KEY}", "Content-Type": "application/json"},
        timeout=_TIMEOUT,
    )


@mcp.tool()
def mempliance_store(end_user_id: str, text: str) -> dict:
    """Store a fact about an end user.

    Call this after every turn where the user reveals a preference, decision,
    tool they use, or any factual statement about themselves or their context.

    The raw text is PII-scrubbed and then processed by an LLM which extracts a
    structured Fact before storage. Duplicate or contradictory facts are
    resolved automatically by the state machine (REINFORCE / MERGE / SUPERSEDE).

    Returns a trace_id you can use with mempliance_get_trace to inspect exactly
    what the pipeline decided to do with the input.
    """
    with _client() as c:
        r = c.post("/store", json={"end_user_id": end_user_id, "text": text})
        r.raise_for_status()
        return r.json()


@mcp.tool()
def mempliance_recall(end_user_id: str, query: str = "", limit: int = 10) -> dict:
    """Recall relevant memories for an end user.

    Call this at the start of every conversation turn to load context about the
    user before generating a response. The returned system_block is formatted
    Markdown ready to prepend to your system prompt.

    Args:
        end_user_id: Opaque identifier for the end user (UUID or internal ID).
        query: Semantic search query. Describes what context you need right now.
               If empty, returns the most recently reinforced memories.
        limit: Maximum number of memories to return (1–100, default 10).
    """
    payload: dict = {"end_user_id": end_user_id, "limit": limit}
    if query:
        payload["query"] = query
    with _client() as c:
        r = c.post("/recall", json=payload)
        r.raise_for_status()
        data = r.json()
    return {
        "system_block": data.get("system_block", ""),
        "memories": data.get("memories", []),
        "total": data.get("total", 0),
        "meta": data.get("meta", {}),
        "roi_audit": data.get("roi_audit", {}),
    }


@mcp.tool()
def mempliance_forget(end_user_id: str) -> dict:
    """Erase all memories for an end user (GDPR right to erasure).

    Immediately and permanently deletes all active memories. An immutable
    ERASED audit event is retained for compliance. There is no undo.

    Call this when a user requests data deletion or when your data retention
    policy requires it.
    """
    with _client() as c:
        r = c.post("/forget", json={"end_user_id": end_user_id})
        r.raise_for_status()
        return r.json()


@mcp.tool()
def mempliance_estimate(text: str) -> dict:
    """Estimate the MemOp cost for a piece of text before storing.

    Does not require authentication and does not store anything.
    Use this to check cost before calling mempliance_store on large inputs.

    Returns characters (exact count) and units_estimated (ceil(chars / 5000)).
    """
    chars = len(text)
    units = max(1, math.ceil(chars / 5000))
    return {"characters": chars, "units_estimated": units}


@mcp.tool()
def mempliance_get_trace(trace_id: str) -> dict:
    """Inspect the full pipeline decision log for a store operation.

    Returns every decision the pipeline made: signal gate result, PII entities
    found, LLM extraction output, and state machine action
    (INSERT / REINFORCE / MERGE / SUPERSEDE).

    Traces are retained for 90 days. Use the trace_id from mempliance_store.
    """
    with _client() as c:
        r = c.get(f"/trace/{trace_id}")
        r.raise_for_status()
        return r.json()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
