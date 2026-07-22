from .sec_financial_data import (
    get_sec_quarterly_data,
    get_sec_cumulative_flow_quarterly_data,
    get_sec_point_in_time_data,
    get_sec_gross_profit,
)

from .common import (
    success_response,
    error_response,
    safe_divide,
)

def calculate_ttm(records):
    if len(records) < 4:
        raise ValueError(
            "At least 4 quarterly reports are required."
        )

    return sum(
        item["value"]
        for item in records[-4:]
    )

def calculate_previous_ttm(records):
    if len(records) < 8:
        raise ValueError(
            "At least 8 quarterly reports are required."
        )

    return sum(
        item["value"]
        for item in records[:4]
    )

def calculate_ttm_average(data):
    values = [
        item["value"]
        for item in data[-4:]
    ]

    return sum(values) / len(values)


def calculate_previous_ttm_average(data):
    values = [
        item["value"]
        for item in data[:4]
    ]

    return sum(values) / len(values)

def get_current_previous_point_in_time(
    records: list[dict],
) -> tuple[dict, dict]:

    if len(records) < 2:

        raise ValueError(
            "At least 2 point-in-time records are required."
        )

    current = records[-1]

    previous = records[-2]

    return current, previous

def calculate_trend_direction(
    latest_value: float | None,
    previous_value: float | None,
    threshold: float = 0.02,
) -> str:

    if (
        latest_value is None
        or previous_value is None
    ):
        return "UNKNOWN"

    if previous_value == 0:
        return "UNKNOWN"

    change = (
        latest_value - previous_value
    ) / abs(previous_value)

    if change > threshold:
        return "IMPROVING"

    if change < -threshold:
        return "DECLINING"

    return "STABLE"


def calculate_percent_change(
    latest_value: float | None,
    previous_value: float | None,
) -> float | None:

    if (
        latest_value is None
        or previous_value is None
        or previous_value == 0
    ):
        return None

    return (
        (latest_value - previous_value)
        / abs(previous_value)
    ) * 100

def get_trend_summary(
    trends: list[dict],
) -> dict:

    if len(trends) < 5:
        raise ValueError(
            "At least 5 quarterly trends are required "
            "for trend summary."
        )

    latest = trends[-1]

    # Compare with the same quarter one year earlier
    previous = trends[-5]

    return {

        "latest_period": latest["period_end"],

        "comparison_period": previous["period_end"],

        # -------------------------------------------------
        # Revenue
        # -------------------------------------------------

        "revenue": {

            "direction": calculate_trend_direction(
                latest["revenue"],
                previous["revenue"],
            ),

            "change_percent": round(
                calculate_percent_change(
                    latest["revenue"],
                    previous["revenue"],
                ),
                2,
            ),

        },

        # -------------------------------------------------
        # Gross Margin
        # -------------------------------------------------

        "gross_margin": {

            "direction": calculate_trend_direction(
                latest["gross_margin"],
                previous["gross_margin"],
            ),

            "change_percentage_points": round(

                (
                    latest["gross_margin"]
                    - previous["gross_margin"]
                ) * 100,

                2,

            ),

        },

        # -------------------------------------------------
        # Operating Margin
        # -------------------------------------------------

        "operating_margin": {

            "direction": calculate_trend_direction(
                latest["operating_margin"],
                previous["operating_margin"],
            ),

            "change_percentage_points": round(

                (
                    latest["operating_margin"]
                    - previous["operating_margin"]
                ) * 100,

                2,

            ),

        },

        # -------------------------------------------------
        # Net Income
        # -------------------------------------------------

        "net_income": {

            "direction": calculate_trend_direction(
                latest["net_income"],
                previous["net_income"],
            ),

            "change_percent": round(
                calculate_percent_change(
                    latest["net_income"],
                    previous["net_income"],
                ),
                2,
            ),

        },

        # -------------------------------------------------
        # Free Cash Flow
        # -------------------------------------------------

        "free_cash_flow": {

            "direction": calculate_trend_direction(
                latest["free_cash_flow"],
                previous["free_cash_flow"],
            ),

            "change_percent": round(
                calculate_percent_change(
                    latest["free_cash_flow"],
                    previous["free_cash_flow"],
                ),
                2,
            ),

        },

    }

