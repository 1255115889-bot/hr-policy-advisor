#!/usr/bin/env python3
"""
HR Policy Advisor - 后端代理服务（DeepSeek）
运行在 5001 端口，Nginx 反向代理 /api/ 路径
"""
from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL   = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "invalid request"}), 400

        # 把前端传来的 {system, messages} 转成 OpenAI 格式
        system  = body.get("system", "")
        messages = body.get("messages", [])

        openai_messages = []
        if system:
            openai_messages.append({"role": "system", "content": system})
        openai_messages.extend(messages)

        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": openai_messages,
            "max_tokens": body.get("max_tokens", 1000),
            "temperature": 0.3,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        }

        resp = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()

        # 转成前端期望的格式：data.content[0].text
        if resp.status_code == 200:
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return jsonify({"content": [{"type": "text", "text": text}]}), 200
        else:
            return jsonify({"error": data}), resp.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "upstream timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "model": DEEPSEEK_MODEL})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
