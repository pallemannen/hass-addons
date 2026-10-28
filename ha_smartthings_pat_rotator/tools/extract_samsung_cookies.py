#!/usr/bin/env python3
"""Extract Chrome cookies for the Samsung/SmartThings login domains.

Run this ON YOUR MACHINE (not in the HA container/add-on) - it reads your
local Chrome cookie store, after logging into these in that browser:
  - https://account.smartthings.com/ - required.
  - https://account.samsung.com/ - recommended (SmartThings login is SSO
    through the Samsung account, so this likely helps the session survive
    longer; not confirmed to be strictly necessary on its own).

Just run:

    python3 extract_samsung_cookies.py

It needs the browser_cookie3 package. If your Python doesn't have it, the
first run installs it into a private environment in
~/.cache/extract_samsung_cookies/ and uses that from then on - no pip or
Homebrew steps, and nothing is installed into your system Python.

macOS will prompt for your login password / Touch ID the first time, since
Chrome's cookie encryption key lives in Keychain ("Chrome Safe Storage") -
that's expected, not an error. Click "Always Allow" if you don't want the
prompt every run.

Writes samsung_cookies.json next to this script. Paste its raw contents into
the add-on's "Cookies JSON" (cookies_json) configuration field - the add-on
converts it and seeds a logged-in browser session automatically, then clears
the field. You need to do this whenever rotation starts failing because the
add-on's saved session has expired - Samsung's fraud detection blocks a
fully cold automated login outright (confirmed: it triggers a real
reCAPTCHA/MFA challenge every time), so a real logged-in session always has
to come from a real browser first.
"""
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

# Private environment for browser_cookie3. Homebrew's Python (and other
# "externally managed" ones) refuse a plain pip install, so the script keeps
# its one dependency here instead of asking the user to set anything up.
VENV_DIR = Path.home() / ".cache" / "extract_samsung_cookies" / "venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run_in_private_venv() -> None:
    """Install browser_cookie3 into VENV_DIR if needed, then re-run this script there."""
    if Path(sys.prefix).resolve() == VENV_DIR.resolve():
        sys.exit(
            f"browser_cookie3 is missing from {VENV_DIR}. Delete that folder "
            "and run the script again."
        )
    try:
        if not VENV_PYTHON.exists():
            print(f"First run: installing browser_cookie3 into {VENV_DIR}")
            venv.create(VENV_DIR, with_pip=True)
        check = [str(VENV_PYTHON), "-c", "import browser_cookie3"]
        if subprocess.run(check, capture_output=True).returncode != 0:
            install = [str(VENV_PYTHON), "-m", "pip", "install", "--quiet", "browser_cookie3"]
            subprocess.run(install, check=True)
    except Exception as err:  # e.g. Debian without the python3-venv package, or no network
        # Don't leave a half-made environment behind for the next run to trip over.
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        sys.exit(f"Could not install browser_cookie3 into {VENV_DIR}: {err}")
    os.execv(VENV_PYTHON, [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]])


try:
    import browser_cookie3
except ImportError:
    run_in_private_venv()

# Substring match against cookie.domain, so this also catches subdomains
# like dls-account.di.atlas.samsung.com and account.smartthings.com.
DOMAINS = [
    "samsung.com",
    "smartthings.com",
]


def main() -> None:
    cj = browser_cookie3.chrome()
    cookies = []
    for c in cj:
        if not any(d in c.domain for d in DOMAINS):
            continue
        http_only = False
        if hasattr(c, "_rest") and isinstance(c._rest, dict):
            http_only = "HttpOnly" in c._rest or bool(c._rest.get("HttpOnly"))
        cookies.append(
            {
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "expires": c.expires,
                "secure": bool(c.secure),
                "httpOnly": http_only,
            }
        )

    out_path = "samsung_cookies.json"
    with open(out_path, "w") as f:
        json.dump(cookies, f, indent=2)

    domains_found = sorted({c["domain"] for c in cookies})
    print(f"Wrote {len(cookies)} cookies to {out_path}")
    print("Domains found:")
    for d in domains_found:
        print(f"  {d}")
    if not cookies:
        print(
            "\nNo matching cookies found. Make sure you're actually logged "
            "in to account.samsung.com in Chrome (the default profile)."
        )


if __name__ == "__main__":
    main()
