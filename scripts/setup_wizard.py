#!/usr/bin/env python3
import json
import os
import urllib.parse
import webbrowser
from getpass import getpass

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


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def build_auth_url(dc, client_id, redirect_uri, scopes):
    base = DC_MAP[dc]["accounts"]
    params = {
        "scope": scopes,
        "client_id": client_id,
        "response_type": "code",
        "access_type": "offline",
        "redirect_uri": redirect_uri,
        "prompt": "consent",
    }
    return f"{base}/auth?{urllib.parse.urlencode(params)}"


def exchange_code(dc, client_id, client_secret, code, redirect_uri):
    import urllib.request
    data = urllib.parse.urlencode(
        {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")
    url = f"{DC_MAP[dc]['accounts']}/token"
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print("Zoho Books setup wizard")
    print("-----------------------")

    dc = input("Datacenter (EU/US/IN/AU/JP) [EU]: ").strip().upper() or "EU"
    if dc not in DC_MAP:
        raise SystemExit("Unsupported datacenter")

    client_id = input("Client ID: ").strip()
    client_secret = getpass("Client Secret (hidden): ").strip()
    redirect_uri = input("Redirect URI [https://127.0.0.1:8443/callback]: ").strip() or "https://127.0.0.1:8443/callback"
    scopes = input(f"Scopes [{DEFAULT_SCOPE}]: ").strip() or DEFAULT_SCOPE

    auth_url = build_auth_url(dc, client_id, redirect_uri, scopes)
    print("\nOpen this URL in your browser and approve:\n")
    print(auth_url)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    code = input("\nPaste the code= value here: ").strip()
    token = exchange_code(dc, client_id, client_secret, code, redirect_uri)
    if "refresh_token" not in token:
        print("\nFailed to exchange code:")
        print(json.dumps(token, indent=2))
        raise SystemExit(1)

    cfg = {
        "datacenter": dc,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "refresh_token": token["refresh_token"],
        "organization_id": "",
    }
    save_config(cfg)

    print("\nSaved config to", CONFIG_PATH)
    print("Next: set organization_id (from Zoho Books → Settings → Organization Profile).")


if __name__ == "__main__":
    main()
