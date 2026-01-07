"""Unstructured MCP Server using FastMCP."""
import os
from pathlib import Path
from typing import Literal
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("unstructured")

# Text file extensions that can be read directly
TEXT_EXTENSIONS = {
    '.txt', '.log', '.md', '.csv', '.json', '.yaml', '.yml',
    '.sh', '.bash', '.py', '.js', '.ts', '.java', '.c', '.cpp',
    '.conf', '.cfg', '.ini', '.properties', '.env', '.sql',
    '.gitignore', '.htaccess', '.xml', '.html', '.css'
}

@mcp.tool()
async def parse_document(
    file_path: str,
    strategy: Literal["auto", "fast", "hi_res", "ocr_only"] = "auto"
) -> dict:
    """
    Parse a local document and extract text.

    Supports PDF, DOCX, PPTX, XLSX, and text-based files (.txt, .log, .py, etc).

    Args:
        file_path: Absolute path to file on host machine
        strategy: Parsing strategy (auto, fast, hi_res, ocr_only)

    Returns:
        Dictionary with text, elements_count, file_type, and processing_time_ms
    """
    import time
    start_time = time.time()

    # Check file exists
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    # Check file size (50MB limit)
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > 50:
        return {"error": f"File too large: {size_mb:.2f}MB (max 50MB)"}

    # Get file extension
    ext = path.suffix.lower()

    # Text-based files: direct read
    if ext in TEXT_EXTENSIONS or not ext:
        try:
            text = path.read_text(encoding='utf-8')
            processing_time = int((time.time() - start_time) * 1000)
            return {
                "text": text,
                "elements_count": 1,
                "file_type": "text/plain",
                "processing_time_ms": processing_time
            }
        except UnicodeDecodeError:
            return {"error": f"Could not decode {file_path} as UTF-8 text"}

    # Unstructured.io parsing for documents
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            with open(file_path, 'rb') as f:
                files = {'files': (path.name, f, 'application/octet-stream')}
                data = {'strategy': strategy}

                response = await client.post(
                    'http://localhost:9104/general/v0/general',
                    files=files,
                    data=data
                )
                response.raise_for_status()

                elements = response.json()
                text = '\n\n'.join(e.get('text', '') for e in elements if e.get('text'))

                processing_time = int((time.time() - start_time) * 1000)

                return {
                    "text": text,
                    "elements_count": len(elements),
                    "file_type": elements[0].get('metadata', {}).get('filetype', 'unknown') if elements else 'unknown',
                    "pages": elements[0].get('metadata', {}).get('page_number') if elements else None,
                    "processing_time_ms": processing_time
                }

    except httpx.ConnectError:
        return {"error": "Unstructured API not reachable. Is the container running on port 9104?"}
    except httpx.HTTPStatusError as e:
        return {"error": f"Unstructured API error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": f"Parse failed: {str(e)}"}


@mcp.tool()
async def parse_batch(file_paths: list[str]) -> list[dict]:
    """
    Parse multiple documents in batch.

    Args:
        file_paths: List of absolute paths to files

    Returns:
        List of results, one per file (success or error)
    """
    results = []

    for file_path in file_paths:
        result = await parse_document(file_path, strategy="auto")
        results.append({
            "file": file_path,
            "success": "error" not in result,
            **result
        })

    return results


def create_server():
    """
    Create and return the FastMCP server instance.

    This function is used by Smithery for deployment.
    The tools are already registered on the global `mcp` instance.
    """
    return mcp


def main():
    """Entry point for the MCP server (standalone usage)."""
    mcp.run()


if __name__ == "__main__":
    main()
