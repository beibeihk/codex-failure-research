"""Run the actual Codex binary against a local scripted Responses endpoint.

This isolates software/tool behavior, not model reliability. Full requests and
headers are never recorded. CODEX_HOME and credential stores are never changed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import threading
import tempfile
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]


def sse(events):
    return "".join("event: " + e["type"] + "\ndata: " + json.dumps(e) + "\n\n" for e in events).encode()


def complete(index):
    return {"type": "response.completed", "response": {"id": f"fixture-response-{index}", "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}}}


def scripted_call(name, arguments):
    return {"type": "response.output_item.done", "item": {"type": "function_call", "call_id": "inventory-call", "name": name, "arguments": json.dumps(arguments)}}


class ReplayServer(ThreadingHTTPServer):
    def __init__(self, tool, arguments):
        super().__init__(("127.0.0.1", 0), Handler)
        self.tool = tool
        self.arguments = arguments
        self.request_count = 0
        self.tool_outputs = []
        self.tool_names = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"data": [], "models": []}')

    def do_POST(self):
        # Only transient in-memory parsing; never record instructions, headers,
        # authorization, account IDs, or conversation bodies.
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        if self.headers.get("Content-Encoding") == "zstd":
            import zstandard
            raw = zstandard.ZstdDecompressor().decompress(raw)
        body = json.loads(raw)
        self.server.request_count += 1
        index = self.server.request_count
        if index == 1:
            self.server.tool_names = [t.get("name", "") for t in body.get("tools", [])]
        for item in body.get("input", []):
            if item.get("type") in ("function_call_output", "custom_tool_call_output") and item.get("call_id") == "inventory-call":
                output = item.get("output")
                if output not in self.server.tool_outputs:
                    self.server.tool_outputs.append(output)
        if index == 1:
            events = [scripted_call(self.server.tool, self.server.arguments), complete(index)]
        else:
            events = [{"type": "response.output_item.done", "item": {"type": "message", "id": "fixture-final", "role": "assistant", "content": [{"type": "output_text", "text": "Synthetic protocol replay complete."}]}}, complete(index)]
        data = sse(events)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def config_args(server_url, modes, trace_dir=None):
    values = {
        "model_provider": "fixture",
        "model_providers.fixture.name": "Synthetic protocol replay",
        "model_providers.fixture.base_url": server_url + "/v1",
        "model_providers.fixture.wire_api": "responses",
        "model_providers.fixture.requires_openai_auth": False,
        "model_providers.fixture.supports_websockets": False,
        "project_doc_max_bytes": 0,
        "approval_policy": "never",
        "features.code_mode": False,
        "features.apps": False,
        "web_search": "disabled",
        "analytics.enabled": False,
    }
    for name, mode in modes.items():
        values[f"mcp_servers.{name}.command"] = sys.executable
        values[f"mcp_servers.{name}.args"] = [str(ROOT / "fixtures/mcp_inventory/server.py"), "--mode", mode]
        if trace_dir:
            values[f"mcp_servers.{name}.args"] += ["--trace-file", str(Path(trace_dir) / (name + ".jsonl"))]
        values[f"mcp_servers.{name}.startup_timeout_sec"] = 10
        values[f"mcp_servers.{name}.tool_timeout_sec"] = 3
    args = []
    for key, value in values.items():
        args.extend(["-c", key + "=" + json.dumps(value)])
    return args


CONDITIONS = {
    "healthy_aggregate": ({"probe": "healthy"}, "list_mcp_resources", {}),
    "empty_aggregate": ({"probe": "empty"}, "list_mcp_resources", {}),
    "error_aggregate": ({"probe": "error"}, "list_mcp_resources", {}),
    "error_named": ({"probe": "error"}, "list_mcp_resources", {"server": "probe"}),
    "mixed_aggregate": ({"probe": "error", "healthy": "healthy"}, "list_mcp_resources", {}),
    "template_error_aggregate": ({"probe": "error"}, "list_mcp_resource_templates", {}),
    "template_error_named": ({"probe": "error"}, "list_mcp_resource_templates", {"server": "probe"}),
    "invalid_aggregate": ({"probe": "invalid"}, "list_mcp_resources", {}),
}


def run(binary, condition, repetition=1, timeout=45):
    modes, tool, arguments = CONDITIONS[condition]
    server = ReplayServer(tool, arguments)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    trace_dir = tempfile.TemporaryDirectory(prefix="codex-research-fixture-")
    cmd = [str(binary), "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral", "--skip-git-repo-check", "--json", "-s", "read-only", "-m", "gpt-5.2"]
    cmd += config_args(url, modes, trace_dir.name)
    cmd += ["Discover the synthetic schema/document resources available through MCP. Do not edit files or run shell commands."]
    started = time.monotonic()
    # Do not change CODEX_HOME, copy auth, or write persistent config.
    try:
        proc = subprocess.run(cmd, cwd=ROOT / "fixtures/mcp_inventory", capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        events = []
        for line in proc.stdout.splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
        items = [e["item"] for e in events if "item" in e and e["item"].get("type") == "mcp_tool_call"]
        # Export only the fixture tool's data, never arbitrary session output.
        items = [i for i in items if i.get("tool") == tool]
        completed = [i for i in items if i.get("status") != "in_progress"]
        result = {
            "run_id": f"{binary.parent.name}-{condition}-{repetition}",
            "scenario": "mcp-inventory-error-visibility",
            "condition": condition,
            "repetition": repetition,
            "codex_version": subprocess.check_output([str(binary), "--version"], text=True).strip(),
            "platform": platform.system() + " " + platform.version() + " " + platform.machine(),
            "harness_version": "0.1.0",
            "fixture_version": "1.0.0",
            "scenario_version": "1.0.0",
            "model": "scripted Responses fixture (model slug gpt-5.2; no inference)",
            "duration_seconds": round(time.monotonic() - started, 3),
            "exit_code": proc.returncode,
            "model_requests": server.request_count,
            "tool_outputs": server.tool_outputs,
            "mcp_items": completed,
            "tool_available": tool in server.tool_names,
            "tool_calls": len(completed),
            "server_traces": {name: [json.loads(line) for line in (Path(trace_dir.name) / (name + ".jsonl")).read_text(encoding="utf-8").splitlines()] if (Path(trace_dir.name) / (name + ".jsonl")).exists() else [] for name in modes},
            "stderr_inventory_warning": "Failed to list resources" in proc.stderr or "Failed to list resource templates" in proc.stderr,
            "diagnostic": "No full stderr retained; rerun locally for installation diagnostics.",
        }
        if not result["tool_outputs"] and not completed:
            # Arbitrary startup stderr may contain personal paths or secrets.
            print("Fixture execution incomplete; inspect local installation and rerun. No raw stderr exported.", file=sys.stderr)
        return result
    finally:
        server.shutdown()
        server.server_close()
        trace_dir.cleanup()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex", type=Path, required=True)
    parser.add_argument("--condition", choices=list(CONDITIONS), default="error_aggregate")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--output", type=Path, default=ROOT / ".cache/pilot.jsonl")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for i in range(1, args.repetitions + 1):
        row = run(args.codex.resolve(), args.condition, i)
        with args.output.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(json.dumps(row, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
