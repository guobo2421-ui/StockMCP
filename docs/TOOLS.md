# Available Tools

StockMCP provides a comprehensive set of MCP tools for market data, company fundamentals, financial analysis, screening, options, and forecasts.

All tools return structured data that AI assistants can use for financial research and investment analysis.


## Market Data
| Tool | Description |
|------|-------------|
| `stock_price` | Latest stock price and trading information |
| `stock_history` | Historical OHLCV price data for a specified period |
| `stock_news` | Latest news for a given stock symbol |
| `market_status` | Current market status |


## Company Fundamentals
| Tool | Description |
|------|-------------|
| `company_info` | Returns company information |
| `income_statement` | Quarterly and annual income statement data |
| `balance_sheet` | Latest quarterly balance sheet data |
| `cash_flow` | Quarterly and annual cash flow statement data |


## Financial Analysis
| Tool | Description |
|------|-------------|
| `profitability_analysis` | Profitability metrics and analysis |
| `liquidity_analysis` | Liquidity metrics and analysis |
| `leverage_analysis` | Leverage metrics and analysis |
| `valuation_analysis` | Valuation metrics and analysis |
| `financial_health_analysis` | Overall financial health analysis |


## Financial Ratios
| Tool | Description |
|------|-------------|
| `financial_ratios` | Key financial ratios |
| `valuation_ratios` | P/E, P/B, EV and other valuation ratios |


## Screening
| Tool | Description |
|------|-------------|
| `compare_watchlist` | Compare multiple companies from a watchlist using financial metrics. |
| `screen_watchlist` | Screen and rank a watchlist of stocks using financial quality scores |


## Options
| Tool | Description |
|------|-------------|
| `option_expirations` | Available option expiration dates |
| `option_chain` | Call and put option chain data |
| `option_summary` | Summarized options analysis and key metrics |


## Reports & Forecasts
| Tool | Description |
|------|-------------|
| `company_report` | Comprehensive company report combining financial metrics, analysis, and market data |
| `company_forecast` | Analyst estimates, price targets, and financial forecasts |


## SEC Financial Data
StockMCP uses SEC Company Facts to retrieve quarterly financial statements,
providing up to eight quarters of standardized historical financial data
for eligible U.S. public companies.


## Notes

- All tools return structured JSON data.
- Data availability depends on the underlying data providers.
- Financial statement data is sourced from SEC Company Facts when available.








