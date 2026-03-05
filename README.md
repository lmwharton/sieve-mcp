[![PyPI version](https://badge.fury.io/py/sieve-mcp.svg)](https://pypi.org/project/sieve-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

# Sieve MCP Server — AI-Powered Venture Capital Due Diligence

**The first MCP server purpose-built for venture capital.** Drop a company name into Claude, Cursor, or Windsurf and get a quantified investment memo in 5 minutes — not a ChatGPT summary, a real analyst-grade IMPACT-X assessment with every claim verified against evidence.

> **"Screen a startup called Acme Corp"** → Sieve researches the company, scores it across 7 dimensions, verifies every claim, and tells you: **Take the meeting** or **Pass**.

## Why Sieve?

Most VCs screen 50+ deals a month. Most of those are obvious passes — but you still spend 2-3 hours per deal on basic diligence before you know that. Sieve does that work in 5 minutes.

| What you get | How it works |
|---|---|
| **Sieve Score (0-140)** | Quantified score across 7 IMPACT-X dimensions — not a vibe check, a structured assessment |
| **Take Meeting / Pass / Need More Info** | Clear recommendation backed by evidence, not gut feel |
| **Evidence-typed findings** | Every finding tagged as Documented, Discovered, Inferred, or Missing — you know exactly what's verified |
| **Real-time deal chat** | Ask follow-up questions, challenge findings, explore scenarios |
| **Sector-aware analysis** | Adapts benchmarks for fintech, healthtech, deeptech, climate, SaaS, consumer |
| **Stage-calibrated** | Different expectations for pre-seed vs seed vs Series A |

### IMPACT-X Framework

| Dimension | What Sieve evaluates |
|---|---|
| **I** — Innovators | Founding team quality, experience, domain expertise |
| **M** — Market | Opportunity size, timing, tailwinds |
| **P** — Product | Solution strength, differentiation, technical depth |
| **A** — Advantage | Competitive moat, defensibility, switching costs |
| **C** — Commerce | Business model, unit economics, pricing power |
| **T** — Traction | Growth metrics, validation signals, customer evidence |
| **X** — X-Factor | Unique qualities, timing advantages, intangibles |

Each dimension scores 0-20. Total Sieve Score ranges from 0-140.

## Quick Start

### Install

```bash
pip install sieve-mcp
```

Or run directly without installing:

```bash
uvx sieve-mcp
```

### Get Your API Key

1. Sign up free at [app.sieve.arceusxventures.com](https://app.sieve.arceusxventures.com)
2. Go to **Settings** → copy your API key
3. Free tier: 2 screens/month. Pro: unlimited.

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

## Available Tools

| Tool | What it does | Read-only |
|---|---|---|
| `sieve_screen` | Start a Quick Screen — pass a company name, optional website URL, pitch deck text, or description | No |
| `sieve_status` | Poll analysis progress — see which dimensions are complete and current scores | Yes |
| `sieve_summary` | Get the full investment memo — Sieve Score, recommendation, strengths, concerns, evidence | Yes |
| `sieve_usage` | Check how many screens you've used this billing period | Yes |

## Example Workflow

Just talk to your AI assistant naturally:

**1. Screen a startup**
> "Run a Sieve screen on Acme Corp at acme.com"

**2. Check progress** (analysis takes 2-5 minutes)
> "What's the status of that Sieve analysis?"

**3. Get the investment memo**
> "Show me the full Sieve results"

**4. Dig deeper**
> "What are the key concerns? How strong is their competitive moat?"

**5. Check your usage**
> "How many Sieve screens do I have left this month?"

### Pro tip: Upload a pitch deck

For the most accurate analysis, paste pitch deck text or founder meeting notes:

> "Screen Acme Corp — here's their pitch deck text: [paste]. Also check acme.com"

Sieve cross-references pitch deck claims against discovered evidence, so you know what's real and what's aspirational.

## Who Uses Sieve

- **Solo GPs** screening 50+ deals/month — stop spending hours on obvious passes
- **Angel investors** evaluating startups outside their domain — Sieve brings sector expertise
- **Emerging fund managers** building a repeatable diligence process — consistent framework, every time
- **Accelerators** standardizing evaluation — compare apples to apples across your cohort

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SIEVE_API_KEY` | Yes | — | Your Sieve API key ([get one free](https://app.sieve.arceusxventures.com/settings)) |
| `SIEVE_API_URL` | No | `https://api.sieve.arceusxventures.com` | API base URL |

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

## Also Available As

Sieve isn't just an MCP server. Use it however fits your workflow:

- **Web App** — [app.sieve.arceusxventures.com](https://app.sieve.arceusxventures.com) — Full experience with real-time deal chat and document upload
- **REST API** — [api.sieve.arceusxventures.com/api/docs](https://api.sieve.arceusxventures.com/api/docs) — Integrate into custom deal flow pipelines
- **Android App** — Screen startups on the go

## Links

- **Website**: [sieve.arceusxventures.com](https://sieve.arceusxventures.com)
- **Web App**: [app.sieve.arceusxventures.com](https://app.sieve.arceusxventures.com)
- **API Docs**: [api.sieve.arceusxventures.com/api/docs](https://api.sieve.arceusxventures.com/api/docs)
- **PyPI**: [pypi.org/project/sieve-mcp](https://pypi.org/project/sieve-mcp/)
- **Contact**: [hello@arceusxventures.com](mailto:hello@arceusxventures.com)

## License

MIT

---

Built by [ArceusX Ventures](https://sieve.arceusxventures.com) — from VCs, for VCs.

<!-- mcp-name: io.github.lmwharton/sieve-mcp -->
