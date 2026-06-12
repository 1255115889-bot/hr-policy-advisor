# HR政策智能顾问

> 基于《员工手册》的AI智能问答系统，帮助员工快速查询公司HR政策。

## 功能特性

- 🤖 自然语言查询 HR 政策
- 📋 严格基于员工手册，不编造答案
- 🔖 回答自动标注政策依据条款
- 💬 超出知识库范围提示联系 HR
- 🎨 简洁专业的企业风格界面

## 本地运行

```bash
python3 server.py
# 访问 http://localhost:8080
```

## 部署到服务器

```bash
bash deploy.sh
```

## 技术栈

- 纯前端 HTML/CSS/JS（无框架依赖）
- Claude Sonnet API（AI 问答）
- Python 内置 HTTP Server
- systemd 服务管理

## 知识库

内置 30 条员工手册政策，涵盖：假期制度、薪酬福利、报销规定、晋升发展、离职流程等。