def get_ttm_income_statement(symbol: str) -> dict:

    revenue = get_sec_quarterly_data(
        symbol,
        "revenue",
        8,
    )

    gross_profit = get_sec_gross_profit(
        symbol,
        8,
    )

    net_income = get_sec_quarterly_data(
        symbol,
        "net_income",
        8,
    )

    operating_income = get_sec_quarterly_data(
        symbol,
        "operating_income",
        8,
    )

    diluted_eps = get_sec_quarterly_data(
        symbol,
        "diluted_eps",
        8,
    )

    if (
        len(revenue) < 4
        or len(gross_profit) < 4        
        or len(net_income) < 4
        or len(operating_income) < 4           
        or len(diluted_eps) < 4
    ):
        raise ValueError(
            "At least 4 quarterly reports are required for TTM calculation."
        )

    current_ttm_revenue = calculate_ttm(
        revenue
    )

    previous_ttm_revenue = calculate_previous_ttm(
        revenue
    )

    current_ttm_gross_profit = calculate_ttm(
        gross_profit
    )

    previous_ttm_gross_profit = calculate_previous_ttm(
        gross_profit
    )

    current_ttm_net_income = calculate_ttm(
        net_income
    )

    previous_ttm_net_income = calculate_previous_ttm(
        net_income
    )


    current_ttm_operating_income = calculate_ttm(
        operating_income
    )

    previous_ttm_operating_income = calculate_previous_ttm(
        operating_income
    )

    current_ttm_diluted_eps = calculate_ttm(
        diluted_eps
    )

    previous_ttm_diluted_eps = calculate_previous_ttm(
        diluted_eps
    )

    return success_response(

        symbol=symbol,

        current_ttm={

            "revenue": current_ttm_revenue,

            "gross_profit": current_ttm_gross_profit,

            "net_income": current_ttm_net_income,

            "operating_income":
                current_ttm_operating_income,

            "diluted_eps": current_ttm_diluted_eps,

            "latest_date": revenue[-1]["period_end"],
        },

        previous_ttm={

            "revenue": previous_ttm_revenue,

            "gross_profit": previous_ttm_gross_profit,

            "net_income": previous_ttm_net_income,

            "operating_income":
                previous_ttm_operating_income,

            "diluted_eps": previous_ttm_diluted_eps,

        },

    )


def get_ttm_cash_flow(symbol: str) -> dict:

    operating_cash_flow = get_sec_cumulative_flow_quarterly_data(
        symbol,
        "operating_cash_flow",
        8,
    )

    capital_expenditures = get_sec_cumulative_flow_quarterly_data(
        symbol,
        "capital_expenditures",
        8,
    )

    if (
        len(operating_cash_flow) < 4
        or len(capital_expenditures) < 4        
    ):
        raise ValueError(
            "At least 4 quarterly reports are required for TTM calculation."
        )

    current_ttm_operating_cash_flow = calculate_ttm(
        operating_cash_flow
    )

    previous_ttm_operating_cash_flow = calculate_previous_ttm(
        operating_cash_flow
    )
    
    current_ttm_capital_expenditures = calculate_ttm(
        capital_expenditures
    )

    previous_ttm_capital_expenditures = calculate_previous_ttm(
        capital_expenditures
    )

    return success_response(

        symbol=symbol,

        current_ttm={

            "operating_cash_flow": current_ttm_operating_cash_flow,

            "capital_expenditures": current_ttm_capital_expenditures,
        },

        previous_ttm={

            "operating_cash_flow": previous_ttm_operating_cash_flow,

            "capital_expenditures": previous_ttm_capital_expenditures,
        },

    )

def get_current_balance_sheet(symbol: str) -> dict:

    stockholders_equity = get_sec_point_in_time_data(
        symbol,
        "stockholders_equity",
        8,
    )

    assets = get_sec_point_in_time_data(
        symbol,
        "assets",
        8,
    )

    liabilities = get_sec_point_in_time_data(
        symbol,
        "liabilities",
        8,
    )

    current_debt = get_sec_point_in_time_data(
        symbol,
        "current_debt",
        8,
    )

    noncurrent_debt = get_sec_point_in_time_data(
        symbol,
        "noncurrent_debt",
        8,
    )

    if (
        not stockholders_equity
        or not assets
        or not liabilities
        or not current_debt
        or not noncurrent_debt
    ):
        raise ValueError(
            "Current balance-sheet data is required."
        )

    current_equity = stockholders_equity[-1]
    current_assets = assets[-1]
    current_liabilities = liabilities[-1]
    current_current_debt = current_debt[-1]
    current_noncurrent_debt = noncurrent_debt[-1]

    return success_response(

        symbol=symbol,

        current={

            "stockholders_equity":
                current_equity["value"],

            "assets":
                current_assets["value"],

            "liabilities":
                current_liabilities["value"],

            "current_debt":
                current_current_debt["value"],

            "noncurrent_debt":
                current_noncurrent_debt["value"],

            "latest_date":
                current_assets["period_end"],
        },

    )

