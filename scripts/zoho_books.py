#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

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


def api_request(cfg, dc_info, method, path, query=None, body=None):
    token = refresh_token(cfg, dc_info).get("access_token")
    if not token:
        raise SystemExit("Failed to refresh access token")
    org_id = cfg.get("organization_id")
    if not org_id:
        raise SystemExit("Missing organization_id in config")

    query = query or {}
    query["organization_id"] = org_id
    url = f"{dc_info['api']}{path}?{urllib.parse.urlencode(query)}"

    data = None
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


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

    s = sub.add_parser("request", help="Make API request")
    s.add_argument("--dc", default=None)
    s.add_argument("--method", required=True)
    s.add_argument("--path", required=True)
    s.add_argument("--query", default=None, help="JSON object")
    s.add_argument("--body", default=None, help="JSON object")

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

    if args.cmd == "request":
        dc, dc_info = get_dc(cfg, args.dc)
        query = json.loads(args.query) if args.query else {}
        body = json.loads(args.body) if args.body else None
        resp = api_request(cfg, dc_info, args.method, args.path, query, body)
        print(resp)
        return

    p.print_help()


if __name__ == "__main__":
    main()
