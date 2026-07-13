"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

import math
from typing import Any

import yfinance as yf
from datetime import datetime
from .common import success_response, error_response, clean_value

def get_stock_price(symbol: str) -> dict[str, Any]:
    """Return the latest stock price."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d")

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    if df.empty:      
        return error_response(
            "NO_DATA",
            "No price data found"
        )

    close_price = float(df["Close"].iloc[-1])

    return success_response(
        symbol = symbol,
        price = close_price,
    )


def get_stock_history(
    symbol: str,
    period: str,
) -> list[dict[str, Any]]:
    """Return historical OHLCV data."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    if df.empty:      
        return error_response(
            "NO_DATA",
            "No historical data found"
        )

    records = []

    for date, row in df.iterrows():
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


def get_company_info(symbol: str) -> dict[str, Any]:
    """Return company information."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    if not info:      
        return error_response(
            "NO_DATA",
            "No company information found"
        )

    fields = {
        "symbol": info.get("symbol", symbol),
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
        value = clean_value(value)

        if value is not None:
            cleaned[key] = value

    return success_response(**cleaned)


def get_stock_news(symbol: str) -> dict[str, Any]:
    """Return the latest news articles for the given stock symbol."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news[:10]

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    if not news:      
        return error_response(
            "NO_DATA",
            "No historical data found"
        )

    articles = []

    for item in news:
        content = item.get("content", {})

        if not content.get("title"):
            continue

        articles.append(
            {
                "title": content.get("title"),
                "summary": content.get("summary"),
                "publisher": content.get("provider", {}).get("displayName"),
                "published": content.get("pubDate"),
                "url": content.get("canonicalUrl", {}).get("url"),
            }
        )

    return success_response(
        symbol = symbol,
        count = len(articles),
        news = articles,
    ) 