# SEC historical trends
def get_financial_trends(symbol: str) -> dict:

    revenue = get_sec_quarterly_data(
        symbol,
        "revenue",
        8,
    )

    gross_profit = get_sec_gross_profit(
        symbol,
        8,
    )

    operating_income = get_sec_quarterly_data(
        symbol,
        "operating_income",
        8,
    )

    net_income = get_sec_quarterly_data(
        symbol,
        "net_income",
        8,
    )

    operating_cash_flow = (
        get_sec_cumulative_flow_quarterly_data(
            symbol,
            "operating_cash_flow",
            8,
        )
    )

    capital_expenditures = (
        get_sec_cumulative_flow_quarterly_data(
            symbol,
            "capital_expenditures",
            8,
        )
    )

    # ---------------------------------------------------------
    # Validate data
    # ---------------------------------------------------------
    if (
        len(revenue) < 4
        or len(gross_profit) < 4
        or len(operating_income) < 4
        or len(net_income) < 4
        or len(operating_cash_flow) < 4
        or len(capital_expenditures) < 4
    ):
        raise ValueError(
            "At least 4 quarterly reports are required "
            "for financial trends."
        )

    # ---------------------------------------------------------
    # Create lookup dictionaries by period_end
    # ---------------------------------------------------------

    gross_profit_by_date = {
        item["period_end"]: item
        for item in gross_profit
    }

    operating_income_by_date = {
        item["period_end"]: item
        for item in operating_income
    }

    net_income_by_date = {
        item["period_end"]: item
        for item in net_income
    }

    operating_cash_flow_by_date = {
        item["period_end"]: item
        for item in operating_cash_flow
    }

    capital_expenditures_by_date = {
        item["period_end"]: item
        for item in capital_expenditures
    }

    # ---------------------------------------------------------
    # Build trends
    # ---------------------------------------------------------

    trends = []

    for revenue_item in revenue:

        period_end = revenue_item["period_end"]

        revenue_value = revenue_item["value"]

        gross_profit_item = (
            gross_profit_by_date.get(period_end)
        )

        operating_income_item = (
            operating_income_by_date.get(period_end)
        )

        net_income_item = (
            net_income_by_date.get(period_end)
        )

        operating_cash_flow_item = (
            operating_cash_flow_by_date.get(period_end)
        )

        capital_expenditures_item = (
            capital_expenditures_by_date.get(period_end)
        )

        # Skip incomplete quarters
        if (
            gross_profit_item is None
            or operating_income_item is None
            or net_income_item is None
            or operating_cash_flow_item is None
            or capital_expenditures_item is None
        ):
            continue

        gross_profit_value = (
            gross_profit_item["value"]
        )

        operating_income_value = (
            operating_income_item["value"]
        )

        net_income_value = (
            net_income_item["value"]
        )

        operating_cash_flow_value = (
            operating_cash_flow_item["value"]
        )

        capital_expenditures_value = (
            capital_expenditures_item["value"]
        )

        free_cash_flow = (
            operating_cash_flow_value
            - abs(capital_expenditures_value)
        )

        trends.append({

            "period_end": period_end,

            "revenue": revenue_value,

            "gross_margin": safe_divide(
                gross_profit_value,
                revenue_value,
            ),

            "operating_margin": safe_divide(
                operating_income_value,
                revenue_value,
            ),

            "net_income": net_income_value,

            "free_cash_flow": free_cash_flow,

        })
       
    if len(trends) < 4:

        raise ValueError(
            "At least 4 complete quarterly reports "
            "are required for financial trends."
        )

    summary = get_trend_summary(
        trends
    )

    return success_response(

        symbol=symbol,

        count=len(trends),

        trends=trends,

        summary=summary,

    )