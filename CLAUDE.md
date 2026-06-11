# Mempliance MCP Server

Model Context Protocol server that wraps the Mempliance API for AI agents.
Provides tools: store_memory, recall_memory, forget_user.

## Auth
Set MEMPLIANCE_API_KEY=msk_live_xxx in environment. The MCP server passes this as Bearer token.

## Agent skills

### Issue tracker
Issues live in GitHub at github.com/mempliance/mempliance-mcp. See `docs/agents/issue-tracker.md`.

### Triage labels
Default five-label vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs
Single-context repo. See `docs/agents/domain.md`.
