#!/usr/bin/env python3
import argparse
import json
import os
import time
import mimetypes
import uuid
import urllib.parse
import urllib.request
import urllib.error

CONFIG_PATH = os.path.expanduser("~/.openclaw/zoho-books/config.json")

DC_MAP = {
    "EU": {
        "api": "https://www.zohoapis.eu/books/v3",
        "accounts": "https://accounts.zoho.eu/oauth/v2",
    },
    "US": {
        "api": "https://www.zohoapis.com/books/v3",
        "accounts": "https://accounts.zoho.com/oauth/v2",
    },
    "IN": {
        "api": "https://www.zohoapis.in/books/v3",
        "accounts": "https://accounts.zoho.in/oauth/v2",
    },
    "AU": {
        "api": "https://www.zohoapis.com.au/books/v3",
        "accounts": "https://accounts.zoho.com.au/oauth/v2",
    },
    "JP": {
        "api": "https://www.zohoapis.jp/books/v3",
        "accounts": "https://accounts.zoho.jp/oauth/v2",
    },
}

DEFAULT_SCOPE = "ZohoBooks.fullaccess.all"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def get_dc(cfg, override=None):
    dc = (override or cfg.get("datacenter") or "EU").upper()
    if dc not in DC_MAP:
        raise SystemExit(f"Unsupported datacenter: {dc}")
    return dc, DC_MAP[dc]


def build_auth_url(cfg, dc, scopes, redirect_uri, state=None):
    base = DC_MAP[dc]["accounts"]
    params = {
        "scope": scopes,
        "client_id": cfg.get("client_id", ""),
        "response_type": "code",
        "access_type": "offline",
        "redirect_uri": redirect_uri,
        "prompt": "consent",
    }
    if state:
        params["state"] = state
    return f"{base}/auth?{urllib.parse.urlencode(params)}"


def http_post(url, data, headers=None):
    headers = headers or {}
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def refresh_token(cfg, dc_info):
    if "refresh_token" not in cfg:
        raise SystemExit("Missing refresh_token in config")
    data = {
        "refresh_token": cfg["refresh_token"],
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "grant_type": "refresh_token",
    }
    url = f"{dc_info['accounts']}/token"
    raw = http_post(url, data)
    return json.loads(raw)


def get_access_token(cfg, dc_info):
    token = cfg.get("access_token")
    expires_at = cfg.get("access_token_expires_at")
    now = int(time.time())
    if token and expires_at and now < int(expires_at) - 60:
        return token
    resp = refresh_token(cfg, dc_info)
    token = resp.get("access_token")
    if not token:
        raise SystemExit("Failed to refresh access token")
    expires_in = int(resp.get("expires_in", 3600))
    cfg["access_token"] = token
    cfg["access_token_expires_at"] = now + expires_in
    save_config(cfg)
    return token


def build_multipart(fields, files):
    boundary = f"----OpenClawBoundary{uuid.uuid4().hex}"
    lines = []

    for name, value in fields.items():
        lines.append(f"--{boundary}")
        lines.append(f"Content-Disposition: form-data; name=\"{name}\"")
        lines.append("")
        lines.append(str(value))

    for name, path in files.items():
        filename = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = f.read()
        lines.append(f"--{boundary}")
        lines.append(
            f"Content-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\""
        )
        lines.append(f"Content-Type: {ctype}")
        lines.append("")
        lines.append(data)

    lines.append(f"--{boundary}--")

    body = b""
    for part in lines:
        if isinstance(part, bytes):
            body += part + b"\r\n"
        else:
            body += str(part).encode("utf-8") + b"\r\n"

    return body, boundary


def api_request(cfg, dc_info, method, path, query=None, body=None, files=None, require_org=True):
    token = get_access_token(cfg, dc_info)
    org_id = cfg.get("organization_id")
    if require_org and not org_id:
        raise SystemExit("Missing organization_id in config")

    query = query or {}
    if require_org:
        query["organization_id"] = org_id
    url = f"{dc_info['api']}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"

    data = None
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}

    if files:
        fields = {}
        if body:
            fields.update(body)
        data, boundary = build_multipart(fields, files)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    elif body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise SystemExit(body)


def api_request_raw(cfg, dc_info, method, path, query=None, body=None, files=None, require_org=True):
    token = get_access_token(cfg, dc_info)
    org_id = cfg.get("organization_id")
    if require_org and not org_id:
        raise SystemExit("Missing organization_id in config")

    query = query or {}
    if require_org:
        query["organization_id"] = org_id
    url = f"{dc_info['api']}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"

    data = None
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}

    if files:
        fields = {}
        if body:
            fields.update(body)
        data, boundary = build_multipart(fields, files)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    elif body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise SystemExit(body)


