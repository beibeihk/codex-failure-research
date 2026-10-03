"""Synthetic, line-delimited JSON-RPC MCP server. No dependencies or secrets."""
import argparse
import json
from pathlib import Path
import sys


def response(request, mode):
    method = request.get("method")
    if "id" not in request:
        return None
    base = {"jsonrpc": "2.0", "id": request["id"]}
    if method == "initialize":
        result = {
            "protocolVersion": request.get("params", {}).get("protocolVersion", "2025-11-25"),
            "capabilities": {"resources": {}, "tools": {}},
            "serverInfo": {"name": "synthetic-inventory", "version": "1.0.0"},
        }
    elif method == "tools/list":
        result = {"tools": []}
    elif method in ("resources/list", "resources/templates/list"):
        if mode == "error":
            return {**base, "error": {"code": -32603, "message": "Synthetic inventory unavailable"}}
        if mode == "invalid":
            result = {"resources": "invalid", "resourceTemplates": "invalid"}
        elif mode == "empty":
            result = {"resources": []} if method == "resources/list" else {"resourceTemplates": []}
        elif method == "resources/list":
            result = {"resources": [{"uri": "research://public/schema", "name": "schema", "mimeType": "text/plain"}]}
        else:
            result = {"resourceTemplates": [{"uriTemplate": "research://public/{name}", "name": "schema-template"}]}
    elif method == "resources/read":
        result = {"contents": [{"uri": request["params"]["uri"], "text": "synthetic schema v1", "mimeType": "text/plain"}]}
    elif method == "ping":
        result = {}
    else:
        return {**base, "error": {"code": -32601, "message": "Method not found"}}
    return {**base, "result": result}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["healthy", "empty", "error", "invalid"], default="healthy")
    parser.add_argument("--trace-file", type=Path)
    args = parser.parse_args()
    for line in sys.stdin:
        try:
            request = json.loads(line)
            reply = response(request, args.mode)
            if args.trace_file:
                trace = {"method": request.get("method"), "mode": args.mode,
                         "error_code": (reply or {}).get("error", {}).get("code")}
                with args.trace_file.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(trace) + "\n")
            if reply is not None:
                print(json.dumps(reply), flush=True)
        except (ValueError, KeyError, TypeError):
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}), flush=True)


if __name__ == "__main__":
    main()

