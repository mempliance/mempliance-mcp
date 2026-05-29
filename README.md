# mempliance-mcp

MCP server for [Mempliance](https://mempliance.ai) — adds persistent, GDPR-compliant user memory to any MCP-compatible AI agent.

```bash
pip install mempliance-mcp
# or run without installing:
uvx mempliance-mcp
```

## What it does

Exposes five MCP tools that wrap the Mempliance HTTP API:

| Tool | Description |
|---|---|
| `mempliance_store` | Store a fact about an end user after a meaningful exchange |
| `mempliance_recall` | Retrieve relevant memories before generating a response |
| `mempliance_forget` | Erase all memories for an end user (GDPR right to erasure) |
| `mempliance_estimate` | Estimate MemOp cost before storing |
| `mempliance_get_trace` | Inspect the full pipeline decision log for a store call |

## Quick setup

Get an API key at [mempliance.ai](https://mempliance.ai) (free 14-day trial), then add the server to your agent config.

---

## Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "mempliance": {
      "command": "uvx",
      "args": ["mempliance-mcp"],
      "env": {
        "MEMPLIANCE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Code. The five tools are now available in every session.

**Suggested CLAUDE.md addition** (project or global):

```markdown
## Memory

You have access to persistent user memory via Mempliance MCP tools.

- Call `mempliance_recall` with the user's ID and a relevant query before every response.
- Call `mempliance_store` after any turn where the user reveals a preference, tool, decision,
  or factual detail about themselves.
- Never store greetings, questions, or filler. Only concrete user facts.
- The `end_user_id` must be a stable opaque identifier — never an email address.
```

---

## Cline (VS Code)

In VS Code, open the Cline extension settings and add under **MCP Servers**:

```json
{
  "mempliance": {
    "command": "uvx",
    "args": ["mempliance-mcp"],
    "env": {
      "MEMPLIANCE_API_KEY": "your-api-key-here"
    }
  }
}
```

Or edit `~/.cline/settings.json` directly with the same block.

---

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mempliance": {
      "command": "uvx",
      "args": ["mempliance-mcp"],
      "env": {
        "MEMPLIANCE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Desktop to load the new server.

---

## Goose (Block)

Add to your Goose profile (`~/.config/goose/profiles.yaml`):

```yaml
extensions:
  mempliance:
    name: mempliance
    type: stdio
    cmd: uvx
    args:
      - mempliance-mcp
    env:
      MEMPLIANCE_API_KEY: your-api-key-here
    enabled: true
```

Run `goose session start` — the Mempliance tools load automatically.

---

## How agents should use the tools

### Pattern: recall before respond, store after

```
User message arrives
  → mempliance_recall(end_user_id, query=<relevant topic>)
  → inject system_block into context
  → generate response
  → if user revealed new information:
      mempliance_store(end_user_id, text=<the relevant message>)
```

### Store selectively

Only store messages with concrete user information:

```
Store:   "I prefer TypeScript over JavaScript for all new projects."
Store:   "I'm building a customer support bot for a SaaS company."
Skip:    "Can you help me with something?"
Skip:    "Thanks!"
```

### end_user_id

The `end_user_id` must be a stable, opaque identifier — a UUID or your internal user ID. Never use an email address or phone number. This value persists in audit logs even after erasure.

For single-user local agents, a fixed string like `"local-user"` works fine.

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `MEMPLIANCE_API_KEY` | Yes | — | Your Mempliance API key |
| `MEMPLIANCE_BASE_URL` | No | `https://api.mempliance.ai` | Override for self-testing |
| `MEMPLIANCE_TIMEOUT` | No | `15` | HTTP timeout in seconds |

---

## License

MIT
