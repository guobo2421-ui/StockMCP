# Development Guide
This guide explains the architecture of StockMCP and how to add new MCP tools and services.

StockMCP follows a layered architecture that separates MCP tool definitions from business logic, making the codebase modular, testable, and easy to extend.


## Project Structure

```text
StockMCP/
├── server.py
├── tools/
├── services/
├── tests/
├── images/
├── docs/
├── requirements.txt
└── README.md
```


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
              │  market.py       news.py               │
              │                                        │
              │  @mcp.tool()                           │
              └──────────────────┬─────────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────────┐
              │             services/                    │
              │          Business Logic Layer            │
              │                                          │
              │  yahoo.py           market_data.py       │
              │  financial_data.py  financial_ttm.py     │
              │  forecast_data.py   sec_financial_data.py│
              │                                          │
              │  Data retrieval                          │
              │  Calculations                            │
              │  Financial analysis                      │
              └──────────────────┬───────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │ Yahoo    │ │ SEC      │ │ Other    │
             │ Finance  │ │ Company  │ │ API      │
             │          │ │ Facts    │ │          │
             └──────────┘ └──────────┘ └──────────┘

The architecture separates MCP tool definitions from the underlying business logic. This layered design makes individual service modules easier to test, reuse, and extend while keeping the MCP interface lightweight.
```


## Development Guide

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
def company_forecast(
    symbol: str,
) -> dict[str, Any]:
    """Get financial forecasts and analyst expectations."""

    return get_company_forecast(symbol)
```

Functions decorated with `@mcp.tool()` become MCP tools that are exposed to AI clients such as Claude Desktop and Cursor.

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
> **Important**
>
> Every MCP tool module must be imported by `server.py`.
> Otherwise the `@mcp.tool()` decorator will never execute,
> and the tool will not be registered with the MCP server.

### 4. Add a test in `tests/`

Add a test for the service function:

```python
def test_company_forecast():

    print("\n=== Company forecast ===")

    print(
        get_company_forecast(SYMBOL)
    )
```

Run the unit test to verify the service logic before testing the tool through an MCP client such as Claude Desktop or Cursor.

This development workflow makes it easier to isolate issues in the service layer before debugging MCP integration.


## Development Flow

```
┌──────────────────────────────┐
│ 1. services/forecast_data.py │
│                              │
│ Implement business logic     │
│ get_company_forecast()       │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────┐
│ 2. tools/forecast.py     │
│                          │
│ Expose MCP tool          │
│ company_forecast()       │
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

## Design Principles
The following principles help keep StockMCP consistent as new features are added.

When adding new features:

- Keep business logic inside `services/`.
- Keep MCP tools as lightweight wrappers.
- Reuse existing service modules whenever possible.
- Return structured data instead of formatted text.
- Write tests for new service functions.






