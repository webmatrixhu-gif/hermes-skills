#!/usr/bin/env python3
"""Publish one verified HTML visualization to a random Surge subdomain."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import ssl
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SURGE_SUFFIX = ".surge.sh"
DEFAULT_PREFIX = "wm-viz"
ROBOTS_META = '<meta name="robots" content="noindex,nofollow,noarchive">'
ROBOTS_TXT = "User-agent: *\nDisallow: /\n"


def fail(message: str) -> "NoReturn":
    print(f"publish_surge: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_and_prepare(source: Path) -> bytes:
    if not source.exists() or not source.is_file():
        fail(f"HTML source does not exist or is not a regular file: {source}")
    if source.is_symlink():
        fail(f"HTML source must not be a symlink: {source}")

    try:
        html = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail("HTML source must be UTF-8 text")

    stripped = html.strip()
    if not re.match(r"(?is)^<!doctype\s+html\b", stripped):
        fail("HTML must start with <!doctype html>")
    if not re.search(r"(?is)<html(?:\s|>)", stripped) or not re.search(r"(?is)</html>\s*$", stripped):
        fail("HTML must be a complete document ending with </html>")
    if not re.search(r"(?is)<head(?:\s|>)", stripped) or not re.search(r"(?is)</head>", stripped):
        fail("HTML must contain a complete <head> section")

    if not re.search(r"(?is)<meta\b[^>]*\bname\s*=\s*['\"]robots['\"]", html):
        html, replacements = re.subn(
            r"(?is)</head>",
            f"  {ROBOTS_META}\n</head>",
            html,
            count=1,
        )
        if replacements != 1:
            fail("Could not inject robots metadata")

    return html.encode("utf-8")


def normalize_domain(value: str | None, prefix: str) -> str:
    if value:
        domain = value.strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")
        if not domain.endswith(SURGE_SUFFIX):
            fail(f"Explicit domain must end with {SURGE_SUFFIX}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*[a-z0-9]", domain):
            fail("Explicit domain contains unsafe characters")
        return domain

    safe_prefix = re.sub(r"[^a-z0-9-]+", "-", prefix.lower()).strip("-")
    if not safe_prefix:
        safe_prefix = DEFAULT_PREFIX
    return f"{safe_prefix}-{secrets.token_hex(10)}{SURGE_SUFFIX}"


def require_surge_auth() -> None:
    try:
        result = subprocess.run(
            ["surge", "whoami"],
            stdin=subprocess.DEVNULL,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
    except FileNotFoundError:
        fail("Surge CLI is not installed")
    except subprocess.TimeoutExpired:
        fail("Surge authentication check timed out")

    output = result.stdout or ""
    normalized = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output).lower()
    if (
        result.returncode != 0
        or "not authenticated" in normalized
        or "email:" in normalized
        or "login or create" in normalized
    ):
        fail("Surge CLI is installed but not authenticated; run `surge login` in an SSH terminal first")


def publish(project: Path, domain: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["surge", str(project), domain],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    except FileNotFoundError:
        fail("Surge CLI is not installed")
    except subprocess.TimeoutExpired:
        fail("Surge publish timed out after 180 seconds")

    output = result.stdout or ""
    succeeded = result.returncode == 0 and "success" in output.lower()
    return succeeded, output


def verify(url: str, expected: bytes, attempts: int = 20) -> tuple[int, str]:
    expected_hash = hashlib.sha256(expected).hexdigest()
    last_error = "no response"
    context = ssl.create_default_context()

    for attempt in range(attempts):
        if attempt:
            time.sleep(3)
        try:
            request = Request(url, headers={"User-Agent": "Hermes-visualize-this-verifier/1.0"})
            with urlopen(request, timeout=15, context=context) as response:
                body = response.read()
                status = int(response.status)
            actual_hash = hashlib.sha256(body).hexdigest()
            if status == 200 and actual_hash == expected_hash:
                return status, actual_hash
            last_error = f"HTTP {status}; expected SHA-256 {expected_hash}, got {actual_hash}"
        except (HTTPError, URLError, TimeoutError, ssl.SSLError) as error:
            last_error = str(error)

    fail(f"published URL did not verify: {last_error}")


def record_deployment(domain: str, source: Path, sha256: str) -> None:
    registry = Path.home() / "visualizations" / ".surge-deployments.jsonl"
    registry.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "domain": domain,
        "url": f"https://{domain}/",
        "source_name": source.name,
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sha256": sha256,
    }
    descriptor = os.open(registry, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, (json.dumps(record, sort_keys=True) + "\n").encode("utf-8"))
    finally:
        os.close(descriptor)
    os.chmod(registry, 0o600)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Complete UTF-8 HTML document to publish")
    parser.add_argument("--domain", help="Optional explicit *.surge.sh domain")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="Random domain prefix")
    args = parser.parse_args()

    require_surge_auth()
    source = args.html.expanduser().absolute()
    prepared = read_and_prepare(source)

    with tempfile.TemporaryDirectory(prefix="hermes-visualize-surge-") as temp_name:
        project = Path(temp_name)
        (project / "index.html").write_bytes(prepared)
        (project / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")

        output = ""
        domain = ""
        for _ in range(4):
            domain = normalize_domain(args.domain, args.prefix)
            ok, output = publish(project, domain)
            if ok:
                break
            if args.domain:
                fail(f"Surge publish failed for {domain}: {output.strip()[-1200:]}")
        else:
            fail(f"Surge publish failed after four random domains: {output.strip()[-1200:]}")

        url = f"https://{domain}/"
        status, remote_hash = verify(url, prepared)
        record_deployment(domain, source, remote_hash)

    print(json.dumps({
        "success": True,
        "url": url,
        "domain": domain,
        "http_status": status,
        "sha256": remote_hash,
        "robots": "noindex,nofollow,noarchive",
        "teardown_command": f"surge teardown {domain}",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