def load_json_arg(value):
    if value is None:
        return None
    value = value.strip()
    if value.startswith("@"):
        path = value[1:]
        with open(path, "r") as f:
            return json.load(f)
    return json.loads(value)


def build_path(template, args):
    return template.format(**args.__dict__)


def cmd_orgs_list(cfg, dc_info):
    resp = api_request(cfg, dc_info, "GET", "/organizations", require_org=False)
    print(resp)


def cmd_orgs_select(cfg, org_id):
    cfg["organization_id"] = org_id
    save_config(cfg)
    print(f"Selected organization_id: {org_id}")


def cmd_contacts_upsert(cfg, dc_info, name, contact_type):
    resp = api_request(cfg, dc_info, "GET", "/contacts", query={"search_text": name})
    data = json.loads(resp)
    for c in data.get("contacts", []):
        if c.get("contact_name") == name and c.get("contact_type") == contact_type:
            print(json.dumps({"action": "exists", "contact": c}, indent=2))
            return
    resp = api_request(
        cfg,
        dc_info,
        "POST",
        "/contacts",
        body={"contact_name": name, "contact_type": contact_type},
    )
    print(resp)


def cmd_expenses_create(cfg, dc_info, body, receipt=None, attachment=None):
    resp = api_request(cfg, dc_info, "POST", "/expenses", body=body)
    print(resp)

    if receipt or attachment:
        data = json.loads(resp)
        expense_id = data.get("expense", {}).get("expense_id")
        if not expense_id:
            raise SystemExit("Expense created but expense_id not found in response")
        if receipt:
            api_request(
                cfg,
                dc_info,
                "POST",
                f"/expenses/{expense_id}/receipt",
                files={"receipt": receipt},
            )
        if attachment:
            api_request(
                cfg,
                dc_info,
                "POST",
                f"/expenses/{expense_id}/attachment",
                files={"attachment": attachment},
            )
        print(json.dumps({"expense_id": expense_id, "receipt": bool(receipt), "attachment": bool(attachment)}))


def cmd_invoices_email(cfg, dc_info, invoice_id, body=None):
    resp = api_request(cfg, dc_info, "POST", f"/invoices/{invoice_id}/email", body=body or {})
    print(resp)


def cmd_banktransactions_match(cfg, dc_info, transaction_id, body):
    resp = api_request(
        cfg,
        dc_info,
        "POST",
        f"/banktransactions/uncategorized/{transaction_id}/match",
        body=body,
    )
    print(resp)


def cmd_banktransactions_uncategorized_matches(cfg, dc_info, transaction_id):
    resp = api_request(
        cfg,
        dc_info,
        "GET",
        f"/banktransactions/uncategorized/{transaction_id}/match",
    )
    print(resp)


def handle_api_command(cfg, dc_info, args):
    path = build_path(args._path, args)
    query = load_json_arg(args.query) if getattr(args, "query", None) else {}
    body = load_json_arg(args.body) if getattr(args, "body", None) else None
    resp = api_request(cfg, dc_info, args._method, path, query=query, body=body)
    print(resp)


def add_resource_commands(sub, name, base_path, actions=None, skip=None):
    skip = set(skip or [])
    actions = actions or []

    if "list" not in skip:
        s = sub.add_parser(f"{name}-list", help=f"List {name}")
        s.add_argument("--dc", default=None)
        s.add_argument("--query", default=None, help="JSON object (or @file.json)")
        s.set_defaults(_method="GET", _path=base_path, _handler=handle_api_command)

    if "get" not in skip:
        s = sub.add_parser(f"{name}-get", help=f"Get {name} by id")
        s.add_argument("--dc", default=None)
        s.add_argument("--id", required=True)
        s.add_argument("--query", default=None, help="JSON object (or @file.json)")
        s.set_defaults(_method="GET", _path=f"{base_path}/{{id}}", _handler=handle_api_command)

    if "create" not in skip:
        s = sub.add_parser(f"{name}-create", help=f"Create {name}")
        s.add_argument("--dc", default=None)
        s.add_argument("--body", required=True, help="JSON object (or @file.json)")
        s.set_defaults(_method="POST", _path=base_path, _handler=handle_api_command)

    if "update" not in skip:
        s = sub.add_parser(f"{name}-update", help=f"Update {name}")
        s.add_argument("--dc", default=None)
        s.add_argument("--id", required=True)
        s.add_argument("--body", required=True, help="JSON object (or @file.json)")
        s.set_defaults(_method="PUT", _path=f"{base_path}/{{id}}", _handler=handle_api_command)

    if "delete" not in skip:
        s = sub.add_parser(f"{name}-delete", help=f"Delete {name}")
        s.add_argument("--dc", default=None)
        s.add_argument("--id", required=True)
        s.set_defaults(_method="DELETE", _path=f"{base_path}/{{id}}", _handler=handle_api_command)

    for action in actions:
        s = sub.add_parser(f"{name}-{action['name']}", help=action.get("help", ""))
        s.add_argument("--dc", default=None)
        if action.get("needs_id", True):
            s.add_argument("--id", required=True)
        if action.get("query", False):
            s.add_argument("--query", default=None, help="JSON object (or @file.json)")
        if action.get("body", False):
            s.add_argument("--body", default=None, help="JSON object (or @file.json)")
        s.set_defaults(_method=action["method"], _path=action["path"], _handler=handle_api_command)


