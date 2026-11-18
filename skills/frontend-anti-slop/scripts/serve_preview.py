#!/usr/bin/env python3
"""
serve_preview.py - Lightweight local web server for direct webpage visual inspection.
Spins up a local HTTP server to preview static HTML or frontend build folders,
enabling browser subagents and developers to inspect rendered pixels and layout.
No external dependencies (uses standard library http.server, socketserver, argparse).
"""

import argparse
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
import socket
import socketserver
import sys
import threading
import time


def find_available_port(start_port: int = 8080, max_attempts: int = 20) -> int:
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError(f"Could not find an available port starting from {start_port}")


def main():
    parser = argparse.ArgumentParser(
        description="Serve local HTML or frontend build folder for direct visual inspection."
    )
    parser.add_argument("target", nargs="?", default=".", help="Target HTML file or directory to serve")
    parser.add_argument("--port", type=int, default=8080, help="Preferred port (default: 8080)")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"錯誤：找不到目標路徑 {target_path}", file=sys.stderr)
        sys.exit(1)

    if target_path.is_file():
        serve_dir = target_path.parent
        index_file = target_path.name
    else:
        serve_dir = target_path
        index_file = ""

    port = find_available_port(args.port)

    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *h_args, **h_kwargs):
            super().__init__(*h_args, directory=str(serve_dir), **h_kwargs)

        def log_message(self, format, *log_args):
            # Keep terminal output clean during inspection
            pass

    server = socketserver.TCPServer(("127.0.0.1", port), CustomHandler)
    url = f"http://127.0.0.1:{port}/{index_file}"

    print("=" * 72)
    print("  FRONTEND ANTI-SLOP LOCAL PREVIEW SERVER")
    print("=" * 72)
    print(f"服務目錄 : {serve_dir}")
    print(f"預覽網址 : {url}")
    print("-" * 72)
    print("💡 視覺審查指示：")
    print("1. 請調度 browser subagent 或在本機瀏覽器中開啟上方網址。")
    print("2. 執行遠看測試 (Squint Test)，檢查首屏視覺焦點與色彩預算。")
    print("3. 測量各 Section 垂直內距是否達到 160px，主標題字級比是否 ≥ 3.0 倍。")
    print("4. 修改代碼後重新整理頁面，反覆觀看對比直到視覺收斂。")
    print("=" * 72)
    print("按 Ctrl+C 可停止伺服器...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已安全停止。")
        server.server_close()


if __name__ == "__main__":
    main()
