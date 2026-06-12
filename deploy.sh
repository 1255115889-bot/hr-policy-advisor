#!/bin/bash
# deploy.sh - 一键部署脚本（在阿里云服务器上执行）
set -e

APP_DIR="/opt/hr-policy-advisor"
SERVICE="hr-advisor"

echo "=== [1/4] 拉取最新代码 ==="
cd $APP_DIR && git pull origin main

echo "=== [2/4] 安装 systemd 服务 ==="
cp $APP_DIR/hr-advisor.service /etc/systemd/system/
systemctl daemon-reload

echo "=== [3/4] 启动/重启服务 ==="
systemctl enable $SERVICE
systemctl restart $SERVICE

echo "=== [4/4] 检查状态 ==="
systemctl status $SERVICE --no-pager
echo ""
echo "✅ 部署完成！访问地址：http://$(curl -s ifconfig.me):8080"
