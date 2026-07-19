from services.yahoo import get_company_info
from services.financial_data import (
    get_income_statement,
    get_balance_sheet,
    get_cash_flow,
)

from services.financial_ratios import get_financial_ratios
from services.valuation_ratios import get_valuation_ratios

from services.financial_analysis import (
    get_profitability_analysis,
    get_liquidity_analysis,
    get_leverage_analysis,
    get_valuation_analysis,
    get_financial_health_analysis,
)

from services.financial_ttm import (
    get_ttm_income_statement,
    get_current_balance_sheet,
    get_ttm_cash_flow,
)

from services.company_report import get_company_report


SYMBOL = "GOOGL"


def test_company_info():
    print("\n=== Company info ===")    
    result = get_company_info(SYMBOL)
    print(result)


def test_financial_statements():
    print("\n=== Income statement ===")    
    print(get_income_statement(SYMBOL))

    print("\n=== Balance sheet ===")   
    print(get_balance_sheet(SYMBOL))

    print("\n=== Cash flow ===")    
    print(get_cash_flow(SYMBOL))


def test_ratios():
    print("\n=== Financial ratios ===")    
    print(get_financial_ratios(SYMBOL))

    print("\n=== Valuation ratios ===")    
    print(get_valuation_ratios(SYMBOL))


def test_analysis():

    print("\n=== Profitability ===")
    print(get_profitability_analysis(SYMBOL))

    print("\n=== Liquidity ===")
    print(get_liquidity_analysis(SYMBOL))

    print("\n=== Leverage ===")
    print(get_leverage_analysis(SYMBOL))

    print("\n=== Valuation ===")
    print(get_valuation_analysis(SYMBOL))

    print("\n=== Financial Health ===")
    print(get_financial_health_analysis(SYMBOL))


def test_finacial_ttm():

    print("\n=== ttm imcome statement ===")
    print(get_ttm_income_statement(SYMBOL))

    print("\n=== ttm balance sheet ===")
    print(get_ttm_balance_sheet(SYMBOL))

    print("\n=== ttm cash flow ===")
    print(get_ttm_cash_flow(SYMBOL))

def test_finacial_ttm():

    print("\n=== ttm imcome statement ===")
    print(get_ttm_income_statement(SYMBOL))

    print("\n=== ttm balance sheet ===")
    print(get_current_balance_sheet(SYMBOL))

    print("\n=== ttm cash flow ===")
    print(get_ttm_cash_flow(SYMBOL))

def test_company_report():

    print("\n=== COMPANY REPORT ===")
    report = get_company_report(SYMBOL)

    print(report)



if __name__ == "__main__":

    test_company_info()
    test_financial_statements()
    test_ratios()
    test_analysis()
    test_finacial_ttm()  
    test_company_report()