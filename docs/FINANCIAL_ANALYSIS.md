# Financial Analysis Guide

StockMCP provides AI-assisted financial analysis using SEC filings, company fundamentals, financial ratios, and scoring models.

The analysis combines historical financial data, profitability metrics, liquidity measurements, leverage evaluation, valuation indicators, and financial health scoring.


## Overview

StockMCP financial analysis includes:

- Income statement analysis
- Balance sheet analysis
- Cash flow analysis
- Financial ratios
- Financial health scoring
- Company comparison
- Watchlist screening

StockMCP analyzes companies across:

- Profitability
- Liquidity
- Leverage
- Valuation
- Financial health


## Data Sources

StockMCP uses:

- SEC CompanyFacts API
  - Quarterly financial statements
  - Up to 8 quarters of historical data

  SEC CompanyFacts data may contain company-specific reporting differences. StockMCP normalizes available financial metrics to provide consistent analysis across companies.

- Yahoo Finance
  - Market price
  - Company information
  - Market data


## Analysis Workflow

StockMCP follows a multi-step financial analysis process:
```text
SEC Financial Statements
          |
          ▼
Quarterly Financial Data
          |
          ▼
TTM Calculations
          |
          ▼
Financial Ratios
          |
          ▼
Category Scores
          |
          ▼
Overall Financial Assessment
```

The workflow combines historical financial performance with current market information to generate an AI-readable company analysis.


## Financial Metrics

### Profitability

Measures a company's ability to generate profit.

Metrics include:
- Gross margin
- Operating margin
- Net margin
- Return on equity (ROE)
- Return on assets (ROA)


#### Gross Margin

Formula:

Gross Profit / Revenue

Indicates pricing power and operational efficiency.

#### Operating Margin

Formula:

Operating Income / Revenue

Measures profitability after operating expenses.

#### Net Margin

Formula:

Net Income / Revenue

Shows the final profitability after all expenses.


### Liquidity Analysis

Evaluates a company's ability to meet short-term obligations.

#### Current Ratio

Formula:

Current Assets / Current Liabilities

Higher values generally indicate stronger short-term financial flexibility.


### Leverage Analysis

Measures financial risk from debt.

#### Debt to Equity

Formula:

Total Debt / Shareholders' Equity

Lower leverage generally indicates lower financial risk.


### Cash Flow Analysis

StockMCP evaluates:

- Operating cash flow
- Capital expenditures
- Free cash flow

#### Free Cash Flow

Formula:

Operating Cash Flow - Capital Expenditures

Positive and growing free cash flow is generally considered a sign of financial strength.


### Valuation Analysis

Evaluates how the market values a company relative to its fundamentals.

Metrics include:

- Price-to-Earnings (P/E)
- Price-to-Sales (P/S)
- Enterprise Value metrics

Valuation is considered together with business quality and financial strength.
A lower valuation does not always indicate a better investment opportunity, and a higher valuation may reflect stronger growth expectations.


### Financial Trends

StockMCP analyzes historical trends including:

- Revenue growth
- Gross margin trends
- Operating margin trends
- Net income trends
- Free cash flow trends

Trend analysis helps identify whether financial performance is improving, declining, or remaining stable.

## Financial Health Scoring

StockMCP evaluates companies using five major categories:

| Category | Purpose |
|---|---|
| Profitability | Measures earnings generation ability |
| Liquidity | Evaluates short-term financial strength |
| Leverage | Measures debt-related financial risk |
| Valuation | Compares market price with fundamentals |
| Financial Health | Evaluates overall balance sheet strength |

Scores are normalized to a 0-100 scale.

Example:

| Category | Score |
|---|---:|
| Overall Score | 90 |
| Profitability | 95 |
| Liquidity | 85 |
| Leverage | 90 |
| Valuation | 80 |
| Financial Health | 95 |


## Score Interpretation

Scores are normalized from 0 to 100:

| Score Range | Interpretation |
|---|---|
| 90-100 | Excellent |
| 80-89 | Strong |
| 70-79 | Good |
| 60-69 | Average |
| Below 60 | Weak |

Scores should be interpreted together with business conditions and valuation.

## Company Reports

StockMCP can generate comprehensive company reports combining:

- Company overview
- Financial trends
- Key ratios
- Valuation metrics
- Financial health assessment
- Risks and strengths

Example:

"Generate a complete company report for Costco"


## Company Comparison

StockMCP compare multiple companies:

Example:
Compare AAPL, MSFT, NVDA, GOOGL, AVGO

The analysis provides:

- Overall ranking
- Category scores
- Best-in-class metrics
- Strengths
- Risks


## Watchlist Screening

Watchlist screening applies the same financial framework across multiple companies.

Example:

"Find the strongest companies in my watchlist"

The result includes:

- Overall ranking
- Category scores
- Best-in-class companies
- Strengths
- Potential risks


## Why Trailing Twelve Months (TTM)?

Quarterly financial statements can be affected by seasonality.

StockMCP uses TTM calculations to provide a more consistent view:

TTM (Trailing Twelve Months) = Sum of the most recent four quarterly periods

Benefits:

- Reduces seasonal distortion
- Provides current annualized performance
- Enables more meaningful company comparison


## Important Notes

Financial scores are designed to support investment research.

They should not be considered investment advice.

Investors should consider:

- Business fundamentals
- Industry conditions
- Competitive position
- Future growth opportunities
- Market valuation