def add_tasks_commands(sub):
    base = "/projects/{project_id}/tasks"
    s = sub.add_parser("tasks-list", help="List tasks for a project")
    s.add_argument("--dc", default=None)
    s.add_argument("--project-id", required=True)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.set_defaults(_method="GET", _path=base, _handler=handle_api_command)

    s = sub.add_parser("tasks-get", help="Get task")
    s.add_argument("--dc", default=None)
    s.add_argument("--project-id", required=True)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path=f"{base}/{{id}}", _handler=handle_api_command)

    s = sub.add_parser("tasks-create", help="Create task")
    s.add_argument("--dc", default=None)
    s.add_argument("--project-id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path=base, _handler=handle_api_command)

    s = sub.add_parser("tasks-update", help="Update task")
    s.add_argument("--dc", default=None)
    s.add_argument("--project-id", required=True)
    s.add_argument("--id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="PUT", _path=f"{base}/{{id}}", _handler=handle_api_command)

    s = sub.add_parser("tasks-delete", help="Delete task")
    s.add_argument("--dc", default=None)
    s.add_argument("--project-id", required=True)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="DELETE", _path=f"{base}/{{id}}", _handler=handle_api_command)


def add_timeentry_commands(sub):
    base = "/projects/timeentries"
    add_resource_commands(sub, "timeentries", base)

    s = sub.add_parser("timeentries-timer-start", help="Start time entry timer")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="POST", _path="/projects/timeentries/{id}/timer/start", _handler=handle_api_command)

    s = sub.add_parser("timeentries-timer-stop", help="Stop running timer")
    s.add_argument("--dc", default=None)
    s.add_argument("--body", default=None, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path="/projects/timeentries/timer/stop", _handler=handle_api_command)

    s = sub.add_parser("timeentries-timer-running", help="Get running timer for me")
    s.add_argument("--dc", default=None)
    s.set_defaults(_method="GET", _path="/projects/timeentries/runningtimer/me", _handler=handle_api_command)


def cmd_upload(cfg, dc_info, path, file_path, field="attachment", body=None):
    body = load_json_arg(body) if isinstance(body, str) else body
    resp = api_request(cfg, dc_info, "POST", path, body=body, files={field: file_path})
    print(resp)


def cmd_download(cfg, dc_info, path, out_path, query=None):
    query = load_json_arg(query) if isinstance(query, str) and query else (query or {})
    data = api_request_raw(cfg, dc_info, "GET", path, query=query)
    with open(out_path, "wb") as f:
        f.write(data)
    print(json.dumps({"saved": out_path, "bytes": len(data)}))


def add_comments_commands(sub, prefix, base_path):
    s = sub.add_parser(f"{prefix}-comments-list", help=f"List {prefix} comments")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path=base_path, _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-comments-add", help=f"Add {prefix} comment")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path=base_path, _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-comments-delete", help=f"Delete {prefix} comment")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--comment-id", required=True)
    s.set_defaults(_method="DELETE", _path=base_path + "/{comment_id}", _handler=handle_api_command)


def add_attachment_command(sub, prefix, path_template):
    s = sub.add_parser(f"{prefix}-attach", help=f"Attach file to {prefix}")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--file", required=True)
    s.add_argument("--field", default="attachment")
    s.add_argument("--body", default=None, help="JSON object (or @file.json)")
    s.set_defaults(_handler="_upload", _path=path_template)


def add_templates_commands(sub, prefix, base):
    s = sub.add_parser(f"{prefix}-templates-list", help=f"List {prefix} templates")
    s.add_argument("--dc", default=None)
    s.set_defaults(_method="GET", _path=f"/{base}/templates", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-template-apply", help=f"Apply {prefix} template")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--template-id", required=True)
    s.set_defaults(_method="PUT", _path=f"/{base}/{{id}}/templates/{{template_id}}", _handler=handle_api_command)


