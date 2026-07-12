"""
StockMCP - A Model Context Protocol server for fetching stock prices.
Run with: python server.py
"""

# Standard library imports
import math
from typing import Annotated, Any

# Third-party imports
import yfinance as yf
#from fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server initialization
# Create a FastMCP server instance. The name is shown to MCP clients.
# ---------------------------------------------------------------------------
mcp = FastMCP("StockMCP")


# ---------------------------------------------------------------------------
# Tool definitions
# Expose Python functions as MCP tools using the @mcp.tool decorator.
# ---------------------------------------------------------------------------
@mcp.tool()
def stock_price(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
) -> float:
    """Return the latest closing price for the given stock symbol."""
    # Fetch recent price history for the ticker (last trading day).
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")

    if history.empty:
        raise ValueError(f"No price data found for symbol: {symbol}")

    # Return the most recent close price as a float.
    return float(history["Close"].iloc[-1])


@mcp.tool()
def stock_history(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
    period: Annotated[
        str,
        "Time range for historical data (e.g. 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
    ],
) -> list[dict[str, Any]]:
    """Return historical OHLCV price data for the given stock symbol."""
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period)

    if history.empty:
        raise ValueError(f"No historical data found for symbol: {symbol}")

    # Convert each trading day into a JSON-friendly record.
    records: list[dict[str, Any]] = []
    for date, row in history.iterrows():
        records.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
        )

    return records


@mcp.tool()
def stock_info(
    symbol: Annotated[str, "Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)"],
) -> dict[str, Any]:
    """Return key company information for the given stock symbol."""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    if not info:
        raise ValueError(f"No company information found for symbol: {symbol}")

    # Select commonly useful company fields from yfinance metadata.
    fields = {
        "symbol": info.get("symbol", symbol),
        "name": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "dividend_yield": info.get("dividendYield"),
        "pe_ratio": info.get("trailingPE"),
        "website": info.get("website"),
        "summary": info.get("longBusinessSummary"),
    }

    # Drop empty values and normalize floats for clean JSON output.
    cleaned: dict[str, Any] = {}
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, float) and math.isnan(value):
            continue
        cleaned[key] = value

    if not cleaned:
        raise ValueError(f"No company information found for symbol: {symbol}")

    return cleaned


# ---------------------------------------------------------------------------
# Entry point
# Start the MCP server when this file is executed directly.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
