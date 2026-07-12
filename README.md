# StockMCP

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![MCP](https://img.shields.io/badge/MCP-server-green)

StockMCP is an MCP (Model Context Protocol) server that allows AI assistants such as Claude Desktop and Cursor to retrieve real-time US stock market information through structured tools.

StockMCP provides stock prices, company information, valuation metrics, financial statements, and news through MCP tools that can be used by Claude Desktop, Cursor, and other MCP-compatible AI clients.

```
Claude Desktop
        │
        │ MCP
        ▼
+------------------+
|   StockMCP       |
|------------------|
| stock_price()    |
| company_info()   |
| financials()     |
+------------------+
        │
        ▼
    Yahoo Finance
```

## Features
- Real-time stock price
- Company information
- Market capitalization
- P/E Ratio
- P/S Ratio
- Financial statements
- Option Chain
- Stock news
- AI-ready MCP tools

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
```json
{
  "mcpServers": {
    "stock": {
      "command": "python",
      "args": [
        "C:\\MCP_Claude\\StockMCP\\server.py"
      ]
    }
  }
}
```
Restart Claude Desktop.

### Test
![StockMCP Demo](images/StockMCP_Claude.png)

### Cursor Configuration
Same configuration as Claude Desktop.

## Available Tools
- `stock_price()`
- `company_info()`
- `market_cap()`
- `pe_ratio()`
- `ps_ratio()`
- `financials()`
- `option_chain()`
- `news()`

## Roadmap
- [ ] v0.1 — Stock price
- [ ] v0.2 — Company Information
- [ ] v0.3 — Financial Statements
- [ ] v0.4 — Options
- [ ] v1.0 — AI Stock Analysis

## Topics
`mcp` `claude` `cursor` `stock` `finance` `ai` `python` `yfinance`