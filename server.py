"""
StockMCP - A Model Context Protocol server for fetching stock information.

Run with:
    python server.py
"""

from mcp_instance import mcp

# Register tools
import tools.stock
import tools.company
import tools.market
import tools.news
import tools.financials
import tools.forecast
import tools.option
import tools.screen_watchlist
import tools.compare_watchlist

if __name__ == "__main__":
    mcp.run()
