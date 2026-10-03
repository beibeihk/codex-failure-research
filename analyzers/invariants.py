"""Score explicit inventory outcomes only after verifying the exercised path."""
import json


MODES = {
    "healthy_aggregate": {"probe": "healthy"},
    "empty_aggregate": {"probe": "empty"},
    "error_aggregate": {"probe": "error"},
    "error_named": {"probe": "error"},
    "mixed_aggregate": {"probe": "error", "healthy": "healthy"},
    "template_error_aggregate": {"probe": "error"},
    "template_error_named": {"probe": "error"},
    "invalid_aggregate": {"probe": "invalid"},
}


def _explicit_server_errors(catalog, unavailable):
    """Accept structured partial results, never incidental words in resource text."""
    if not isinstance(catalog, dict):
        return False
    errors = catalog.get("errors")
    if not isinstance(errors, dict):
        return False
    for server in unavailable:
        detail = errors.get(server)
        if isinstance(detail, str):
            if not detail.strip():
                return False
        elif isinstance(detail, dict):
            if not (detail.get("message") or detail.get("code")):
                return False
        else:
            return False
    return True


def score_inventory(row):
    condition = row.get("condition", "")
    modes = MODES.get(condition, {})
    templates = condition.startswith("template_")
    tool = "list_mcp_resource_templates" if templates else "list_mcp_resources"
    method = "resources/templates/list" if tool.endswith("templates") else "resources/list"
    named = condition.endswith("_named")
    traces = row.get("server_traces", {})
    items, outputs = row.get("mcp_items", []), row.get("tool_outputs", [])
    valid_execution = (bool(modes) and set(traces) == set(modes)
                       and row.get("exit_code") == 0 and row.get("tool_available") is True
                       and row.get("model_requests") == 2 and row.get("tool_calls") == 1
                       and len(items) == 1 and len(outputs) == 1 and isinstance(outputs[0], str))
    if valid_execution:
        item = items[0]
        valid_execution = (item.get("type") == "mcp_tool_call" and item.get("tool") == tool
                           and item.get("server") == ("probe" if named else "codex")
                           and item.get("arguments") == ({"server": "probe"} if named else {}))
        for name, mode in modes.items():
            trace = traces[name]
            methods = [t.get("method") for t in trace]
            inventory = [t for t in trace if t.get("method") == method]
            initialized = [t for t in trace if t.get("method") == "initialize"]
            valid_execution = valid_execution and (
                len(initialized) == 1 and initialized[0].get("error_code") is None
                and "notifications/initialized" in methods and len(inventory) == 1
                and methods.index("initialize") < methods.index("notifications/initialized") < methods.index(method)
                and all(t.get("mode") == mode for t in trace)
                and inventory[0].get("error_code") == (-32603 if mode == "error" else None))
    if not valid_execution:
        return {"execution_valid": False, "success": None, "failure_types": [], "attribution": "evaluation", "reason": "Fixture handshake/call evidence incomplete; exclude from failure denominator."}
    try:
        catalog = json.loads(outputs[0])
    except (ValueError, TypeError):
        catalog = None
    unavailable = {name for name, mode in modes.items() if mode in ("error", "invalid")}
    message = (item.get("error") or {}).get("message", "")
    # A failed item must identify this server and error in model-facing text too.
    failed = item.get("status") == "failed" and all(
        name in message and name in outputs[0]
        and (("-32603" in message and "-32603" in outputs[0]) if modes[name] == "error"
             else any(word in message.lower() and word in outputs[0].lower()
                      for word in ("invalid", "malformed", "deserializ")))
        for name in unavailable)
    disclosed = bool(unavailable) and (failed or _explicit_server_errors(catalog, unavailable))
    key, uri_key = ("resourceTemplates", "uriTemplate") if templates else ("resources", "uri")
    uri = "research://public/{name}" if templates else "research://public/schema"
    inventory = catalog.get(key) if isinstance(catalog, dict) else None
    healthy = {name for name, mode in modes.items() if mode == "healthy"}
    catalog_ok = isinstance(inventory, list) and all(
        any(isinstance(resource, dict) and resource.get("server") == name
            and resource.get(uri_key) == uri for resource in inventory) for name in healthy)
    if not unavailable and not healthy:
        catalog_ok = catalog_ok and inventory == []
    success = (disclosed and (not healthy or catalog_ok)) if unavailable else (
        catalog_ok and item.get("status") == "completed" and item.get("error") is None)
    return {"execution_valid": True, "success": bool(success), "failure_types": [] if success else ["F07", "F08"], "attribution": "harness", "reason": "Inventory outcome is explicit." if success else "Server failure absent from successful model-facing inventory."}