def add_payments_commands(sub, prefix, base):
    s = sub.add_parser(f"{prefix}-payments-list", help=f"List {prefix} payments")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path=f"/{base}/{{id}}/payments", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-payments-add", help=f"Add {prefix} payment")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path=f"/{base}/{{id}}/payments", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-payments-get", help=f"Get {prefix} payment")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--payment-id", required=True)
    s.set_defaults(_method="GET", _path=f"/{base}/{{id}}/payments/{{payment_id}}", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-payments-delete", help=f"Delete {prefix} payment")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--payment-id", required=True)
    s.set_defaults(_method="DELETE", _path=f"/{base}/{{id}}/payments/{{payment_id}}", _handler=handle_api_command)


def add_refunds_commands(sub, prefix, base, refund_param="refund_id"):
    s = sub.add_parser(f"{prefix}-refunds-list", help=f"List {prefix} refunds")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path=f"/{base}/{{id}}/refunds", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-refunds-add", help=f"Add {prefix} refund")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path=f"/{base}/{{id}}/refunds", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-refunds-get", help=f"Get {prefix} refund")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument(f"--{refund_param.replace('_','-')}", required=True)
    s.set_defaults(_method="GET", _path=f"/{base}/{{id}}/refunds/{{{refund_param}}}", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-refunds-update", help=f"Update {prefix} refund")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument(f"--{refund_param.replace('_','-')}", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="PUT", _path=f"/{base}/{{id}}/refunds/{{{refund_param}}}", _handler=handle_api_command)

    s = sub.add_parser(f"{prefix}-refunds-delete", help=f"Delete {prefix} refund")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.add_argument(f"--{refund_param.replace('_','-')}", required=True)
    s.set_defaults(_method="DELETE", _path=f"/{base}/{{id}}/refunds/{{{refund_param}}}", _handler=handle_api_command)


def add_custom_modules_commands(sub):
    s = sub.add_parser("custommodules-list", help="List records for a custom module")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.set_defaults(_method="GET", _path="/{module}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-create", help="Create record in a custom module")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="POST", _path="/{module}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-bulk-update", help="Bulk update custom module records")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="PUT", _path="/{module}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-delete", help="Delete custom module")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.set_defaults(_method="DELETE", _path="/{module}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-get", help="Get custom module record")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path="/{module}/{id}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-update", help="Update custom module record")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.set_defaults(_method="PUT", _path="/{module}/{id}", _handler=handle_api_command)

    s = sub.add_parser("custommodules-delete-record", help="Delete custom module record")
    s.add_argument("--dc", default=None)
    s.add_argument("--module", required=True)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="DELETE", _path="/{module}/{id}", _handler=handle_api_command)


