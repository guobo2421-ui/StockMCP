"""
Yahoo Finance options service layer.

This module handles options data retrieval from yfinance.
It does not contain MCP tools.
"""

from datetime import date
from typing import Any

import yfinance as yf

from .common import success_response, error_response, clean_value


def get_option_expirations(symbol: str) -> dict[str, Any]:
    """Return available option expiration dates."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required",
        )

    symbol = symbol.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        expirations = ticker.options

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e),
        )

    if not expirations:
        return error_response(
            "NO_DATA",
            "No option expiration dates found",
        )

    return success_response(
        symbol=symbol,
        expiration_dates=list(expirations),
        count=len(expirations),
    )


def get_option_chain(
    symbol: str,
    expiration: str,
) -> dict[str, Any]:
    """Return call and put option chains for an expiration date."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required",
        )

    if not expiration:
        return error_response(
            "MISSING_EXPIRATION",
            "expiration is required",
        )

    symbol = symbol.strip().upper()
    expiration = expiration.strip()

    try:
        ticker = yf.Ticker(symbol)

        if expiration not in ticker.options:
            return error_response(
                "INVALID_EXPIRATION",
                f"Expiration date is not available: {expiration}",
            )

        option_chain = ticker.option_chain(expiration)

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e),
        )

    def convert_options(df) -> list[dict[str, Any]]:
        options = []

        for _, row in df.iterrows():
            options.append(
                {
                    "contract_symbol": clean_value(row["contractSymbol"]),
                    "last_trade_date": clean_value(row["lastTradeDate"]),
                    "strike": clean_value(row["strike"]),
                    "last_price": clean_value(row["lastPrice"]),
                    "bid": clean_value(row["bid"]),
                    "ask": clean_value(row["ask"]),
                    "change": clean_value(row["change"]),
                    "percent_change": clean_value(row["percentChange"]),
                    "volume": clean_value(row["volume"]),
                    "open_interest": clean_value(row["openInterest"]),
                    "implied_volatility": clean_value(
                        row["impliedVolatility"]
                    ),
                    "in_the_money": clean_value(row["inTheMoney"]),
                    "contract_size": clean_value(row["contractSize"]),
                    "currency": clean_value(row["currency"]),
                }
            )

        return options

    calls = convert_options(option_chain.calls)
    puts = convert_options(option_chain.puts)

    return success_response(
        symbol=symbol,
        expiration=expiration,
        calls=calls,
        puts=puts,
        call_count=len(calls),
        put_count=len(puts),
    )

