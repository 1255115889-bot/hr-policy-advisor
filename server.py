#!/usr/bin/env python3
"""Simple HTTP server for HR Policy Advisor"""
import http.server, socketserver, os

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

print(f"HR Policy Advisor running at http://0.0.0.0:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
