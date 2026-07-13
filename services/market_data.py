"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

import yfinance as yf
from .common import success_response, error_response

def get_market_status():


    try:
        sp500 = yf.Ticker("^GSPC")
        nasdaq = yf.Ticker("^IXIC")
    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    return success_response(
        sp500 = sp500.fast_info["lastPrice"],
        nasdaq = nasdaq.fast_info["lastPrice"],
    )    