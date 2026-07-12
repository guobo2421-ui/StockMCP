"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

import yfinance as yf

def get_market_status():

    sp500 = yf.Ticker("^GSPC")
    nasdaq = yf.Ticker("^IXIC")

    return {
        "sp500": sp500.fast_info["lastPrice"],
        "nasdaq": nasdaq.fast_info["lastPrice"],
    }