"""Confirm the origin negotiates h2 via TLS ALPN."""

from __future__ import annotations

import os
import ssl
import socket

BASE_URL = os.environ.get("RUNLOOP_BASE_URL", "https://api.runloop.ai")
url_parts = BASE_URL.split("://", 1)
host = url_parts[1].split("/")[0] if len(url_parts) > 1 else url_parts[0]
port = 443

print(f"Checking ALPN for {host}:{port}")

ctx = ssl.create_default_context()
ctx.set_alpn_protocols(["h2", "http/1.1"])

with socket.create_connection((host, port)) as sock:
    with ctx.wrap_socket(sock, server_hostname=host) as tls:
        print(f"Negotiated protocol: {tls.selected_alpn_protocol()}")
        print(f"TLS version:         {tls.version()}")
