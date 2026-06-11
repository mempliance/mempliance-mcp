# Domain Documentation

Repository: https://github.com/mempliance/mempliance-mcp

## Overview

This is a single-context MCP server repository. It exposes the Mempliance API
as Model Context Protocol tools so that AI agents can persist and retrieve
per-user memories across sessions.

## Exposed MCP tools

| Tool | Description |
|------|-------------|
| `store_memory` | Persist a memory string for a given user_id |
| `recall_memory` | Retrieve relevant memories for a given user_id and query |
| `forget_user` | Delete all stored memories for a given user_id |

## Authentication

The server reads `MEMPLIANCE_API_KEY` from the environment and forwards it as a
`Bearer` token on every request to the Mempliance API.

## Key constraints

- One tenant per API key. The key encodes the tenant; the server does not accept
  a tenant_id parameter.
- `user_id` values are opaque strings chosen by the caller. Use stable
  identifiers (e.g. Clerk user IDs) so memories survive session restarts.
