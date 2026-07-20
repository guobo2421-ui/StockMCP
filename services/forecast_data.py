from typing import Any

import yfinance as yf

from .financial_ttm import (
    get_financial_trends,
)

from .common import (
    success_response,
    error_response,
)


def clean_value(
    value: Any,
) -> Any:

    if value is None:
        return None

    try:

        if hasattr(value, "item"):

            value = value.item()

    except Exception:

        pass

    return value

def calculate_eps_revision_summary(
    eps_estimates: list[dict],
) -> dict[str, Any]:

    summary = {}

    for item in eps_estimates:

        period = item["period"]

        current = item.get("current")

        previous = item.get("90_days_ago")

        if (
            current is None
            or previous is None
            or previous == 0
        ):
            continue

        change_percent = (
            (current - previous)
            / abs(previous)
        ) * 100

        if change_percent > 0.5:

            direction = "UPWARD"

        elif change_percent < -0.5:

            direction = "DOWNWARD"

        else:

            direction = "STABLE"

        summary[period] = {

            "direction": direction,

            "change_percent": round(
                change_percent,
                2,
            ),

            "current_eps": current,

            "eps_90_days_ago": previous,

        }

    return summary

def calculate_price_target_summary(
    price_targets: dict[str, Any],
) -> dict[str, Any]:

    current = price_targets.get(
        "current"
    )

    mean = price_targets.get(
        "mean"
    )

    median = price_targets.get(
        "median"
    )

    high = price_targets.get(
        "high"
    )

    low = price_targets.get(
        "low"
    )

    def calculate_upside(
        target: float | None,
    ) -> float | None:

        if (
            current is None
            or target is None
            or current == 0
        ):
            return None

        return round(

            (
                target - current
            )
            / current
            * 100,

            2,

        )

    return {

        "current_price": current,

        "mean_target": mean,

        "median_target": median,

        "low_target": low,

        "high_target": high,

        "upside_to_mean_percent":
            calculate_upside(mean),

        "upside_to_median_percent":
            calculate_upside(median),

        "upside_to_high_percent":
            calculate_upside(high),

        "downside_to_low_percent":
            calculate_upside(low),

    }

def get_earnings_estimates(
    ticker: yf.Ticker,
) -> dict[str, Any]:

    try:

        data = ticker.get_earnings_dates(
            limit=8
        )

        if data is None or data.empty:

            return {}

        estimates = []

        for index, row in data.iterrows():

            estimates.append({

                "date": str(index),

                "eps_estimate": clean_value(
                    row.get("EPS Estimate")
                ),

                "reported_eps": clean_value(
                    row.get("Reported EPS")
                ),

                "surprise": clean_value(
                    row.get("Surprise")
                ),

                "surprise_percent": clean_value(
                    row.get("Surprise(%)")
                ),

            })

        return {

            "earnings_estimates": estimates

        }

    except Exception:

        return {}

def get_eps_estimates(
    ticker: yf.Ticker,
) -> dict[str, Any]:

    try:

        data = ticker.get_eps_trend()

        if data is None or data.empty:

            return {}

        estimates = []

        for period, row in data.iterrows():

            estimates.append({

                "period": str(period),

                "current": clean_value(
                    row.get("current")
                ),

                "7_days_ago": clean_value(
                    row.get("7daysAgo")
                ),

                "30_days_ago": clean_value(
                    row.get("30daysAgo")
                ),

                "60_days_ago": clean_value(
                    row.get("60daysAgo")
                ),

                "90_days_ago": clean_value(
                    row.get("90daysAgo")
                ),

            })

        return {

            "eps_estimates": estimates

        }

    except Exception:

        return {}

def get_growth_estimates(
    ticker: yf.Ticker,
) -> dict[str, Any]:

    try:

        data = ticker.get_growth_estimates()

        if data is None or data.empty:

            return {}

        estimates = []

        for period, row in data.iterrows():

            stock = clean_value(
                row.get("stock")
            )

            index = clean_value(
                row.get("index")
            )

            industry = clean_value(
                row.get("industry")
            )

            sector = clean_value(
                row.get("sector")
            )

            # Skip rows with no usable data
            if all(
                value is None
                for value in (
                    stock,
                    index,
                    industry,
                    sector,
                )
            ):

                continue

            estimates.append({

                "period": str(period),

                "stock": stock,

                "index": index,

                "industry": industry,

                "sector": sector,

            })

        if not estimates:

            return {}

        return {

            "growth_estimates": estimates

        }

    except Exception:

        return {}

def get_price_targets(
    ticker: yf.Ticker,
) -> dict[str, Any]:

    try:

        data = ticker.get_analyst_price_targets()

        if not data:

            return {}

        return {

            "price_targets": {

                "current": clean_value(
                    data.get("current")
                ),

                "low": clean_value(
                    data.get("low")
                ),

                "high": clean_value(
                    data.get("high")
                ),

                "mean": clean_value(
                    data.get("mean")
                ),

                "median": clean_value(
                    data.get("median")
                ),

            }

        }

    except Exception:

        return {}


def get_analyst_forecast(
    symbol: str,
) -> dict[str, Any]:

    if not symbol:

        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:

        ticker = yf.Ticker(symbol)

        forecast = {}

        forecast.update(
            get_eps_estimates(ticker)
        )

        forecast.update(
            get_price_targets(ticker)
        )

        # -------------------------------------------------
        # EPS revision summary
        # -------------------------------------------------

        eps_estimates = (
            forecast.get(
                "eps_estimates"
            )
        )

        if eps_estimates:

            forecast[
                "eps_revision_summary"
            ] = (
                calculate_eps_revision_summary(
                    eps_estimates
                )
            )

        # -------------------------------------------------
        # Price target summary
        # -------------------------------------------------

        price_targets = (
            forecast.get(
                "price_targets"
            )
        )

        if price_targets:

            forecast[
                "price_target_summary"
            ] = (
                calculate_price_target_summary(
                    price_targets
                )
            )

        return success_response(

            symbol=symbol,

            forecast=forecast,

        )

    except Exception as e:

        return error_response(

            "FORECAST_DATA_ERROR",

            str(e)

        )

def get_company_forecast(
    symbol: str,
) -> dict[str, Any]:

    if not symbol:

        return error_response(
            "MISSING_SYMBOL",
            "symbol is required"
        )

    symbol = symbol.strip().upper()

    try:

        # ---------------------------------------------
        # Historical financial trends
        # ---------------------------------------------

        financial_trends = (
            get_financial_trends(symbol)
        )

        if not financial_trends["success"]:

            return financial_trends

        # ---------------------------------------------
        # Analyst forecast
        # ---------------------------------------------

        analyst_forecast = (
            get_analyst_forecast(symbol)
        )

        if not analyst_forecast["success"]:

            return analyst_forecast

        return success_response(

            symbol=symbol,

            financial_trends=(
                financial_trends["trends"]
            ),

            financial_trend_summary=(
                financial_trends.get(
                    "summary"
                )
            ),

            analyst_forecast=(
                analyst_forecast["forecast"]
            ),

        )

    except ValueError as e:

        return error_response(

            "INSUFFICIENT_DATA",

            str(e)

        )

    except Exception as e:

        return error_response(

            "FORECAST_ERROR",

            str(e)

        )        