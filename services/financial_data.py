"""
Yahoo Finance service layer.

This module handles data retrieval from yfinance.
It does not contain MCP tools.
"""

from typing import Any

import pandas as pd
import yfinance as yf

from .common import success_response, error_response, clean_value

INCOME_STATEMENT_MAPPING: dict[str, str] = {
    "revenue": "Total Revenue",
    "expenses": "Total Expenses",
    "gross_profit": "Gross Profit",
    "operating_income": "Operating Income",
    "operating_expense": "Operating Expense",
    "net_income": "Net Income",
    "diluted_eps": "Diluted EPS",
    "basic_eps": "Basic EPS",
    "ebit": "EBIT",
    "ebitda": "EBITDA",
    "interest_expense": "Interest Expense",
    "gross_profit": "Gross Profit",    
}


BALANCE_SHEET_MAPPING: dict[str, str] = {
    "cash": "Cash And Cash Equivalents",
    "total_assets": "Total Assets",
    "current_assets": "Current Assets",
    "total_liabilities": "Total Liabilities Net Minority Interest",
    "current_liabilities": "Current Liabilities",
    "stockholders_equity": "Stockholders Equity",
    "total_debt": "Total Debt",
    "net_debt": "Net Debt",
    "working_capital": "Working Capital",
    "accumulated_depreciation": "Accumulated Depreciation",    
    "inventory": "Inventory",
}


CASH_FLOW_MAPPING: dict[str, str] = {
    "operating_cash_flow": "Operating Cash Flow",
    "investing_cash_flow": "Investing Cash Flow",
    "financing_cash_flow": "Financing Cash Flow",
    "free_cash_flow": "Free Cash Flow",
    "capital_expenditure": "Capital Expenditure",
    "net_income": "Net Income From Continuing Operations",
}


STATEMENT_MAPPING = {
    "income": {
        "annual": "income_stmt",
        "quarterly": "quarterly_income_stmt",
    },
    "balance": {
        "annual": "balance_sheet",
        "quarterly": "quarterly_balance_sheet",
    },
    "cash_flow": {
        "annual": "cash_flow",
        "quarterly": "quarterly_cash_flow",
    },
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
    except (KeyError, IndexError, AttributeError):
        return None


def get_financial_dataframe(
    ticker: yf.Ticker,
    statement: str,
    period: str,
) -> pd.DataFrame:
    attribute = STATEMENT_MAPPING[statement][period]
    return getattr(ticker, attribute)


def get_financial_data(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
    statement: str = "income",
    mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Return finacial data.
    """

    if mapping is None:
        return error_response(
            "INVALID_STATEMENT",
            "mapping is required"
        )

    if period not in ("annual", "quarterly"):
        return error_response(
            "INVALID_PERIOD",
            "period must be 'annual' or 'quarterly"
        )

    try:
        limit = int(limit)
    except (ValueError, TypeError):
        return error_response(
            "INVALID_PERIOD",
            "limit must be an integer"
        )

    limit = max(1, min(limit, 10))

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        df = get_financial_dataframe(ticker, statement, period)

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e)
        )

    if df.empty:      
        return error_response(
            "NO_DATA",
            "No financial data found"
        )

    # Keep the latest reports according to the limit parameter.
    df = df.sort_index(axis=1, ascending=False)
    df = df.iloc[:, :limit]

    financials = []

    for column in df.columns:
        report = {
            "date": column.strftime("%Y-%m-%d")
        }

        for key, row_name in mapping.items():
            report[key] = clean_value(get_dataframe_value(df, row_name, column))

        financials.append(report)

    return success_response(
        symbol = symbol,
        period = period,
        count = len(financials),
        financials = financials,
    ) 


def get_income_statement(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company income statement.
    """

    return  get_financial_data(symbol, period, limit, "income", INCOME_STATEMENT_MAPPING)


def get_balance_sheet(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company balance sheet.
    """

    return  get_financial_data(symbol, period, limit, "balance", BALANCE_SHEET_MAPPING)    


def get_cash_flow(
    symbol: str,
    period: str = "annual",
    limit: int = 4,
) -> dict[str, Any]:
    """
    Return company cash flow.
    """

    return  get_financial_data(symbol, period, limit, "cash_flow", CASH_FLOW_MAPPING) 