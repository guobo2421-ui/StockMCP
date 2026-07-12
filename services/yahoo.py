"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

import math
from typing import Any

import yfinance as yf


def get_stock_price(symbol: str) -> dict[str, Any]:
    """Return the latest stock price."""

    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")

    if history.empty:
        raise ValueError(f"No price data found for symbol: {symbol}")

    close_price = float(history["Close"].iloc[-1])

    return {
        "symbol": symbol.upper(),
        "price": close_price,
    }


def get_stock_history(
    symbol: str,
    period: str,
) -> list[dict[str, Any]]:
    """Return historical OHLCV data."""

    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period)

    if history.empty:
        raise ValueError(
            f"No historical data found for symbol: {symbol}"
        )

    records = []

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


def get_stock_info(symbol: str) -> dict[str, Any]:
    """Return company information."""

    ticker = yf.Ticker(symbol)
    info = ticker.info

    if not info:
        raise ValueError(
            f"No company information found for symbol: {symbol}"
        )

    fields = {
        "symbol": info.get("symbol", symbol.upper()),
        "name": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "current_price": (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
        ),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "dividend_yield": info.get("dividendYield"),
        "pe_ratio": info.get("trailingPE"),
        "website": info.get("website"),
        "summary": info.get("longBusinessSummary"),
    }

    cleaned = {}

    for key, value in fields.items():
        if value is None:
            continue

        if isinstance(value, float) and math.isnan(value):
            continue

        cleaned[key] = value

    return cleaned