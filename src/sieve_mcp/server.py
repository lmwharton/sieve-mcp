"""Sieve AI Due Diligence - MCP Server.

Exposes Sieve's startup screening API as MCP tools for
Claude, ChatGPT, Cursor, Windsurf, and other AI platforms.
"""

from fastmcp import FastMCP

from sieve_mcp import client

mcp = FastMCP(
    "Sieve AI Due Diligence",
    instructions=(
        "Sieve is an AI-powered startup due diligence platform. "
        "It scores startups across 7 IMPACT-X dimensions: "
        "Innovators (Team), Market, Product, Advantage, Commerce, Traction, X-Factor. "
        "Use sieve_screen to start an analysis, sieve_status to poll progress, "
        "and sieve_summary to get the final results once complete."
    ),
)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_screen(
    company_name: str,
    website_url: str = "",
    pitch_deck_text: str = "",
    description: str = "",
) -> dict:
    """Run a Sieve IMPACT-X Quick Screen on a startup.

    Analyzes the company across 7 dimensions (Innovators, Market, Product,
    Advantage, Commerce, Traction, X-Factor) and returns an analysis ID.
    Takes 2-5 minutes to complete.

    Args:
        company_name: Name of the startup to screen.
        website_url: Company website URL (optional, improves accuracy).
        pitch_deck_text: Extracted pitch deck text (optional, improves accuracy).
        description: Brief company description (optional).
    """
    return await client.screen(
        company_name=company_name,
        website_url=website_url,
        pitch_deck_text=pitch_deck_text,
        description=description,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_status(analysis_id: str) -> dict:
    """Check the progress of a Sieve analysis.

    Returns which IMPACT-X dimensions are complete with their scores,
    overall progress percentage, and current phase.

    Args:
        analysis_id: The analysis ID returned by sieve_screen.
    """
    return await client.status(analysis_id)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_summary(analysis_id: str) -> dict:
    """Get the full results of a completed Sieve analysis.

    Returns the Sieve Score (0-140), meeting decision (Take Meeting/Pass/
    Need More Info), executive summary, key strengths, and key concerns.

    Args:
        analysis_id: The analysis ID returned by sieve_screen.
    """
    return await client.summary(analysis_id)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_usage() -> dict:
    """Check your Sieve API usage for the current billing period.

    Shows screens used, monthly limit, and tier.
    """
    return await client.usage()


def main():
    """Entry point — supports stdio (default) and HTTP transports."""
    import sys

    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport == "http":
        import os

        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)),
        )
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
