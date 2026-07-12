"""
StockMCP - A Model Context Protocol server for fetching stock information.

Run with:
    python server.py
"""

from mcp_instance import mcp

# Register tools
import tools.stock


if __name__ == "__main__":
    mcp.run()