def get_option_summary(
    symbol: str,
    expiration: str,
) -> dict[str, Any]:
    """Return a Claude-friendly summary of an option chain."""

    if not symbol:
        return error_response(
            "MISSING_SYMBOL",
            "symbol is required",
        )

    if not expiration:
        return error_response(
            "MISSING_EXPIRATION",
            "expiration is required",
        )

    symbol = symbol.strip().upper()
    expiration = expiration.strip()

    try:
        ticker = yf.Ticker(symbol)

        if expiration not in ticker.options:
            return error_response(
                "INVALID_EXPIRATION",
                f"Expiration date is not available: {expiration}",
            )

        underlying_price = clean_value(
            ticker.fast_info.get("lastPrice")
        )

        if underlying_price is None:
            return error_response(
                "NO_DATA",
                "Unable to retrieve underlying stock price",
            )

        option_chain = ticker.option_chain(expiration)

    except Exception as e:
        return error_response(
            "API_ERROR",
            str(e),
        )

    calls = option_chain.calls
    puts = option_chain.puts

    expiration_date = date.fromisoformat(expiration)
    days_to_expiration = (
        expiration_date - date.today()
    ).days

    def convert_option(row) -> dict[str, Any]:
        strike = clean_value(row["strike"])

        return {
            "contract_symbol": clean_value(row["contractSymbol"]),
            "strike": strike,
            "last_price": clean_value(row["lastPrice"]),
            "bid": clean_value(row["bid"]),
            "ask": clean_value(row["ask"]),
            "volume": clean_value(row["volume"]),
            "open_interest": clean_value(row["openInterest"]),
            "implied_volatility": clean_value(
                row["impliedVolatility"]
            ),
            "in_the_money": clean_value(row["inTheMoney"]),
        }

    call_options = [
        convert_option(row)
        for _, row in calls.iterrows()
    ]

    put_options = [
        convert_option(row)
        for _, row in puts.iterrows()
    ]

    def sort_by(
        options: list[dict[str, Any]],
        field: str,
    ) -> list[dict[str, Any]]:
        return sorted(
            options,
            key=lambda option: option[field] or 0,
            reverse=True,
        )

    def average_iv(
        options: list[dict[str, Any]],
    ) -> float | None:
        values = [
            option["implied_volatility"]
            for option in options
            if option["implied_volatility"] is not None
        ]

        if not values:
            return None

        return sum(values) / len(values)

    call_volume = sum(
        option["volume"] or 0
        for option in call_options
    )

    put_volume = sum(
        option["volume"] or 0
        for option in put_options
    )

    call_open_interest = sum(
        option["open_interest"] or 0
        for option in call_options
    )

    put_open_interest = sum(
        option["open_interest"] or 0
        for option in put_options
    )

    def ratio(
        numerator: int,
        denominator: int,
    ) -> float | None:
        if denominator == 0:
            return None

        return numerator / denominator

    def strike_range(
        options: list[dict[str, Any]],
        field: str,
        limit: int = 5,
    ) -> tuple[float | None, float | None]:
        """Return the strike range of the top options."""

        top_options = sort_by(options, field)[:limit]

        strikes = [
            option["strike"]
            for option in top_options
            if option["strike"] is not None
        ]

        if not strikes:
            return None, None

        return min(strikes), max(strikes)

    call_oi_min, call_oi_max = strike_range(
        call_options,
        "open_interest",
    )

    put_oi_min, put_oi_max = strike_range(
        put_options,
        "open_interest",
    )

    call_volume_min, call_volume_max = strike_range(
        call_options,
        "volume",
    )

    put_volume_min, put_volume_max = strike_range(
        put_options,
        "volume",
    )

    # Find the option strike closest to the current stock price.
    all_strikes = sorted(
        {
            option["strike"]
            for option in call_options + put_options
            if option["strike"] is not None
        }
    )

    atm_strike = min(
        all_strikes,
        key=lambda strike: abs(
            strike - underlying_price
        ),
    ) if all_strikes else None

    atm_call = next(
        (
            option
            for option in call_options
            if option["strike"] == atm_strike
        ),
        None,
    )

    atm_put = next(
        (
            option
            for option in put_options
            if option["strike"] == atm_strike
        ),
        None,
    )

    return success_response(
        symbol=symbol,
        expiration=expiration,
        underlying_price=underlying_price,
        days_to_expiration=days_to_expiration,

        metrics={
            "call_volume": call_volume,
            "put_volume": put_volume,
            "call_open_interest": call_open_interest,
            "put_open_interest": put_open_interest,
            "call_put_volume_ratio": ratio(
                call_volume,
                put_volume,
            ),
            "call_put_open_interest_ratio": ratio(
                call_open_interest,
                put_open_interest,
            ),
            "average_call_iv": average_iv(call_options),
            "average_put_iv": average_iv(put_options),
        },

        atm={
            "strike": atm_strike,
            "call": atm_call,
            "put": atm_put,
        },

        highest_volume_calls=sort_by(
            call_options,
            "volume",
        )[:10],

        highest_volume_puts=sort_by(
            put_options,
            "volume",
        )[:10],

        highest_open_interest_calls=sort_by(
            call_options,
            "open_interest",
        )[:10],

        highest_open_interest_puts=sort_by(
            put_options,
            "open_interest",
        )[:10],
        
        analysis={
            "call_open_interest_concentration": {
                "strike_range": (
                    f"${call_oi_min:.2f}-$"
                    f"{call_oi_max:.2f}"
                    if call_oi_min is not None
                    else None
                ),
                "description": (
                    "Top call open interest is concentrated "
                    "within this strike range."
                ),
            },

            "put_open_interest_concentration": {
                "strike_range": (
                    f"${put_oi_min:.2f}-$"
                    f"{put_oi_max:.2f}"
                    if put_oi_min is not None
                    else None
                ),
                "description": (
                    "Top put open interest is concentrated "
                    "within this strike range."
                ),
            },

            "call_volume_concentration": {
                "strike_range": (
                    f"${call_volume_min:.2f}-$"
                    f"{call_volume_max:.2f}"
                    if call_volume_min is not None
                    else None
                ),
            },

            "put_volume_concentration": {
                "strike_range": (
                    f"${put_volume_min:.2f}-$"
                    f"{put_volume_max:.2f}"
                    if put_volume_min is not None
                    else None
                ),
            },

            "interpretation": [
                (
                    "Open interest shows outstanding contracts "
                    "but does not reveal whether positions are "
                    "long or short."
                ),
                (
                    "Call and put open-interest concentrations "
                    "should not be interpreted as definitive "
                    "bullish or bearish signals by themselves."
                ),
                (
                    "Deep in-the-money and deep out-of-the-money "
                    "options may show less reliable implied "
                    "volatility when liquidity is low."
                ),
            ],
        },
    )    