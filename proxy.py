#!/usr/bin/env python3
"""
HR Policy Advisor - 后端代理服务
解决浏览器直接调用 Anthropic API 的 CORS 问题
运行在 5001 端口，Nginx 反向代理 /api/ 路径
"""
from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "invalid request"}), 400

        headers = {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        }

        resp = requests.post(ANTHROPIC_API_URL, json=body, headers=headers, timeout=30)
        return jsonify(resp.json()), resp.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "upstream timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
