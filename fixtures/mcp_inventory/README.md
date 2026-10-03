# Minimal MCP inventory fixture

The server announces resource support, initializes normally, and returns either
a healthy catalog, a genuinely empty catalog, or a valid JSON-RPC internal error.
No external network, model service, real database, or credential is required.

The normal workflow is discovering schema/document resources before a coding
task. `error` models a temporary backend failure. It does not issue adversarial
instructions or request unsafe actions.

```sh
python fixtures/mcp_inventory/server.py --mode error
```

