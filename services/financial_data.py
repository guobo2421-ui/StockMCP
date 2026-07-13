"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

from typing import Any

import pandas as pd
import yfinance as yf

from .common import success_response, error_response, clean_value

FIELD_MAPPING: dict[str, str] = {
    "revenue": "Total Revenue",
    "gross_profit": "Gross Profit",
    "operating_income": "Operating Income",
    "net_income": "Net Income",
    "diluted_eps": "Diluted EPS",
    "ebit": "EBIT",
    "ebitda": "EBITDA",
    "interest_expense": "Interest Expense",
}

def get_financial_value(
    df: pd.DataFrame,
    row_name: str,
    column: Any
) -> Any:
    """
    Safely retrieve a value from a financial statement.
    """

    try:
        value = df.loc[row_name, column]

        if pd.isna(value):
            return None

        if hasattr(value, "item"):
            return value.item()

        return value

    except (KeyError, IndexError, AttributeError):
        return None


def get_dataframe_value(
    df: pd.DataFrame,
    row_name: str,
    column: Any,
) -> Any:
    try:
        return df.loc[row_name, column]
    except (KeyError, IndexError):
        return None


def get_income_statement(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company income statement.
    """
    if period not in ("annual", "quarterly"):
        return error_response(
            "NO_DATA",
            "period must be 'annual' or 'quarterly"
        )

    try:
        limit = int(limit)
    except (ValueError, TypeError):
        return error_response(
            "NO_DATA",
            "limit must be an integer"
        )

    limit = max(1, min(limit, 10))

    if not symbol:
        return error_response(
            "NO_DATA",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)

        if period == "quarterly":
            df = ticker.quarterly_income_stmt
        else:
            df = ticker.income_stmt

    except Exception as e:
        return error_response(
            "NO_DATA",
            str(e)
        )

    if df.empty:      
        return error_response(
            "NO_DATA",
            "No income statement found"
        )

    # Keep the latest reports according to the limit parameter.
    df = df.sort_index(axis=1, ascending=False)
    df = df.iloc[:, :limit]

    financials = []

    for column in df.columns:
        statement = {
            "date": column.strftime("%Y-%m-%d")
        }

        for key, row_name in FIELD_MAPPING.items():
            statement[key] = clean_value(get_dataframe_value(df, row_name, column))
            #statement[key] = get_financial_value(df, row_name, column)

        financials.append(statement)

    return success_response(
        symbol = symbol,
        period = period,
        count = len(financials),
        financials = financials,
    )        