# StockMCP

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![MCP](https://img.shields.io/badge/MCP-server-green)

StockMCP is an MCP (Model Context Protocol) server that allows AI assistants such as Claude Desktop and Cursor to retrieve real-time US stock market information through structured tools.

StockMCP provides stock prices, historical data, company information, market data, and financial news through MCP tools that can be used by Claude Desktop, Cursor, and other MCP-compatible AI clients.

## Architecture
```
                         ┌─────────────────────┐
                         │   AI Clients        │
                         │ Claude / Cursor     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     server.py       │
                         │  MCP Server Entry   │
                         │                     │
                         │  imports tools/*    │
                         └──────────┬──────────┘
                                    │
                                    ▼
              ┌────────────────────────────────────────┐
              │              tools/                    │
              │          MCP Tool Layer                │
              │                                        │
              │  stock.py       company.py             │
              │  financials.py  forecast.py            │
              │  market.py       news.py                │
              │                                        │
              │  @mcp.tool()                           │
              └──────────────────┬─────────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │             services/                  │
              │          Business Logic Layer           │
              │                                        │
              │  yahoo.py          market_data.py      │
              │  financial_data.py  financial_ttm.py   │
              │  forecast_data.py   sec_financial_data.py│
              │                                        │
              │  Data retrieval                        │
              │  Calculations                          │
              │  Financial analysis                     │
              └──────────────────┬─────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │ Yahoo    │ │ SEC      │ │ Other    │
             │ Finance  │ │ Company  │ │ Data     │
             │          │ │ Facts    │ │ Sources  │
             └──────────┘ └──────────┘ └──────────┘

StockMCP separates business logic (services/) from MCP tool interfaces (tools/), making the core functionality independently testable and reusable.
```

## Features
- Real-time stock prices
- Historical OHLCV data
- Company information
- Market capitalization
- Valuation metrics
- Financial news
- Market overview
- AI-ready MCP tools

## Available Tools
| Tool | Description |
|------|-------------|
| `balance_sheet` | Company balance sheet data |
| `cash_flow` | Company cash flow statement data |
| `company_info` | Returns general company information |
| `company_report` | Comprehensive company report |
| `financial_health_analysis` | Overall financial health analysis |
| `financial_ratios` | Key financial ratios |
| `get_forecast` | Get a forecast for a stock |
| `income_statement` | Company income statement data |
| `leverage_analysis` | Debt/leverage analysis |
| `liquidity_analysis` | Liquidity analysis |
| `market_status` | Current market status |
| `profitability_analysis()` | Profitability analysis |
| `stock_history` | Historical OHLCV (open/high/low/close/volume) price data |
| `stock_news` | Latest news for a given stock symbol |
| `stock_price` | Closing stock price for a given symbol |
| `valuation_analysis` | valuation_analysis |
| `valuation_ratios` | Valuation ratios |

## Supported AI Clients

| Client         | Supported |
|----------------|-----------|
| Claude Desktop | ✅        |
| Cursor         | ✅        |
| VS Code + MCP  | Planned   |
| Windsurf       | Planned   |

## Quick Start

### Requirements
- Python 3.11+

Dependencies:
- MCP
- yfinance

---

### Clone the Repository
```bash
git clone https://github.com/byronguo/StockMCP.git
cd StockMCP
```

### Create Virtual Environment
```bash
python -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run StockMCP Server
```bash
python server.py
```

### Claude Desktop Configuration
Add below configuration in claude_desktop_config.json
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\MCP_Claude"
      ]
    },
    "StockMCP": {
      "command": "C:\\Python314\\python.exe",
      "args": [
        "C:\\MCP_Claude\\StockMCP\\server.py"
      ]
    }
  }
  ...
}
```
Restart Claude Desktop.

### Test
![StockMCP Demo](images/StockMCP_Claude.png)

### Cursor Configuration
Add below configuration in mcp.json
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\MCP_Claude"
      ]
    }    
  },
  "StockMCP": {
    "command": "python",
    "args": [
      "C:\\MCP_Claude\\StockMCP\\server.py"
    ]
  }
}
```

## Roadmap
v0.1
- stock server

v0.2
- refactored architecture
- company
- market
- news

- [x] Stock price
- [x] Historical data
- [x] Company information
- [x] Market data
- [x] Stock news
- [x] Financial statements
- [x] Financial analysis
- [x] Financial forecast

Upcoming:
- [ ] Options chain
- [ ] Technical indicators
- [ ] AI stock analysis

## Adding a New Feature

When adding a new StockMCP feature, follow these four steps:

### 1. Implement the business logic in `services/`

Create or update a service module, for example:

```text
services/forecast_data.py
```

Implement the main business logic there:

```python
def get_company_forecast(
    symbol: str,
) -> dict[str, Any]:
    ...
```

The service layer handles data retrieval, calculations, transformations, and business logic.

### 2. Expose the feature as an MCP tool in `tools/`

Create an MCP tool wrapper:

```text
tools/forecast.py
```

Example:

```python
@mcp.tool()
def get_forecast(
    symbol: str,
) -> dict[str, Any]:
    """Get financial forecasts and analyst expectations."""

    return get_company_forecast(symbol)
```

The function decorated with `@mcp.tool()` is the function exposed to AI clients such as Claude.

### 3. Import the new tool module in `server.py`

Add the new tool module to the imports in `server.py`:

```python
from tools import (
    stock,
    company,
    market,
    news,
    financials,
    forecast,
)
```

This step is required to register the MCP tool.

> Important: If the new module is not imported by `server.py`, the `@mcp.tool()` decorator will not be executed and the tool will not be available to MCP clients.

### 4. Add a test in `tests/`

Add a test for the service function:

```python
def test_company_forecast():

    print("\n=== Company forecast ===")

    print(
        get_company_forecast(SYMBOL)
    )
```

Then run the test to verify the feature before testing it through an MCP client.

### Development Flow

```
example:
┌──────────────────────────┐
│ 1. services/             │
│                          │
│ Implement business logic │
│ get_company_forecast()   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ 2. tools/                │
│                          │
│ Expose MCP tool          │
│ get_forecast()           │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ 3. server.py             │
│                          │
│ Import new tool module   │
│ Register MCP tool        │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ 4. tests/                │
│                          │
│ Test service function    │
│ Verify results           │
└──────────────────────────┘
```

## Topics
`mcp` `claude` `cursor` `stock` `finance` `ai` `python` `yfinance`