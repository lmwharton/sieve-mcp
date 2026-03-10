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
        "It scores startups across 7 IMPACT-X dimensions (each 0-20, total 0-140) "
        "and returns a Take Meeting / Pass / Need More Info recommendation.\n\n"
        "WORKFLOW:\n"
        "1. Add documents: sieve_dataroom_add with company_name + file/text/url\n"
        "   - Creates the deal automatically on first add\n"
        "   - Add more documents with deal_id from the response\n"
        "2. Screen: sieve_screen with deal_id to analyze everything in the data room\n"
        "3. Poll: sieve_status every 15-30 seconds until complete\n"
        "4. Results: sieve_results for full diligence, sieve_memo for investment memo\n\n"
        "DISCOVERY:\n"
        "- sieve_deals to search/list deals in the pipeline\n"
        "- sieve_dataroom to see what's in a deal's data room\n"
        "- sieve_usage to check account and quota\n\n"
        "INTERPRETING RESULTS:\n"
        "- Sieve Score 100+: Exceptional, strong across most dimensions\n"
        "- Sieve Score 70-99: Promising, worth deeper investigation\n"
        "- Sieve Score below 70: Significant concerns in multiple areas\n"
        "- 'Take Meeting': Strong signals, recommend pursuing\n"
        "- 'Pass': Significant red flags identified\n"
        "- 'Need More Info': Evidence gaps — provide more context (pitch deck, description) and re-screen\n\n"
        "ERROR HANDLING:\n"
        "- If sieve_screen returns a rate limit error: call sieve_usage to check quota, "
        "suggest the user upgrade at https://app.sieve.arceusxventures.com/settings\n"
        "- If sieve_status returns 'failed': the analysis encountered an error, suggest re-screening\n"
        "- If sieve_results returns 404: analysis not yet complete, continue polling sieve_status\n\n"
        "IMPACT-X DIMENSIONS:\n"
        "I = Innovators (Team quality and experience)\n"
        "M = Market (Opportunity size and timing)\n"
        "P = Product (Solution strength and differentiation)\n"
        "A = Advantage (Competitive moat and defensibility)\n"
        "C = Commerce (Business model and unit economics)\n"
        "T = Traction (Growth metrics and validation)\n"
        "X = X-Factor (Unique qualities and intangibles)"
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
    company_name: str = "",
    deal_id: str = "",
    website_url: str = "",
    pitch_deck_text: str = "",
    description: str = "",
    confirm: bool = False,
) -> dict:
    """Run a Sieve IMPACT-X Quick Screen on a startup.

    Analyzes the company across 7 dimensions (Innovators, Market, Product,
    Advantage, Commerce, Traction, X-Factor) and returns an analysis ID.
    Takes 2-5 minutes to complete. Upserts -- if the company was previously
    screened, returns the existing deal (set confirm=true to re-screen).

    Two ways to use:
    - v3 (recommended): First add documents with sieve_dataroom_add, then
      call sieve_screen(deal_id=...) to analyze everything in the data room.
    - v2 (legacy): Call sieve_screen(company_name=..., website_url=...) directly.
      At least one of website_url or pitch_deck_text is required in this mode.

    Args:
        company_name: Name of the startup to screen (v2 flow, or to create new deal).
        deal_id: Screen an existing deal by ID (v3 flow -- use after sieve_dataroom_add).
        website_url: Company website URL (v2 flow).
        pitch_deck_text: Extracted pitch deck text (v2 flow).
        description: Brief company description (optional).
        confirm: Set to true to re-screen an existing deal.
    """
    return await client.screen(
        company_name=company_name,
        deal_id=deal_id,
        website_url=website_url,
        pitch_deck_text=pitch_deck_text,
        description=description,
        confirm=confirm,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_status(deal_id: str) -> dict:
    """Check the progress of a Sieve analysis.

    Returns which IMPACT-X dimensions are complete with their scores,
    overall progress percentage, and current phase.

    Args:
        deal_id: The deal ID returned by sieve_screen.
    """
    return await client.status(deal_id)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_results(deal_id: str, sections: str = "") -> dict:
    """Get the full results of a completed Sieve analysis.

    Returns the Sieve Score (0-140), meeting decision (Take Meeting/Pass/
    Need More Info), executive summary, key strengths, and key concerns.

    Args:
        deal_id: The deal ID returned by sieve_screen.
        sections: Comma-separated filter (e.g. 'summary,strengths,concerns').
                  Options: summary, profiles, findings, questions, strengths, concerns.
                  Empty returns everything. Score and decision are always included.
    """
    return await client.results(deal_id, sections=sections)


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_usage() -> dict:
    """Check your Sieve API usage for the current billing period.

    Shows screens used, monthly limit, tier, and organization name.
    """
    return await client.usage()


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_deals(search: str = "", limit: int = 20) -> dict:
    """List deals in your Sieve pipeline.

    Search by company name or list all deals. Returns deal metadata
    including Sieve scores for screened deals.

    Args:
        search: Search by company name (partial match). Empty returns all.
        limit: Maximum results to return (1-100, default 20).
    """
    return await client.deals(search=search, limit=limit)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_memo(deal_id: str, generate: bool = False, memo_type: str = "internal") -> dict:
    """Get or generate an investment memo for a deal.

    If generate=false (default), retrieves the existing memo.
    If generate=true, creates a new memo (~15-30 seconds).
    Requires a completed screen.

    Args:
        deal_id: The deal ID (from sieve_deals or sieve_screen).
        generate: Set to true to generate a new memo.
        memo_type: 'internal' (IC-facing, full risks) or 'external' (founder-facing). Default: internal.
    """
    return await client.memo(deal_id=deal_id, generate=generate, memo_type=memo_type)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_dataroom_add(
    title: str,
    company_name: str = "",
    deal_id: str = "",
    website_url: str = "",
    document_type: str = "other",
    file_path: str = "",
    text: str = "",
    url: str = "",
) -> dict:
    """Add a document to a deal's data room. Creates the deal if needed.

    This is the primary way to get documents into Sieve for screening.
    Upload a pitch deck, financials, or any document -- then call sieve_screen
    to analyze everything in the data room.

    Provide company_name to create a new deal (or find existing),
    or deal_id to add to an existing deal.

    Provide exactly one content source: file_path (local file),
    text (raw text/markdown), or url (fetch from URL).

    Args:
        title: Document title (e.g. "Pitch Deck Q1 2026").
        company_name: Company name -- creates deal if new, finds existing if not.
        deal_id: Add to an existing deal (from sieve_deals or previous sieve_dataroom_add).
        website_url: Company website URL (used when creating a new deal).
        document_type: Type: 'pitch_deck', 'financials', 'legal', or 'other'.
        file_path: Path to a local file (PDF, DOCX, XLSX). The tool reads and uploads it.
        text: Raw text or markdown content (alternative to file).
        url: URL to fetch document from (alternative to file).
    """
    return await client.dataroom_add(
        company_name=company_name,
        deal_id=deal_id,
        website_url=website_url,
        title=title,
        document_type=document_type,
        file_path=file_path,
        text=text,
        url=url,
    )


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
    }
)
async def sieve_dataroom(deal_id: str) -> dict:
    """List all documents in a deal's data room.

    Shows what files and content have been uploaded for a deal,
    along with their processing status.

    Args:
        deal_id: The deal ID (from sieve_deals or sieve_dataroom_add).
    """
    return await client.dataroom(deal_id)


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
