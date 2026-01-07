# unstructured-mcp-server

FastMCP server for Unstructured.io document parsing.

## Overview

This MCP server provides tools for parsing documents (PDF, DOCX, TXT, logs, etc.) using Unstructured.io API. It connects Claude to document parsing capabilities via the Model Context Protocol.

## Requirements

- Python >= 3.10
- Unstructured API running (via Docker or cloud)

## Installation

```bash
pip install unstructured-mcp-server
```

Or with uv:

```bash
uv pip install unstructured-mcp-server
```

## Usage

### As MCP Server

```bash
unstructured-mcp
```

### Configuration

Set environment variables:

```bash
export UNSTRUCTURED_API_URL=http://localhost:9104
```

## Tools

| Tool | Description |
|------|-------------|
| `parse_document` | Parse a single document (PDF, DOCX, TXT, logs) |
| `parse_batch` | Parse multiple documents in batch |

## Example Claude Code Configuration

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "unstructured": {
      "command": "unstructured-mcp",
      "env": {
        "UNSTRUCTURED_API_URL": "http://localhost:9104"
      }
    }
  }
}
```

## License

MIT