def main():
    p = argparse.ArgumentParser(description="Zoho Books CLI helper")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("init", help="Create config template")
    s.add_argument("--dc", default="EU")

    s = sub.add_parser("auth-url", help="Generate OAuth consent URL")
    s.add_argument("--dc", default=None)
    s.add_argument("--scopes", default=DEFAULT_SCOPE)
    s.add_argument("--redirect-uri", required=True)
    s.add_argument("--state", default=None)

    s = sub.add_parser("exchange-code", help="Exchange code for refresh token")
    s.add_argument("--dc", default=None)
    s.add_argument("--code", required=True)
    s.add_argument("--redirect-uri", required=True)

    s = sub.add_parser("refresh", help="Refresh access token")
    s.add_argument("--dc", default=None)

    
    s = sub.add_parser("upload", help="Upload file (multipart) to a path")
    s.add_argument("--dc", default=None)
    s.add_argument("--path", required=True)
    s.add_argument("--file", required=True)
    s.add_argument("--field", default="attachment")
    s.add_argument("--body", default=None, help="JSON object (or @file.json)")

    s = sub.add_parser("download", help="Download raw response to file")
    s.add_argument("--dc", default=None)
    s.add_argument("--path", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")

    s = sub.add_parser("request", help="Make API request")
    s.add_argument("--dc", default=None)
    s.add_argument("--method", required=True)
    s.add_argument("--path", required=True)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--body", default=None, help="JSON object (or @file.json)")

    s = sub.add_parser("orgs-list", help="List organizations")
    s.add_argument("--dc", default=None)

    s = sub.add_parser("orgs-select", help="Select organization")
    s.add_argument("--id", required=True)

    s = sub.add_parser("contacts-upsert", help="Create contact only if missing")
    s.add_argument("--dc", default=None)
    s.add_argument("--name", required=True)
    s.add_argument("--type", required=True, choices=["customer", "vendor"])

    s = sub.add_parser("expenses-create", help="Create expense (optionally attach receipt/attachment)")
    s.add_argument("--dc", default=None)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")
    s.add_argument("--receipt", default=None)
    s.add_argument("--attachment", default=None)

    s = sub.add_parser("invoices-email", help="Email invoice")
    s.add_argument("--dc", default=None)
    s.add_argument("--invoice-id", required=True)
    s.add_argument("--body", default=None, help="JSON object (or @file.json)")

    s = sub.add_parser("banktransactions-match", help="Match uncategorized bank transaction")
    s.add_argument("--dc", default=None)
    s.add_argument("--transaction-id", required=True)
    s.add_argument("--body", required=True, help="JSON object (or @file.json)")

    s = sub.add_parser("banktransactions-match-suggestions", help="Get match suggestions")

    s = sub.add_parser("invoices-pdf", help="Download invoice PDF")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/invoices/pdf")

    s = sub.add_parser("invoices-print", help="Download invoice print")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/invoices/print")

    s = sub.add_parser("estimates-pdf", help="Download estimate PDF")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/estimates/pdf")

    s = sub.add_parser("estimates-print", help="Download estimate print")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/estimates/print")

    s = sub.add_parser("salesorders-pdf", help="Download sales order PDF")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/salesorders/pdf")

    s = sub.add_parser("salesorders-print", help="Download sales order print")
    s.add_argument("--dc", default=None)
    s.add_argument("--query", default=None, help="JSON object (or @file.json)")
    s.add_argument("--out", required=True)
    s.set_defaults(_handler="_download", _path="/salesorders/print")

    s.add_argument("--dc", default=None)
    s.add_argument("--transaction-id", required=True)

    add_resource_commands(
        sub,
        "contacts",
        "/contacts",
        actions=[
            {"name": "activate", "method": "POST", "path": "/contacts/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/contacts/{id}/inactive"},
            {"name": "portal-enable", "method": "POST", "path": "/contacts/{id}/portal/enable"},
        ],
    )

    add_resource_commands(
        sub,
        "expenses",
        "/expenses",
        actions=[
            {"name": "comments-list", "method": "GET", "path": "/expenses/{id}/comments"},
        ],
        skip={"create"},
    )

    add_resource_commands(
        sub,
        "invoices",
        "/invoices",
        actions=[
            {"name": "status-sent", "method": "POST", "path": "/invoices/{id}/status/sent"},
            {"name": "status-void", "method": "POST", "path": "/invoices/{id}/status/void"},
            {"name": "status-draft", "method": "POST", "path": "/invoices/{id}/status/draft"},
            {"name": "submit", "method": "POST", "path": "/invoices/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/invoices/{id}/approve"},
            {"name": "paymentreminder-enable", "method": "POST", "path": "/invoices/{id}/paymentreminder/enable"},
            {"name": "paymentreminder-disable", "method": "POST", "path": "/invoices/{id}/paymentreminder/disable"},
            {"name": "writeoff", "method": "POST", "path": "/invoices/{id}/writeoff"},
            {"name": "writeoff-cancel", "method": "POST", "path": "/invoices/{id}/writeoff/cancel"},
        ],
    )

    add_resource_commands(
        sub,
        "bills",
        "/bills",
        actions=[
            {"name": "status-open", "method": "POST", "path": "/bills/{id}/status/open"},
            {"name": "status-void", "method": "POST", "path": "/bills/{id}/status/void"},
            {"name": "submit", "method": "POST", "path": "/bills/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/bills/{id}/approve"},
        ],
    )

    add_resource_commands(
        sub,
        "items",
        "/items",
        actions=[
            {"name": "activate", "method": "POST", "path": "/items/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/items/{id}/inactive"},
        ],
    )

    add_resource_commands(
        sub,
        "chartofaccounts",
        "/chartofaccounts",
        actions=[
            {"name": "activate", "method": "POST", "path": "/chartofaccounts/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/chartofaccounts/{id}/inactive"},
        ],
    )

    add_resource_commands(
        sub,
        "bankaccounts",
        "/bankaccounts",
        actions=[
            {"name": "activate", "method": "POST", "path": "/bankaccounts/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/bankaccounts/{id}/inactive"},
        ],
    )

    add_resource_commands(
        sub,
        "banktransactions",
        "/banktransactions",
        actions=[
            {"name": "categorize", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize", "body": True},
            {"name": "categorize-expenses", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize/expenses", "body": True},
            {"name": "categorize-vendorpayments", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize/vendorpayments", "body": True},
            {"name": "categorize-customerpayments", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize/customerpayments", "body": True},
            {"name": "categorize-creditnoterefunds", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize/creditnoterefunds", "body": True},
            {"name": "categorize-vendorcreditrefunds", "method": "POST", "path": "/banktransactions/uncategorized/{id}/categorize/vendorcreditrefunds", "body": True},
            {"name": "categorize-paymentrefunds", "method": "POST", "path": "/banktransactions/uncategorized/{statement_line_id}/categorize/paymentrefunds", "body": True},
            {"name": "categorize-vendorpaymentrefunds", "method": "POST", "path": "/banktransactions/uncategorized/{statement_line_id}/categorize/vendorpaymentrefunds", "body": True},

            {"name": "unmatch", "method": "POST", "path": "/banktransactions/{id}/unmatch"},
            {"name": "uncategorize", "method": "POST", "path": "/banktransactions/{id}/uncategorize"},
        ],
    )

    add_resource_commands(
        sub,
        "vendorcredits",
        "/vendorcredits",
        actions=[
            {"name": "status-open", "method": "POST", "path": "/vendorcredits/{id}/status/open"},
            {"name": "status-void", "method": "POST", "path": "/vendorcredits/{id}/status/void"},
            {"name": "submit", "method": "POST", "path": "/vendorcredits/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/vendorcredits/{id}/approve"},
        ],
    )

    add_resource_commands(
        sub,
        "vendorpayments",
        "/vendorpayments",
        actions=[
            {"name": "email", "method": "POST", "path": "/vendorpayments/{id}/email", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "customerpayments",
        "/customerpayments",
    )

    add_resource_commands(
        sub,
        "estimates",
        "/estimates",
        actions=[
            {"name": "status-sent", "method": "POST", "path": "/estimates/{id}/status/sent"},
            {"name": "status-accepted", "method": "POST", "path": "/estimates/{id}/status/accepted"},
            {"name": "status-declined", "method": "POST", "path": "/estimates/{id}/status/declined"},
            {"name": "submit", "method": "POST", "path": "/estimates/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/estimates/{id}/approve"},
            {"name": "email", "method": "POST", "path": "/estimates/{id}/email", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "salesorders",
        "/salesorders",
        actions=[
            {"name": "status-open", "method": "POST", "path": "/salesorders/{id}/status/open"},
            {"name": "status-void", "method": "POST", "path": "/salesorders/{id}/status/void"},
            {"name": "submit", "method": "POST", "path": "/salesorders/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/salesorders/{id}/approve"},
            {"name": "email", "method": "POST", "path": "/salesorders/{id}/email", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "purchaseorders",
        "/purchaseorders",
        actions=[
            {"name": "status-open", "method": "POST", "path": "/purchaseorders/{id}/status/open"},
            {"name": "status-billed", "method": "POST", "path": "/purchaseorders/{id}/status/billed"},
            {"name": "status-cancelled", "method": "POST", "path": "/purchaseorders/{id}/status/cancelled"},
            {"name": "submit", "method": "POST", "path": "/purchaseorders/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/purchaseorders/{id}/approve"},
            {"name": "email", "method": "POST", "path": "/purchaseorders/{id}/email", "body": True},
            {"name": "reject", "method": "POST", "path": "/purchaseorders/{id}/reject", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "creditnotes",
        "/creditnotes",
        actions=[
            {"name": "status-void", "method": "POST", "path": "/creditnotes/{id}/status/void"},
            {"name": "status-draft", "method": "POST", "path": "/creditnotes/{id}/status/draft"},
            {"name": "status-open", "method": "POST", "path": "/creditnotes/{id}/status/open"},
            {"name": "submit", "method": "POST", "path": "/creditnotes/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/creditnotes/{id}/approve"},
            {"name": "email", "method": "POST", "path": "/creditnotes/{id}/email", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "retainerinvoices",
        "/retainerinvoices",
        actions=[
            {"name": "status-sent", "method": "POST", "path": "/retainerinvoices/{id}/status/sent"},
            {"name": "status-void", "method": "POST", "path": "/retainerinvoices/{id}/status/void"},
            {"name": "status-draft", "method": "POST", "path": "/retainerinvoices/{id}/status/draft"},
            {"name": "submit", "method": "POST", "path": "/retainerinvoices/{id}/submit"},
            {"name": "approve", "method": "POST", "path": "/retainerinvoices/{id}/approve"},
            {"name": "email", "method": "POST", "path": "/retainerinvoices/{id}/email", "body": True},
        ],
    )

    add_resource_commands(
        sub,
        "projects",
        "/projects",
        actions=[
            {"name": "activate", "method": "POST", "path": "/projects/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/projects/{id}/inactive"},
            {"name": "clone", "method": "POST", "path": "/projects/{id}/clone"},
        ],
    )

    add_tasks_commands(sub)
    add_timeentry_commands(sub)

    add_resource_commands(
        sub,
        "journals",
        "/journals",
        actions=[
            {"name": "publish", "method": "POST", "path": "/journals/{id}/status/publish"},
        ],
    )

    add_resource_commands(sub, "taxes", "/settings/taxes")
    add_resource_commands(sub, "taxgroups", "/settings/taxgroups")
    add_resource_commands(sub, "taxauthorities", "/settings/taxauthorities")
    add_resource_commands(sub, "taxexemptions", "/settings/taxexemptions")

    add_resource_commands(sub, "bankrules", "/bankaccounts/rules")
    add_resource_commands(sub, "basecurrencyadjustment", "/basecurrencyadjustment")
    add_resource_commands(sub, "contactpersons", "/contacts/contactpersons")
    add_resource_commands(sub, "currencies", "/settings/currencies")
    add_resource_commands(sub, "fixedassets", "/fixedassets")
    add_resource_commands(
        sub,
        "locations",
        "/locations",
        actions=[
            {"name": "enable", "method": "POST", "path": "/settings/locations/enable", "needs_id": False},
            {"name": "activate", "method": "POST", "path": "/locations/{id}/active"},
            {"name": "deactivate", "method": "POST", "path": "/locations/{id}/inactive"},
            {"name": "mark-primary", "method": "POST", "path": "/locations/{id}/markasprimary"},
        ],
    )
    add_resource_commands(sub, "openingbalances", "/settings/openingbalances")
    add_resource_commands(sub, "organizations", "/organizations", skip={"create", "update", "delete"})
    add_resource_commands(sub, "recurringbills", "/recurringbills")
    add_resource_commands(sub, "recurringexpenses", "/recurringexpenses")
    add_resource_commands(sub, "recurringinvoices", "/recurringinvoices")
    add_resource_commands(
        sub,
        "reportingtags",
        "/reportingtags",
        actions=[
            {"name": "mark-default", "method": "POST", "path": "/reportingtags/{id}", "query": True},
        ],
    )
    add_resource_commands(sub, "salesreceipts", "/salesreceipts")

    # Advanced actions: comments, attachments, templates, payments, refunds
    add_comments_commands(sub, "invoices", "/invoices/{id}/comments")
    add_attachment_command(sub, "invoices", "/invoices/{id}/attachment")
    add_templates_commands(sub, "invoices", "invoices")
    add_payments_commands(sub, "invoices", "invoices")

    add_comments_commands(sub, "bills", "/bills/{id}/comments")
    add_attachment_command(sub, "bills", "/bills/{id}/attachment")
    add_payments_commands(sub, "bills", "bills")

    add_comments_commands(sub, "estimates", "/estimates/{id}/comments")
    add_templates_commands(sub, "estimates", "estimates")

    add_comments_commands(sub, "salesorders", "/salesorders/{id}/comments")
    add_attachment_command(sub, "salesorders", "/salesorders/{id}/attachment")
    add_templates_commands(sub, "salesorders", "salesorders")

    add_comments_commands(sub, "purchaseorders", "/purchaseorders/{id}/comments")
    add_attachment_command(sub, "purchaseorders", "/purchaseorders/{id}/attachment")
    add_templates_commands(sub, "purchaseorders", "purchaseorders")

    add_comments_commands(sub, "creditnotes", "/creditnotes/{id}/comments")
    s = sub.add_parser("creditnotes-emailhistory", help="Get credit note email history")
    s.add_argument("--dc", default=None)
    s.add_argument("--id", required=True)
    s.set_defaults(_method="GET", _path="/creditnotes/{id}/emailhistory", _handler=handle_api_command)

    add_templates_commands(sub, "creditnotes", "creditnotes")
    add_refunds_commands(sub, "creditnotes", "creditnotes", refund_param="creditnote_refund_id")

    add_comments_commands(sub, "retainerinvoices", "/retainerinvoices/{id}/comments")
    add_attachment_command(sub, "retainerinvoices", "/retainerinvoices/{id}/attachment")
    add_templates_commands(sub, "retainerinvoices", "retainerinvoices")

    add_comments_commands(sub, "journals", "/journals/{id}/comments")
    add_attachment_command(sub, "journals", "/journals/{id}/attachment")

    add_comments_commands(sub, "vendorcredits", "/vendorcredits/{id}/comments")
    add_refunds_commands(sub, "vendorcredits", "vendorcredits", refund_param="vendor_credit_refund_id")

    add_refunds_commands(sub, "vendorpayments", "vendorpayments", refund_param="vendorpayment_refund_id")
    add_refunds_commands(sub, "customerpayments", "customerpayments", refund_param="refund_id")

    add_resource_commands(sub, "users", "/users")

    args = p.parse_args()
    cfg = load_config()

    if args.cmd == "init":
        cfg = {
            "datacenter": args.dc.upper(),
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "",
            "refresh_token": "",
            "organization_id": "",
        }
        save_config(cfg)
        print(f"Created config template at {CONFIG_PATH}")
        return

    if args.cmd == "auth-url":
        dc, _ = get_dc(cfg, args.dc)
        url = build_auth_url(cfg, dc, args.scopes, args.redirect_uri, args.state)
        print(url)
        return

    if args.cmd == "exchange-code":
        dc, dc_info = get_dc(cfg, args.dc)
        data = {
            "code": args.code,
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "grant_type": "authorization_code",
            "redirect_uri": args.redirect_uri,
        }
        url = f"{dc_info['accounts']}/token"
        raw = http_post(url, data)
        resp = json.loads(raw)
        if "refresh_token" in resp:
            cfg["refresh_token"] = resp["refresh_token"]
            save_config(cfg)
        print(json.dumps(resp, indent=2))
        return

    if args.cmd == "refresh":
        dc, dc_info = get_dc(cfg, args.dc)
        resp = refresh_token(cfg, dc_info)
        print(json.dumps(resp, indent=2))
        return


    if args.cmd == "upload":
        dc, dc_info = get_dc(cfg, args.dc)
        path = args.path
        body = args.body
        cmd_upload(cfg, dc_info, path, args.file, field=args.field, body=body)
        return

    if args.cmd == "download":
        dc, dc_info = get_dc(cfg, args.dc)
        cmd_download(cfg, dc_info, args.path, args.out, query=args.query)
        return

    if args.cmd == "request":
        dc, dc_info = get_dc(cfg, args.dc)
        query = load_json_arg(args.query) if args.query else {}
        body = load_json_arg(args.body) if args.body else None
        resp = api_request(cfg, dc_info, args.method, args.path, query, body)
        print(resp)
        return

    if args.cmd == "orgs-list":
        dc, dc_info = get_dc(cfg, args.dc)
        cmd_orgs_list(cfg, dc_info)
        return

    if args.cmd == "orgs-select":
        cmd_orgs_select(cfg, args.id)
        return

    if args.cmd == "contacts-upsert":
        dc, dc_info = get_dc(cfg, args.dc)
        cmd_contacts_upsert(cfg, dc_info, args.name, args.type)
        return

    if args.cmd == "expenses-create":
        dc, dc_info = get_dc(cfg, args.dc)
        body = load_json_arg(args.body)
        cmd_expenses_create(cfg, dc_info, body, receipt=args.receipt, attachment=args.attachment)
        return

    if args.cmd == "invoices-email":
        dc, dc_info = get_dc(cfg, args.dc)
        body = load_json_arg(args.body) if args.body else None
        cmd_invoices_email(cfg, dc_info, args.invoice_id, body=body)
        return

    if args.cmd == "banktransactions-match":
        dc, dc_info = get_dc(cfg, args.dc)
        body = load_json_arg(args.body)
        cmd_banktransactions_match(cfg, dc_info, args.transaction_id, body)
        return

    if args.cmd == "banktransactions-match-suggestions":
        dc, dc_info = get_dc(cfg, args.dc)
        cmd_banktransactions_uncategorized_matches(cfg, dc_info, args.transaction_id)
        return



    if getattr(args, "_handler", None) == "_download":
        dc, dc_info = get_dc(cfg, args.dc)
        path = build_path(args._path, args)
        cmd_download(cfg, dc_info, path, args.out, query=args.query)
        return

    if getattr(args, "_handler", None) == "_upload":
        dc, dc_info = get_dc(cfg, args.dc)
        path = build_path(args._path, args)
        cmd_upload(cfg, dc_info, path, args.file, field=args.field, body=args.body)
        return

    if hasattr(args, "_handler"):
        dc, dc_info = get_dc(cfg, args.dc)
        args._handler(cfg, dc_info, args)
        return

    p.print_help()


if __name__ == "__main__":
    main()
