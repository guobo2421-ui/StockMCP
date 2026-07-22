import requests
from datetime import date


SEC_HEADERS = {
    "User-Agent": "MCP_Claude guobo2421@gmail.com"
}


CIK_MAPPING: dict[str, str] | None = None

SEC_TICKERS_URL = (
    "https://www.sec.gov/files/company_tickers.json"
)

SEC_BASE_URL = (
    "https://data.sec.gov/api/xbrl/companyfacts"
)

SEC_METRIC_MAPPING = {
    # FLOW_MAPPING
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
    ],

    "gross_profit": [
        "GrossProfit",
        "GrossProfitLoss",
    ],
   
    "cost_of_revenue": [
        "CostOfRevenue",
        "CostOfGoodsAndServicesSold",
    ],

    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
    ],

    # EPS_MAPPING
    "diluted_eps":
        "EarningsPerShareDiluted",   

    "operating_income":
        "OperatingIncomeLoss",

    "operating_cash_flow":
        "NetCashProvidedByUsedInOperatingActivities",

    "capital_expenditures": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],   

    # POINT_IN_TIME_MAPPING
    "stockholders_equity":
        "StockholdersEquity",

    "assets":
        "Assets",

    "liabilities": [
        "Liabilities",
        "LiabilitiesAndStockholdersEquity",
    ],

    "current_debt": [
        "LongTermDebtCurrent",
        "DebtCurrent",
        "LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths",        
    ],

    "noncurrent_debt":
        "LongTermDebtNoncurrent",  
              
}

