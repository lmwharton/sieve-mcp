[![PyPI version](https://badge.fury.io/py/sieve-mcp.svg)](https://pypi.org/project/sieve-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

# Sieve MCP Server

AI-powered startup due diligence, delivered as an [MCP](https://modelcontextprotocol.io) server. Sieve scores startups across 7 IMPACT-X dimensions (Innovators, Market, Product, Advantage, Commerce, Traction, X-Factor) and recommends whether to take a meeting, pass, or request more information.

## Quick Start

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sieve": {
      "command": "uvx",
      "args": ["sieve-mcp"],
      "env": {
        "SIEVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add sieve -- uvx sieve-mcp
```

Then set your API key in the environment:

```bash
export SIEVE_API_KEY="your-api-key"
```

### Cursor / Windsurf

Add to your MCP settings:

```json
{
  "mcpServers": {
    "sieve": {
      "command": "uvx",
      "args": ["sieve-mcp"],
      "env": {
        "SIEVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIEVE_API_KEY` | Yes | — | Your Sieve API key. Get one at [sieve.arceusxventures.com/settings](https://sieve.arceusxventures.com/settings) |
| `SIEVE_API_URL` | No | `https://api.sieve.arceusxventures.com` | API base URL (override for self-hosted) |

## Available Tools

| Tool | Description | Read-only |
|------|-------------|-----------|
| `sieve_screen` | Run a Quick Screen on a startup | No |
| `sieve_status` | Check analysis progress | Yes |
| `sieve_summary` | Get full results of a completed analysis | Yes |
| `sieve_usage` | Check API usage for current billing period | Yes |

## Example Usage

A typical workflow in any MCP-compatible AI assistant:

1. **Screen a startup:**
   > "Run a Sieve screen on Acme Corp at acme.com"

2. **Poll for progress** (analysis takes 2-5 minutes):
   > "Check the status of that Sieve analysis"

3. **Get results:**
   > "Show me the Sieve summary for that analysis"

4. **Check usage:**
   > "How many Sieve screens do I have left this month?"

## Running with Docker

```bash
docker build -t sieve-mcp .
docker run -p 8080:8080 -e SIEVE_API_KEY=your-key sieve-mcp
```

## Development

```bash
# Install locally
pip install -e .

# Run in stdio mode (for MCP clients)
sieve-mcp

# Run in HTTP mode (for remote/container deployment)
sieve-mcp http
```

## License

MIT
