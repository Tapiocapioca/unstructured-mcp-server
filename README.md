# unstructured-mcp-server

FastMCP server for Unstructured.io document parsing.

## Overview

This MCP server provides tools for parsing documents (PDF, DOCX, TXT, logs, etc.) using Unstructured.io API. It connects Claude to document parsing capabilities via the Model Context Protocol.

## Prerequisites

- Python >= 3.10
- Unstructured API container running on localhost:9104

### Start the Unstructured API

```bash
docker run -d --name unstructured-api -p 9104:8000 \
  quay.io/unstructured-io/unstructured-api:latest
```

Or using docker-compose (recommended):

```bash
cd brainery-containers
docker-compose up -d unstructured-api
```

## Installation

### Via Smithery (Recommended)

```bash
npx -y @smithery/cli install @tapiocapioca/unstructured-mcp-server --client claude
```

This will:
- Install the package
- Configure Claude Desktop automatically
- Set up the MCP server

### Via pip (Manual)

```bash
pip install unstructured-mcp-server
```

Or with uv:

```bash
uv pip install unstructured-mcp-server
```

Then add to your MCP settings:

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

## Usage

### As MCP Server

```bash
unstructured-mcp
```

### Configuration

Set environment variables (optional):

```bash
export UNSTRUCTURED_API_URL=http://localhost:9104
```

## Tools

| Tool | Description |
|------|-------------|
| `parse_document` | Parse a single document (PDF, DOCX, TXT, logs) and extract text |
| `parse_batch` | Parse multiple documents in batch |

### parse_document

```python
parse_document(file_path: str, strategy: str = "auto")
```

**Parameters:**
- `file_path`: Absolute path to file on host machine
- `strategy`: Parsing strategy - `auto`, `fast`, `hi_res`, or `ocr_only` (default: `auto`)

**Returns:**
- `text`: Extracted text content
- `elements_count`: Number of document elements
- `file_type`: Detected file type
- `processing_time_ms`: Processing time in milliseconds

### parse_batch

```python
parse_batch(file_paths: list[str])
```

**Parameters:**
- `file_paths`: Array of absolute paths to files

**Returns:**
- List of results, one per file (success or error)

## Supported File Types

**Documents (via Unstructured API):**
- PDF, DOCX, PPTX, XLSX, ODT, RTF, EPUB

**Text Files (direct read):**
- `.txt`, `.log`, `.md`, `.csv`, `.json`, `.yaml`, `.yml`
- `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.sh`, `.bash`
- `.conf`, `.cfg`, `.ini`, `.properties`, `.env`, `.sql`
- `.xml`, `.html`, `.css`, `.gitignore`, `.htaccess`

## License

MIT