def get_cik_mapping() -> dict[str, str]:

    global CIK_MAPPING

    if CIK_MAPPING is not None:
        return CIK_MAPPING

    response = requests.get(
        SEC_TICKERS_URL,
        headers=SEC_HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    CIK_MAPPING = {
        item["ticker"].upper():
        str(item["cik_str"]).zfill(10)
        for item in data.values()
    }

    return CIK_MAPPING

def get_duration_days(start: str, end: str) -> int:

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    return (end_date - start_date).days


def get_sec_companyfacts(symbol: str) -> dict:

    symbol = symbol.strip().upper()

    cik_mapping = get_cik_mapping()

    cik = cik_mapping.get(symbol)

    if not cik:
        raise ValueError(
            f"CIK not found for symbol: {symbol}"
        )

    url = (
        f"{SEC_BASE_URL}/CIK{cik}.json"
    )

    response = requests.get(
        url,
        headers=SEC_HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def deduplicate_records(
    records: list[dict],
) -> list[dict]:

    unique = {}

    for item in records:

        key = (

            item.get("period_start"),

            item.get("period_end"),

        )


        if (

            key not in unique

            or item.get("filed", "")
            > unique[key].get("filed", "")

        ):

            unique[key] = item


    return list(unique.values())

def get_sec_gross_profit(
    symbol: str,
    limit: int = 8,
) -> list[dict]:

    try:

        return get_sec_quarterly_data(
            symbol,
            "gross_profit",
            limit,
        )

    except ValueError:

        # Request more history than needed
        revenue = get_sec_quarterly_data_from_candidates(
            symbol,
            "revenue",
            12,
        )

        cost_of_revenue = get_sec_quarterly_data_from_candidates(
            symbol,
            "cost_of_revenue",
            12,
        )

        cost_by_date = {
            item["period_end"]: item
            for item in cost_of_revenue
        }

        gross_profit = []

        for revenue_item in revenue:

            cost_item = cost_by_date.get(
                revenue_item["period_end"]
            )

            if cost_item is None:
                continue

            gross_profit.append({

                **revenue_item,

                "value": (
                    revenue_item["value"]
                    - cost_item["value"]
                ),

                "form": "CALCULATED",

            })

        if len(gross_profit) < limit:

            raise ValueError(
                f"Unable to calculate "
                f"{limit} quarterly gross-profit reports."
            )

        return gross_profit[-limit:]

def _get_quarterly_data_from_concept(
    observations: list[dict],
) -> list[dict]:

    observations_by_period = {}

    for item in observations:

        start = item.get("start")
        end = item.get("end")
        form = item.get("form")
        fp = item.get("fp")

        if not start or not end:
            continue

        if form == "10-Q" and fp == "Q1":

            period_type = "Q1"

        elif form == "10-Q" and fp == "Q2":

            period_type = "Q2"

        elif form == "10-Q" and fp == "Q3":

            period_type = "Q3"

        elif form == "10-K" and fp == "FY":

            period_type = "FY"

        else:

            continue

        key = (
            start,
            end,
            period_type,
        )

        if (
            key not in observations_by_period
            or item.get("filed", "")
            > observations_by_period[key].get(
                "filed",
                "",
            )
        ):

            observations_by_period[key] = item

    fiscal_years = {}

    for item in observations_by_period.values():

        start = item["start"]
        fp = item.get("fp")

        if fp not in (
            "Q1",
            "Q2",
            "Q3",
            "FY",
        ):

            continue

        fiscal_years.setdefault(
            start,
            {},
        )[fp] = item

    quarterly = []

    for periods in fiscal_years.values():

        q1 = periods.get("Q1")
        q2 = periods.get("Q2")
        q3 = periods.get("Q3")
        fy = periods.get("FY")

        if q1:

            quarterly.append({

                "period_start":
                    q1["start"],

                "period_end":
                    q1["end"],

                "value":
                    q1["val"],

                "form":
                    "10-Q",

                "filed":
                    q1.get("filed"),

            })

        if q1 and q2:

            quarterly.append({

                "period_start":
                    q1["end"],

                "period_end":
                    q2["end"],

                "value":
                    q2["val"] - q1["val"],

                "form":
                    "CALCULATED",

                "filed":
                    q2.get("filed"),

            })

        if q2 and q3:

            quarterly.append({

                "period_start":
                    q2["end"],

                "period_end":
                    q3["end"],

                "value":
                    q3["val"] - q2["val"],

                "form":
                    "CALCULATED",

                "filed":
                    q3.get("filed"),

            })

        if q3 and fy:

            quarterly.append({

                "period_start":
                    q3["end"],

                "period_end":
                    fy["end"],

                "value":
                    fy["val"] - q3["val"],

                "form":
                    "CALCULATED",

                "filed":
                    fy.get("filed"),

            })

    quarterly = deduplicate_records(
        quarterly
    )

    quarterly = [

        record

        for record in quarterly

        if record["period_start"]
        < record["period_end"]

    ]

    quarterly.sort(
        key=lambda x:
            x["period_end"]
    )

    return quarterly

def get_sec_quarterly_data_from_candidates(
    symbol: str,
    metric: str,
    limit: int = 8,
) -> list[dict]:
    """
    Retrieve quarterly flow data by combining multiple SEC concepts.

    This is useful when different SEC concepts provide different
    historical periods for the same financial metric.
    """

    if metric not in SEC_METRIC_MAPPING:

        raise ValueError(
            f"Unsupported metric: {metric}"
        )

    data = get_sec_companyfacts(symbol)

    sec_metrics = SEC_METRIC_MAPPING[metric]

    if isinstance(sec_metrics, str):

        sec_metrics = [
            sec_metrics
        ]

    facts = (
        data
        .get("facts", {})
        .get("us-gaap", {})
    )

    combined = {}

    for candidate in sec_metrics:

        concept = facts.get(candidate)

        if concept is None:

            continue

        units = concept.get("units", {})

        if metric == "diluted_eps":

            unit = "USD/shares"

        else:

            unit = "USD"

        if unit not in units:

            continue

        observations = units[unit]

        # Use the existing quarterly reconstruction logic
        # for this individual candidate.
        #
        # Temporarily use the candidate as a single-metric
        # mapping.

        candidate_observations = (
            _get_quarterly_observations(
                observations
            )
        )

        for item in candidate_observations:

            key = item["period_end"]

            if (

                key not in combined

                or item.get("filed", "")
                > combined[key].get(
                    "filed",
                    ""
                )

            ):

                combined[key] = item

    quarterly = list(
        combined.values()
    )

    quarterly.sort(
        key=lambda x:
            x["period_end"]
    )

    if len(quarterly) < limit:

        raise ValueError(
            f"Unable to retrieve "
            f"{limit} quarterly reports for "
            f"{symbol} {metric}. "
            f"Only {len(quarterly)} available."
        )

    return quarterly[-limit:]

def get_sec_quarterly_data_from_candidates(
    symbol: str,
    metric: str,
    limit: int = 8,
) -> list[dict]:

    if metric not in SEC_METRIC_MAPPING:

        raise ValueError(
            f"Unsupported metric: {metric}"
        )

    data = get_sec_companyfacts(
        symbol
    )

    sec_metrics = SEC_METRIC_MAPPING.get(
        metric
    )

    if not sec_metrics:

        raise ValueError(
            f"SEC metric not mapped: {metric}"
        )

    if isinstance(sec_metrics, str):

        sec_metrics = [
            sec_metrics
        ]

    facts = data.get(
        "facts",
        {}
    ).get(
        "us-gaap",
        {}
    )

    if metric == "diluted_eps":

        unit = "USD/shares"

    else:

        unit = "USD"

    combined = {}

    for candidate in sec_metrics:

        concept = facts.get(
            candidate
        )

        if concept is None:

            continue

        units = concept.get(
            "units",
            {}
        )

        if unit not in units:

            continue

        candidate_quarterly = (
            _get_quarterly_data_from_concept(
                units[unit]
            )
        )

        for item in candidate_quarterly:

            period_end = item[
                "period_end"
            ]

            if (

                period_end not in combined

                or item.get("filed", "")
                > combined[period_end].get(
                    "filed",
                    ""
                )

            ):

                combined[period_end] = item

    quarterly = list(
        combined.values()
    )

    quarterly.sort(
        key=lambda x:
            x["period_end"]
    )

    if len(quarterly) < limit:

        raise ValueError(

            f"Unable to retrieve "

            f"{limit} quarterly reports for "

            f"{symbol} {metric}. "

            f"Only {len(quarterly)} available."

        )

    return quarterly[-limit:] 

def get_sec_quarterly_data(
    symbol: str,
    metric: str,
    limit: int = 8,
) -> list[dict]:
    """
    Retrieve quarterly flow data from SEC Company Facts.

    For ordinary flow metrics:

        Q1, Q2, Q3:
            Use standalone quarterly values from 10-Q filings.

        Q4:
            Calculate:

                FY - Q1 - Q2 - Q3

    For diluted EPS:

        SEC may report cumulative EPS:

            Q1: 3 months
            Q2: 6 months
            Q3: 9 months
            FY: 12 months

        Therefore:

            Q1 = Q1

            Q2 = Q2 cumulative - Q1

            Q3 = Q3 cumulative - Q2 cumulative

            Q4 = FY - Q3 cumulative
    """

    if metric not in SEC_METRIC_MAPPING:

        raise ValueError(
            f"Unsupported metric: {metric}"
        )


    data = get_sec_companyfacts(
        symbol
    )


    sec_metrics = SEC_METRIC_MAPPING.get(
        metric
    )


    if not sec_metrics:

        raise ValueError(
            f"SEC metric not mapped: {metric}"
        )


    if isinstance(sec_metrics, str):

        sec_metrics = [
            sec_metrics
        ]


    facts = data.get(
        "facts",
        {}
    ).get(
        "us-gaap",
        {}
    )


    # =========================================================
    # Select unit
    # =========================================================

    if metric == "diluted_eps":

        unit = "USD/shares"

    else:

        unit = "USD"


    # =========================================================
    # Select SEC concept
    #
    # Some companies have multiple possible SEC tags for the
    # same metric.
    #
    # Do not simply select the first existing tag. One tag may
    # contain only old historical data while another contains
    # current data.
    #
    # Select the candidate with the latest observation date.
    # =========================================================

    concept = None

    selected_candidate = None

    latest_end = ""


    for candidate in sec_metrics:

        if candidate not in facts:

            continue


        candidate_concept = facts[candidate]


        candidate_units = candidate_concept.get(
            "units",
            {}
        )


        if unit not in candidate_units:

            continue


        candidate_observations = candidate_units[unit]


        candidate_latest_end = max(

            (

                item.get("end", "")

                for item in candidate_observations

                if item.get("end")

            ),

            default=""

        )


        if candidate_latest_end > latest_end:

            latest_end = candidate_latest_end

            concept = candidate_concept

            selected_candidate = candidate

    if concept is None:

        raise ValueError(

            f"SEC metric not found: {sec_metrics}"

        )


    # =========================================================
    # Get observations
    # =========================================================

    observations = concept["units"][unit]


    # =========================================================
    # STEP 1
    #
    # Collect Q1, Q2, Q3, and FY observations.
    # =========================================================

    observations_by_period = {}


    for item in observations:

        start = item.get("start")

        end = item.get("end")

        form = item.get("form")

        fp = item.get("fp")


        if not start or not end:

            continue


        if form == "10-Q" and fp == "Q1":

            period_type = "Q1"


        elif form == "10-Q" and fp == "Q2":

            period_type = "Q2"


        elif form == "10-Q" and fp == "Q3":

            period_type = "Q3"


        elif form == "10-K" and fp == "FY":

            period_type = "FY"


        else:

            continue


        key = (

            start,

            end,

            period_type,

        )


        # Keep the latest filed version of the same
        # fiscal-period observation.

        if (

            key not in observations_by_period

            or item.get("filed", "")
            > observations_by_period[key].get(
                "filed",
                ""
            )

        ):

            observations_by_period[key] = item


    observations = list(

        observations_by_period.values()

    )


    # =========================================================
    # STEP 2
    #
    # Group observations by fiscal-year start.
    # =========================================================

    fiscal_years = {}


    for item in observations:

        start = item["start"]

        fp = item.get("fp")


        if fp not in (

            "Q1",

            "Q2",

            "Q3",

            "FY",

        ):

            continue


        fiscal_years.setdefault(

            start,

            {}

        )[fp] = item


    # =========================================================
    # STEP 3
    #
    # Calculate standalone quarterly values.
    # =========================================================

    quarterly = []


    for periods in fiscal_years.values():

        q1 = periods.get("Q1")

        q2 = periods.get("Q2")

        q3 = periods.get("Q3")

        fy = periods.get("FY")


        # -----------------------------------------------------
        # Q1
        # -----------------------------------------------------

        if q1:

            quarterly.append({

                "period_start":

                    q1["start"],

                "period_end":

                    q1["end"],

                "value":

                    q1["val"],

                "form":

                    "10-Q",

                "filed":

                    q1.get("filed"),

            })


        # -----------------------------------------------------
        # Q2
        # -----------------------------------------------------

        if q1 and q2:

            quarterly.append({

                "period_start":

                    q1["end"],

                "period_end":

                    q2["end"],

                "value":

                    q2["val"]

                    - q1["val"],

                "form":

                    "CALCULATED",

                "filed":

                    q2.get("filed"),

            })


        # -----------------------------------------------------
        # Q3
        # -----------------------------------------------------

        if q2 and q3:

            quarterly.append({

                "period_start":

                    q2["end"],

                "period_end":

                    q3["end"],

                "value":

                    q3["val"]

                    - q2["val"],

                "form":

                    "CALCULATED",

                "filed":

                    q3.get("filed"),

            })


        # -----------------------------------------------------
        # Q4
        # -----------------------------------------------------

        if q3 and fy:

            quarterly.append({

                "period_start":

                    q3["end"],

                "period_end":

                    fy["end"],

                "value":

                    fy["val"]

                    - q3["val"],

                "form":

                    "CALCULATED",

                "filed":

                    fy.get("filed"),

            })


    # =========================================================
    # STEP 4
    #
    # Remove duplicate quarterly periods.
    # =========================================================

    quarterly = deduplicate_records(

        quarterly

    )

    quarterly = [
        record
        for record in quarterly
        if record["period_start"] < record["period_end"]
    ]

    # =========================================================
    # STEP 5
    #
    # Sort chronologically.
    # =========================================================

    quarterly.sort(

        key=lambda x:

            x["period_end"]

    )

    # =========================================================
    # STEP 6
    #
    # Validate requested history.
    # =========================================================

    if len(quarterly) < limit:

        raise ValueError(

            f"Unable to retrieve "

            f"{limit} quarterly reports for "

            f"{symbol} {metric}. "

            f"Only {len(quarterly)} available."

        )


    return quarterly[-limit:]

def get_sec_cumulative_flow_quarterly_data(
    symbol: str,
    metric: str,
    limit: int = 8,
) -> list[dict]:

    data = get_sec_companyfacts(symbol)

    sec_metrics = SEC_METRIC_MAPPING.get(metric)

    if not sec_metrics:
        raise ValueError(
            f"SEC metric not mapped: {metric}"
        )

    if isinstance(sec_metrics, str):
        sec_metrics = [sec_metrics]

    facts = data.get("facts", {}).get("us-gaap", {})

    concept = None
    concept_name = None
    latest_end = ""

    for candidate in sec_metrics:

        if candidate not in facts:

            continue

        candidate_concept = facts[candidate]

        candidate_units = candidate_concept.get(
            "units",
            {}
        )

        if "USD" not in candidate_units:

            continue

        candidate_observations = candidate_units["USD"]

        candidate_latest_end = max(

            (
                item.get("end", "")

                for item in candidate_observations

                if item.get("end")

            ),

            default=""

        )

        if candidate_latest_end > latest_end:

            latest_end = candidate_latest_end

            concept_name = candidate

            concept = candidate_concept


    if concept is None:

        raise ValueError(
            f"SEC metric not found: {sec_metrics}"
        )

    if "USD" not in concept["units"]:

        raise ValueError(
            f"USD unit not found for {metric}"
        )

    observations = concept["units"]["USD"]

    # ---------------------------------------------------------
    # Step 1: Collect valid annual and quarterly observations
    # ---------------------------------------------------------

    observations_by_period = {}

    for item in observations:

        start = item.get("start")
        end = item.get("end")
        form = item.get("form")
        fp = item.get("fp")

        if not start or not end:
            continue

        days = get_duration_days(start, end)

        # Q1: approximately 3 months
        if form == "10-Q" and fp == "Q1":
            period_type = "Q1"

        # Q2: approximately 6 months
        elif form == "10-Q" and fp == "Q2":
            period_type = "Q2"

        # Q3: approximately 9 months
        elif form == "10-Q" and fp == "Q3":
            period_type = "Q3"

        # FY: approximately 12 months
        elif form == "10-K" and fp == "FY":
            period_type = "FY"

        else:
            continue

        key = (
            start,
            end,
            period_type,
        )

        # Keep latest filed observation
        if (
            key not in observations_by_period
            or item.get("filed", "")
            > observations_by_period[key].get("filed", "")
        ):
            observations_by_period[key] = item

    observations = list(observations_by_period.values())

    # ---------------------------------------------------------
    # Step 2: Group observations by fiscal year
    # ---------------------------------------------------------

    fiscal_years = {}

    for item in observations:

        start = item["start"]
        period_type = None

        fp = item.get("fp")

        if fp == "Q1":
            period_type = "Q1"
        elif fp == "Q2":
            period_type = "Q2"
        elif fp == "Q3":
            period_type = "Q3"
        elif fp == "FY":
            period_type = "FY"

        if not period_type:
            continue

        fiscal_years.setdefault(start, {})[
            period_type
        ] = item

    # ---------------------------------------------------------
    # Step 3: Calculate standalone quarterly values
    # ---------------------------------------------------------

    quarterly = []

    for fiscal_year, periods in fiscal_years.items():

        q1 = periods.get("Q1")
        q2 = periods.get("Q2")
        q3 = periods.get("Q3")
        fy = periods.get("FY")

        # Need Q1
        if q1:

            q1_value = q1["val"]

            quarterly.append({
                "period_start": q1["start"],
                "period_end": q1["end"],
                "value": q1_value,
                "form": "10-Q",
                "filed": q1.get("filed"),
            })

        # Need Q1 + Q2
        if q1 and q2:

            q2_value = q2["val"] - q1["val"]

            quarterly.append({
                "period_start": q1["end"],
                "period_end": q2["end"],
                "value": q2_value,
                "form": "CALCULATED",
                "filed": q2.get("filed"),
            })

        # Need Q1 + Q2 + Q3
        if q1 and q2 and q3:

            q3_value = (
                q3["val"]
                - q2["val"]
            )

            quarterly.append({
                "period_start": q2["end"],
                "period_end": q3["end"],
                "value": q3_value,
                "form": "CALCULATED",
                "filed": q3.get("filed"),
            })

        # Need FY - Q1 - Q2 - Q3
        if q1 and q2 and q3 and fy:

            q4_value = (
                fy["val"]
                - q3["val"]
            )

            quarterly.append({
                "period_start": q3["end"],
                "period_end": fy["end"],
                "value": q4_value,
                "form": "CALCULATED",
                "filed": fy.get("filed"),
            })

    # ---------------------------------------------------------
    # Step 4: Remove duplicate quarters
    # ---------------------------------------------------------

    unique = {}

    for item in quarterly:

        key = (
            item["period_start"],
            item["period_end"],
        )

        if (
            key not in unique
            or item.get("filed", "")
            > unique[key].get("filed", "")
        ):
            unique[key] = item

    quarterly = list(unique.values())

    # ---------------------------------------------------------
    # Step 5: Sort chronologically
    # ---------------------------------------------------------

    quarterly.sort(
        key=lambda x: x["period_end"]
    )

    return quarterly[-limit:] 

def get_sec_point_in_time_data(
    symbol: str,
    metric: str,
    limit: int = 8,
) -> list[dict]:
    """
    Retrieve point-in-time financial data from SEC CompanyFacts.

    Supported metrics:
        assets
        stockholders_equity
    """

    if metric not in SEC_METRIC_MAPPING:
        raise ValueError(
            f"Unsupported point-in-time metric: {metric}"
        )

    data = get_sec_companyfacts(symbol)

    sec_metrics = SEC_METRIC_MAPPING.get(metric)

    if not sec_metrics:
        raise ValueError(
            f"SEC metric not mapped: {metric}"
        )

    if isinstance(sec_metrics, str):
        sec_metrics = [sec_metrics]

    facts = data["facts"]["us-gaap"]

    concept = None
    concept_name = None

    for candidate in sec_metrics:

        if candidate in facts:

            concept_name = candidate
            concept = facts[candidate]

            break

    if concept is None:

        raise ValueError(
            f"SEC metric not found: {sec_metrics}"
        )

    observations = concept["units"]["USD"]

    # ---------------------------------------------------------
    # Step 1: Keep balance-sheet observations
    # ---------------------------------------------------------

    records = []

    for item in observations:

        end = item.get("end")
        form = item.get("form")

        if not end:
            continue

        if form not in ("10-Q", "10-K"):
            continue

        records.append({
            "period_start": None,
            "period_end": end,
            "value": item["val"],
            "form": form,
            "filed": item.get("filed"),
        })

    # ---------------------------------------------------------
    # Step 2: Deduplicate by reporting date
    # ---------------------------------------------------------

    unique = {}

    for item in records:

        key = item["period_end"]

        if (
            key not in unique
            or item.get("filed", "")
            > unique[key].get("filed", "")
        ):
            unique[key] = item

    records = list(unique.values())

    # ---------------------------------------------------------
    # Step 3: Sort chronologically
    # ---------------------------------------------------------

    records.sort(
        key=lambda x: (
            x["period_end"],
            x.get("filed", ""),
        )
    )

    # ---------------------------------------------------------
    # Step 4: Return latest N observations
    # ---------------------------------------------------------

    return records[-limit:]       