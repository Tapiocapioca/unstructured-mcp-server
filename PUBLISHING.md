# Publishing to Smithery

This guide explains how to publish unstructured-mcp-server to [Smithery Registry](https://smithery.ai).

## Prerequisites

1. **GitHub Account**: Repository must be public on GitHub
2. **Smithery Account**: Create at https://smithery.ai

## Configuration Files

The repository is already configured with:

- `smithery.yaml` - Smithery runtime configuration
- `pyproject.toml` - Contains `[tool.smithery]` section pointing to server function
- `src/unstructured_mcp/server.py` - Has `create_server()` function

## Publishing Steps

### 1. Push to GitHub

Ensure all changes are committed and pushed:

```bash
git add smithery.yaml pyproject.toml src/unstructured_mcp/server.py README.md
git commit -m "feat: add Smithery Registry support"
git push origin main
```

### 2. Claim Server on Smithery

1. Go to https://smithery.ai
2. Sign in with GitHub
3. Navigate to your profile
4. Click "Claim Server" or "Add Server"
5. Select the `unstructured-mcp-server` repository

### 3. Deploy

1. Go to your server page on Smithery
2. Navigate to the "Deployments" tab
3. Click "Deploy"
4. Wait for build to complete

Smithery will automatically:
- Clone your repository
- Detect Python runtime from `smithery.yaml`
- Install dependencies from `pyproject.toml`
- Load `create_server()` function from `[tool.smithery]` config
- Package into a containerized HTTP service
- Deploy to hosting infrastructure

### 4. Verify

After deployment, verify by checking:
- Server page shows tools (`parse_document`, `parse_batch`)
- Installation command works

## Installation URL

After publishing, users can install with:

```bash
npx -y @smithery/cli install @tapiocapioca/unstructured-mcp-server --client claude
```

## Registry Page

View at: https://smithery.ai/server/@tapiocapioca/unstructured-mcp-server

## Updating

To publish a new version:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Commit and push:
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to 0.2.0"
   git push origin main
   ```

3. Go to Smithery and redeploy

## Troubleshooting

### Common Issues

**"Missing server configuration"**
- Ensure `pyproject.toml` has `[tool.smithery]` section
- Verify path matches: `unstructured_mcp.server:create_server`

**"Import errors"**
- Check all dependencies are in `dependencies` array
- Verify `fastmcp>=2.0.0` and `smithery>=0.4.2` are listed

**"Server doesn't start"**
- Test locally first: `python -m unstructured_mcp`
- Check `create_server()` returns a FastMCP instance

### Local Testing

Test server creation function:

```python
from unstructured_mcp.server import create_server
server = create_server()
print(server)  # Should print FastMCP instance
```

## Notes

- Smithery hosts the server as HTTP, not stdio
- The Unstructured API container must be running for document parsing
- For Smithery deployment, users will need their own Unstructured API endpoint
