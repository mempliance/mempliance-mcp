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

## bznlabs-core — operational knowledge base

Any time you make a change to infrastructure, security, costs, CI/CD, architecture, or configuration in this repo, you MUST update the corresponding documentation in the **bznlabs-core** repository:
- Repo: https://github.com/mempliance/bznlabs-core
- Local path: /Users/sachinmalpe/VSCODE/Memory/bznlabs-core
- This product's docs live at: products/mempliance/

**What counts as a change requiring a doc update:**
- Any Terraform resource added, removed, or reconfigured → update infrastructure/ docs
- Any Cloud Armor rule change → update security/network.md
- Any new or rotated secret → update security/secrets.md
- Any CI/CD pipeline change → update ci-cd/pipeline.md
- Any cost-affecting resource change → update costs/breakdown.md
- Any architectural decision → add an ADR to decisions/adr/

Stale docs are worse than no docs. If you change it here, update it there.
