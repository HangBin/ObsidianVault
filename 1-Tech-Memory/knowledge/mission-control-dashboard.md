---
author: tech agent
created: 2026-04-22 21:05:56
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
source: tech agent memory/experience-mission-control.md
tags: [tech-agent, experience, knowledge, mission-control]
---


# Mission Control 完整安装部署指南

**版本**: 1.0
**最后更新**: 2026-04-02
**适用对象**: 技术管理员，需要从源码部署 Mission Control
**前置要求**: Node.js 22+, pnpm, systemd, 基础 Linux 操作

---

## 📋 任务背景

用户需要安装 Mission Control（TenacitOS）Dashboard 来监控 OpenClaw 系统状态。

## 📋 目录

1. [环境准备](#环境准备)
2. [下载源码](#下载源码)
3. [配置环境变量](#配置环境变量)
4. [安装依赖](#安装依赖)
5. [构建项目](#构建项目)
6. [数据文件准备](#数据文件准备)
7. [配置 systemd 服务](#配置-systemd-服务)
8. [启动与验证](#启动与验证)
9. [访问与使用](#访问与使用)
10. [常见问题](#常见问题)

## 环境准备

### 1.1 系统要求

| 组件 | 版本要求 | 验证命令 |
|------|----------|----------|
| Node.js | v22+ (推荐 v22.22.2) | `node --version` |
| pnpm | 9.x+ | `pnpm --version` |
| npm | 10.x+ (可选) | `npm --version` |
| Git | 2.x+ | `git --version` |

### 1.2 目录结构规划

**推荐的工作区路径**（遵循 OpenClaw 代理隔离原则）：
```
~/.openclaw/workspace-tech/
└── mission-control/     # Mission Control 运行实例
```

**安装前检查**：
```bash
# 确认在正确的工作区
cd ~/.openclaw/workspace-tech

# 如果目录不存在，创建它
mkdir -p ~/.openclaw/workspace-tech
```

---

## 下载源码

### 2.1 选择源码仓库

Mission Control 的源码仓库是 **OpenClaw Control Center**：
- **仓库地址**: https://github.com/TianyiDataScience/openclaw-control-center.git
- **默认分支**: main
- **许可证**: MIT

### 2.2 克隆到正确位置

**⚠️ 重要**: 不要克隆到 `~/.openclaw/workspace/`（那是 main agent 的工作区），要克隆到 `~/.openclaw/workspace-tech/`（tech agent 的工作区）。

```bash
# 进入工作区
cd ~/.openclaw/workspace-tech

# 克隆仓库
git clone https://github.com/TianyiDataScience/openclaw-control-center.git mission-control

# 进入项目目录
cd mission-control

# 验证克隆成功
ls -la
# 应该看到: package.json, src/, README.md, etc.
```

### 2.3 可选：检查最新版本

```bash
# 查看当前提交
git log --oneline -1

# 拉取最新代码（如果需要更新）
git pull origin main
```

---

## 配置环境变量

### 3.1 创建 `.env.local` 文件

在项目根目录创建环境配置文件：

```bash
# 复制示例文件
cp .env.example .env.local

# 编辑配置文件
nano .env.local
# 或使用 vim/vscode
```

### 3.2 必填配置项

**.env.local 完整示例**：

```bash
# ============================================
# Mission Control 环境配置
# ============================================

# 管理密码（首次登录使用，请修改！）
ADMIN_PASSWORD=JR0JqSeyJUAivUhXpSAT1tQk

# 会话密钥（自动生成即可）
AUTH_SECRET=$(openssl rand -base64 32)
# 或手动设置: AUTH_SECRET=uz6YByGO0EfiWqVldlyDvqU8UrOZ1bMHo26GodpxKW8=

# OpenClaw 路径配置
OPENCLAW_DIR=/root/.openclaw
OPENCLAW_WORKSPACE=/root/.openclaw/workspace

# UI 品牌设置（可选）
NEXT_PUBLIC_AGENT_NAME=Mission Control
NEXT_PUBLIC_AGENT_EMOJI=🤖
NEXT_PUBLIC_AGENT_DESCRIPTION=Your AI co-pilot, powered by OpenClaw
NEXT_PUBLIC_COMPANY_NAME=MISSION CONTROL, INC.
NEXT_PUBLIC_APP_TITLE=Mission Control

# 🌐 本地化设置
# 支持: 'zh' (中文) 或 'en' (英文)
NEXT_PUBLIC_LANGUAGE=en

# ============================================
# 可选：自定义端口（默认 3000）
# ============================================
# UI_PORT=3000
```

### 3.3 生成安全密钥

```bash
# 生成随机会话密钥
openssl rand -base64 32

# 输出示例: uz6YByGO0EfiWqVldlyDvqU8UrOZ1bMHo26GodpxKW8=
# 复制并填入 .env.local 的 AUTH_SECRET
```

### 3.4 重要提醒

- **🔐 安全**: 首次部署后请立即修改 `ADMIN_PASSWORD`
- **📝 注释**: `.env.local` 可以包含 `#` 注释，但如果同时使用 systemd 的 `EnvironmentFile`，需要另外创建**无注释**的纯净版本
- **🔑 密钥**: `AUTH_SECRET` 必须是随机字符串，不要太短

---

## 安装依赖

### 4.1 使用 pnpm（推荐）

Mission Control 使用 pnpm 作为包管理器，可以避免原生模块编译问题：

```bash
# 检查 pnpm 是否安装
pnpm --version
# 预期输出: 9.x.x

# 安装依赖（在项目根目录）
pnpm install

# 如果遇到权限问题，尝试
pnpm install --no-frozen-lockfile
```

**预期输出**：
```
√ Dependencies installed in 1m 23s
   + 500 packages installed
```

### 4.2 备选：使用 npm

如果系统没有 pnpm，可以使用 npm：

```bash
npm install
```

**⚠️ 注意**：npm 可能会尝试编译原生模块（如 better-sqlite3），如果编译失败需要安装构建工具：
```bash
# Ubuntu/Debian
sudo apt-get install -y build-essential python3

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3
```

---

## 构建项目

### 5.1 开发构建（可选，用于测试）

```bash
# 启动开发服务器
pnpm dev

# 访问 http://localhost:3000 验证
# 按 Ctrl+C 停止开发服务器
```

### 5.2 生产构建（必须）

**⚠️ 关键**: 生产构建会读取 `.env.local` 中的 `NEXT_PUBLIC_*` 变量并编译到静态文件。修改环境变量后必须重新构建！

```bash
# 清理旧构建（可选但推荐）
rm -rf .next

# 生产构建
pnpm build
# 或 npm run build

# 预期输出:
# ✓ Compiled successfully in X.Xs
# ✓ Generating static pages using 3 workers (60/60) in XXXms
```

### 5.3 验证构建内容

确认本地化设置生效：

```bash
# 检查欢迎语是否为英文
if grep -r "Overview of agent activity" .next/static/chunks/*.js > /dev/null; then
  echo "✅ 英文本地化已嵌入"
else
  echo "❌ 未找到英文本地化，请检查 NEXT_PUBLIC_LANGUAGE 设置"
  grep -r "welcome" src/config/locale.ts
fi
```

---

## 数据文件准备

### 6.1 数据文件位置

Mission Control 需要从 OpenClaw 安装目录读取数据文件：

```
/root/.openclaw/workspace/
├── cron-jobs.json
├── activities.json
├── notifications.json
└── ...
```

### 6.2 复制数据文件（如果需要）

如果 OpenClaw 已有数据，可以复制到 Mission Control 的 `data/` 目录（可选）：

```bash
# 创建 data 目录
mkdir -p data

# 复制 cron 任务数据（示例）
cp /root/.openclaw/workspace/cron-jobs.json data/ 2>/dev/null || echo "cron-jobs.json 不存在，跳过"

# 复制活动数据（示例）
cp /root/.openclaw/workspace/activities.json data/ 2>/dev/null || echo "activities.json 不存在，跳过"
```

**📝 注意**: Mission Control 主要通过 API 实时读取 OpenClaw 数据，这些文件仅用于缓存或初始化。如果不存在，系统会继续运行但部分数据为空。

---

## 配置 systemd 服务

### 7.1 创建服务文件

```bash
sudo nano /etc/systemd/system/mission-control.service
```

### 7.2 服务文件内容

```ini
[Unit]
Description=TenacitOS — OpenClaw Mission Control Dashboard
After=network.target openclaw-gateway.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace-tech/mission-control

# ⚠️ EnvironmentFile 不支持注释，需要纯净版
EnvironmentFile=/root/.openclaw/workspace-tech/mission-control/.env.minimal

Environment=NODE_ENV=production
Environment=PATH=/root/.nvm/versions/node/v22.22.2/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ExecStart=/root/.nvm/versions/node/v22.22.2/bin/pnpm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**关键配置说明**：
- `WorkingDirectory`: 项目根目录（必须是 workspace-tech）
- `EnvironmentFile`: 指向**无注释**的 `.env.minimal`
- `ExecStart`: 使用 pnpm 启动（不要用 npm，性能较差）

### 7.3 创建纯净环境文件

因为 systemd 的 `EnvironmentFile` 不支持 `#` 注释，需要创建简化版：

```bash
# 从 .env.local 提取关键变量（去掉注释）
grep -v "^#" /root/.openclaw/workspace-tech/mission-control/.env.local | grep -v "^$" > /root/.openclaw/workspace-tech/mission-control/.env.minimal

# 或手动创建（推荐，确保关键变量存在）
cat > /root/.openclaw/workspace-tech/mission-control/.env.minimal << 'EOF'
NEXT_PUBLIC_LANGUAGE=en
ADMIN_PASSWORD=JR0JqSeyJUAivUhXpSAT1tQk
AUTH_SECRET=uz6YByGO0EfiWqVldlyDvqU8UrOZ1bMHo26GodpxKW8=
OPENCLAW_DIR=/root/.openclaw
OPENCLAW_WORKSPACE=/root/.openclaw/workspace
NEXT_PUBLIC_AGENT_NAME=Mission Control
NEXT_PUBLIC_AGENT_EMOJI=🤖
NEXT_PUBLIC_COMPANY_NAME=MISSION CONTROL, INC.
EOF
```

### 7.4 重载 systemd

```bash
sudo systemctl daemon-reload

# 验证服务文件语法
sudo systemctl status mission-control
# 应该显示 "Loaded: loaded" 而不是 "error"
```

---

## 启动与验证

### 8.1 启动服务

```bash
# 启动服务
sudo systemctl start mission-control

# 查看状态
sudo systemctl status mission-control

# 预期输出:
# ● mission-control.service - TenacitOS — OpenClaw Mission Control Dashboard
#      Loaded: loaded (/etc/systemd/system/mission-control.service; enabled; preset: enabled)
#      Active: active (running) since ...
#    Main PID: XXXXXX (node)
#     Memory: XX.XM
```

### 8.2 设置开机自启（可选）

```bash
sudo systemctl enable mission-control
# 输出: Created symlink /etc/systemd/system/multi-user.target.wants/mission-control.service → /etc/systemd/system/mission-control.service
```

### 8.3 查看日志

```bash
# 实时日志（调试用）
sudo journalctl -u mission-control -f

# 查看最近 50 行
sudo journalctl -u mission-control -n 50 --no-pager

# 查看启动日志
sudo journalctl -u mission-control --since "5 min ago" | grep -i "error\|failed"
```

### 8.4 健康检查 API

```bash
# 本地健康检查
curl http://localhost:3000/api/health

# 预期输出（JSON）:
# {
#   "status": "ok",
#   "checks": [...]
# }

# 如果返回 "degraded" 但 Mission Control 状态是 "up"，说明 OpenClaw Gateway 可能未连接，这是正常的
```

---

## 访问与使用

### 9.1 访问地址

**本地访问**：
```
http://localhost:3000
```

**外网访问**（需配置防火墙）：
```
http://<服务器IP>:3000
```

**⚠️ 安全提醒**：
- 默认监听 `0.0.0.0`（所有接口）
- 生产环境建议配置反向代理（Nginx/Caddy）+ HTTPS + 防火墙
- 立即修改默认管理员密码！

### 9.2 登录凭据

首次登录：
- **用户名**: 任意（或 `admin`）
- **密码**: `JR0JqSeyJUAivUhXpSAT1tQk`（见 `.env.local` 中的 `ADMIN_PASSWORD`）

**修改密码**：
1. 登录后点击右上角头像
2. 选择 "Settings" → "Change Password"
3. 输入当前密码和新密码
4. 保存

### 9.3 主要功能页面

| 页面 | 路径 | 说明 |
|------|------|------|
| 仪表板 | `/` | 系统概览、活动 feeds、快速统计 |
| 代理状态 | `/agents` | 所有 agent 的在线状态、会话数 |
| 会话列表 | `/sessions` | 当前和历史会话详情 |
| 成本分析 | `/costs` | Token 消耗和费用统计 |
| 定时任务 | `/cron` | cron 任务管理和手动触发 |
| 文件浏览器 | `/files` | 工作区文件浏览和编辑 |
| 内存搜索 | `/memory` | 搜索 agent 记忆 |
| 系统状态 | `/system` | CPU、内存、磁盘、网络 |
| 设置 | `/settings` | 密码、品牌、通知配置 |

### 9.4 配置数据源（如果需要）

如果 Mission Control 无法看到 OpenClaw 数据，检查：

1. **OpenClaw 路径配置**（`.env.local`）:
   ```bash
   OPENCLAW_DIR=/root/.openclaw
   OPENCLAW_WORKSPACE=/root/.openclaw/workspace
   ```

2. **OpenClaw Gateway 状态**:
   ```bash
   # 检查 gateway 是否运行
   sudo systemctl status openclaw-gateway
   
   # 如果未运行，启动它
   sudo systemctl start openclaw-gateway
   ```

3. **数据目录权限**:
   ```bash
   # 确保 mission-control 有读取权限
   ls -la /root/.openclaw/workspace/
   # 应该有 cron-jobs.json, activities.json 等文件
   ```

---

## 常见问题

### Q1: 构建失败，提示 module not found

**原因**: 依赖未正确安装

**解决**:
```bash
# 清理并重装
rm -rf node_modules .next
pnpm install
pnpm build
```

### Q2: 启动后端口被占用

**症状**: `Error: listen EADDRINUSE: address already in use :::3000`

**解决**:
```bash
# 查找占用端口的进程
sudo lsof -i :3000

# 停止该进程，或修改端口
# 修改 .env.local: UI_PORT=3001
# 然后重启服务
```

### Q3: 环境变量修改后未生效

**症状**: 修改 `.env.local` 后语言/配置未更新

**🔑 关键区别**:
- **编译时变量** (NEXT_PUBLIC_*): 需要重新构建才能生效
- **运行时变量** (如 ADMIN_PASSWORD, OPENCLAW_DIR): 重启服务即可生效

**完整生效流程**:

| 变量类型 | 示例 | 生效方式 | 步骤 |
|----------|------|----------|------|
| 编译时变量 | `NEXT_PUBLIC_LANGUAGE`<br>`NEXT_PUBLIC_AGENT_NAME` | 1. 修改 `.env.local`<br>2. 重新构建<br>3. 重启服务 | 修改 → `pnpm build` → 重启 |
| 运行时变量 | `ADMIN_PASSWORD`<br>`OPENCLAW_DIR`<br>`OPENCLAW_WORKSPACE`<br>`AUTH_SECRET` | 1. 修改 `.env.local`<br>2. 重启服务 | 修改 → 重启 |

**具体操作**：

**情况 A: 只修改了运行时变量**（如 OPENCLAW_DIR, ADMIN_PASSWORD）：
```bash
# 1. 修改 .env.local
nano .env.local
# 修改对应变量值

# 2. 重启服务
sudo systemctl restart mission-control

# 3. 验证
sudo systemctl status mission-control
```

**情况 B: 修改了编译时变量**（如 NEXT_PUBLIC_LANGUAGE, NEXT_PUBLIC_AGENT_NAME）：
```bash
# 1. 修改 .env.local
nano .env.local
# 修改 NEXT_PUBLIC_LANGUAGE=en 等

# 2. 重新构建（必须！）
cd /root/.openclaw/workspace-tech/mission-control
rm -rf .next
pnpm build

# 3. 验证构建内容（可选但推荐）
grep -r "Overview of agent activity" .next/static/  # 检查语言
# 或检查品牌名
grep -r "Mission Control" .next/static/ | head -3

# 4. 重启服务
sudo systemctl restart mission-control

# 5. 客户端强制刷新（浏览器缓存）
# Windows/Linux: Ctrl+F5
# Mac: Cmd+Shift+R
```

**情况 C: 同时修改了两种变量**：
```bash
# 按情况 B 操作（重新构建 + 重启）
```

### Q4: systemd EnvironmentFile 不生效

**原因**: `.env.minimal` 包含注释或格式错误

**解决**:
```bash
# 检查文件格式
cat .env.minimal

# 应该只有:
# KEY=value
# KEY=value
# 没有 # 注释，没有空行

# 重新生成纯净文件
grep -v "^#" .env.local | grep -v "^$" > .env.minimal

# 重载 systemd 并重启
sudo systemctl daemon-reload
sudo systemctl restart mission-control
```

### Q5: 页面显示 "Connection Error" 或数据为空

**原因**: `.env.minimal` 包含注释或格式错误

**解决**:

```bash
# 检查文件格式
cat .env.minimal

# 应该只有:
# KEY=value
# KEY=value
# 没有 # 注释，没有空行

# 重新生成
grep -v "^#" .env.local | grep -v "^$" > .env.minimal
```

### Q5: 页面显示 "Connection Error" 或数据为空

**可能原因**:
- OpenClaw Gateway 未运行
- `OPENCLAW_DIR` 或 `OPENCLAW_WORKSPACE` 路径错误
- 数据文件不存在（会显示空，但不会报错）

**诊断**:
```bash
# 1. 检查 Gateway
sudo systemctl status openclaw-gateway

# 2. 检查路径配置
grep OPENCLAW .env.local

# 3. 检查数据文件
ls -la /root/.openclaw/workspace/ | grep -E "cron|activities|notifications"
```

### Q6: 如何禁用/启用服务

```bash
# 停止服务
sudo systemctl stop mission-control

# 启动服务
sudo systemctl start mission-control

# 禁用开机自启
sudo systemctl disable mission-control

# 启用开机自启
sudo systemctl enable mission-control
```

### Q7: 日志在哪里？

```bash
# systemd 日志（主要）
sudo journalctl -u mission-control -f

# 项目日志（如果有）
tail -f /root/.openclaw/workspace-tech/mission-control/logs/*.log
```

---

## 配置地址汇总

### 项目文件位置

| 文件/目录 | 路径 | 说明 |
|-----------|------|------|
| 项目根目录 | `/root/.openclaw/workspace-tech/mission-control/` | 工作区位置 |
| 环境配置 | `/root/.openclaw/workspace-tech/mission-control/.env.local` | 完整配置（含注释） |
| 纯净环境 | `/root/.openclaw/workspace-tech/mission-control/.env.minimal` | systemd 专用 |
| 构建输出 | `/root/.openclaw/workspace-tech/mission-control/.next/` | 编译后的静态文件 |
| 数据目录 | `/root/.openclaw/workspace-tech/mission-control/data/` | 可选：缓存数据 |
| 服务配置 | `/etc/systemd/system/mission-control.service` | systemd unit 文件 |
| 日志查看 | `sudo journalctl -u mission-control` | systemd 日志 |

### OpenClaw 数据源

| 文件 | 路径 | 用途 |
|------|------|------|
| cron 数据 | `/root/.openclaw/workspace/cron-jobs.json` | 定时任务列表 |
| 活动数据 | `/root/.openclaw/workspace/activities.json` | 活动记录 |
| 通知数据 | `/root/.openclaw/workspace/notifications.json` | 通知中心 |
| 记忆文件 | `/root/.openclaw/workspace/memory/` | agent 记忆存储 |
| Gateway | `openclaw-gateway.service` | OpenClaw 网关服务 |

---

## 一键部署脚本（可选）

为了方便重复部署，可以将以下步骤保存为脚本：

```bash
#!/bin/bash
# deploy-mission-control.sh

set -e  # 遇到错误停止

echo "🚀 开始部署 Mission Control..."

# 1. 进入工作区
cd /root/.openclaw/workspace-tech

# 2. 克隆（如果不存在）
if [ ! -d "mission-control" ]; then
  git clone https://github.com/TianyiDataScience/openclaw-control-center.git mission-control
fi

cd mission-control

# 3. 安装依赖
pnpm install

# 4. 确保环境变量存在
if [ ! -f ".env.local" ]; then
  cp .env.example .env.local
  echo "⚠️  请手动编辑 .env.local 设置 ADMIN_PASSWORD 和 AUTH_SECRET"
  exit 1
fi

# 5. 创建纯净环境文件
grep -v "^#" .env.local | grep -v "^$" > .env.minimal

# 6. 构建
pnpm build

# 7. 配置 systemd
sudo cp /etc/systemd/system/mission-control.service /etc/systemd/system/mission-control.service.backup
sudo sed "s|WorkingDirectory=.*|WorkingDirectory=$(pwd)|" /etc/systemd/system/mission-control.service | sudo tee /etc/systemd/system/mission-control.service > /dev/null
sudo sed "s|EnvironmentFile=.*|EnvironmentFile=$(pwd)/.env.minimal|" /etc/systemd/system/mission-control.service | sudo tee /etc/systemd/system/mission-control.service > /dev/null

sudo systemctl daemon-reload
sudo systemctl restart mission-control

# 8. 验证
echo "📊 服务状态:"
sudo systemctl status mission-control --no-pager | head -10

echo ""
echo "✅ 部署完成！"
echo "🌐 访问地址: http://localhost:3000"
echo "🔑 密码: 查看 .env.local 中的 ADMIN_PASSWORD"
```

**使用**:
```bash
chmod +x deploy-mission-control.sh
./deploy-mission-control.sh
```

---

## 安全加固建议

1. **修改默认密码**
   ```bash
   # 编辑 .env.local
   ADMIN_PASSWORD=你的强密码（至少16位，包含大小写字母、数字、符号）
   # 重新构建并重启
   ```

2. **配置 HTTPS**
   ```bash
   # 使用 Caddy（推荐）
   sudo apt-get install -y caddy
   sudo nano /etc/caddy/Caddyfile
   
   # 内容:
   # your-domain.com {
   #   reverse_proxy localhost:3000
   #   encode gzip
   # }
   
   sudo systemctl restart caddy
   ```

3. **限制 IP 访问**（如果只需要内网访问）
   ```bash
   # ufw 示例
   sudo ufw allow from 192.168.1.0/24 to any port 3000
   sudo ufw deny 3000
   ```

4. **定期更新**
   ```bash
   cd /root/.openclaw/workspace-tech/mission-control
   git pull origin main
   pnpm install
   pnpm build
   sudo systemctl restart mission-control
   ```

---

## 卸载与清理

如果需要完全移除 Mission Control：

```bash
# 1. 停止服务
sudo systemctl stop mission-control
sudo systemctl disable mission-control
sudo systemctl daemon-reload

# 2. 删除服务文件
sudo rm /etc/systemd/system/mission-control.service

# 3. 删除项目目录（⚠️ 会丢失数据）
rm -rf /root/.openclaw/workspace-tech/mission-control

# 4. 清理 systemd 缓存
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

---



## 支持与反馈

- **源码仓库**: https://github.com/TianyiDataScience/openclaw-control-center
- **Issue 提交**: 在仓库 Issues 页面描述问题
- **文档更新**: 本指南应随版本更新，重大变更请同步更新 `experience-mission-control.md`

---

## 📝 安装检查清单

部署完成后，逐项检查：

- [ ] ✅ Node.js v22+ 已安装
- [ ] ✅ pnpm 已安装
- [ ] ✅ 项目克隆到 `~/.openclaw/workspace-tech/mission-control`
- [ ] ✅ `.env.local` 已配置（ADMIN_PASSWORD, AUTH_SECRET）
- [ ] ✅ `.env.minimal` 已创建（无注释）
- [ ] ✅ `pnpm install` 完成
- [ ] ✅ `pnpm build` 成功
- [ ] ✅ systemd service 文件已更新路径
- [ ] ✅ `sudo systemctl daemon-reload` 执行
- [ ] ✅ `sudo systemctl start mission-control` 成功
- [ ] ✅ `sudo systemctl status mission-control` 显示 active (running)
- [ ] ✅ `curl http://localhost:3000/api/health` 返回 JSON
- [ ] ✅ 浏览器访问 http://localhost:3000 显示登录页
- [ ] ✅ 使用 ADMIN_PASSWORD 登录成功
- [ ] ✅ 修改默认密码
- [ ] ✅ （可选）配置 HTTPS 和防火墙

---

**文档维护**: `~/.openclaw/workspace-tech/memory/experience-mission-control.md`
**最后验证**: 2026-04-02 13:30，Mission Control v1.0 正常运行于 workspace-tech





## 🔧 Next.js 编译时本地化工程（2026-04-02）

### 🎯 问题场景

需要将 Mission Control 的 UI 语言从中文切换到英文。

### 🔍 技术调研

1. **翻译架构**:
   - 所有翻译定义在 `src/config/locale.ts` 的 `TRANSLATIONS` 对象
   - `getLanguage()` 函数: `return (process.env.NEXT_PUBLIC_LANGUAGE as Language) || 'zh'`
   - 默认语言是 `'zh'`，不是 `'en'`

2. **Next.js 变量机制**:
   - `NEXT_PUBLIC_*` 环境变量在**构建时**注入客户端
   - 修改 `.env.local` 后必须 `npm run build` 才能生效
   - 运行时修改环境变量无效（已编译进静态 JS）

3. **systemd EnvironmentFile 限制**:
   - 不支持注释行（`#` 开头）
   - 不支持空行
   - 不支持 `export` 关键字
   - 必须格式: `KEY=value` 或 `KEY=value with spaces`

### 🛠️ 实施路径

```
1. 设置环境变量 → 2. 重新构建 → 3. 重启服务 → 4. 客户端验证
```

**步骤详解**:

**Step 1**: 纯净环境文件

```bash
# .env.minimal (无注释)
NEXT_PUBLIC_LANGUAGE=en
```

**Step 2**: 更新 systemd service

```ini
EnvironmentFile=/root/.openclaw/workspace-tech/mission-control/.env.minimal
```

**Step 3**: 清理并构建

```bash
rm -rf .next
npm run build
# 验证: grep "Overview of agent activity" .next/static/chunks/*.js
```

**Step 4**: 重启服务

```bash
sudo systemctl restart mission-control
```

**客户端**: 强制刷新浏览器 (Ctrl+F5 / Cmd+Shift+R)

### 🧪 验证方法

1. **构建验证**:

   ```bash
   grep -r "Overview of agent activity" .next/static/
   # ✅ 应找到英文本地化字符串
   ```

2. **运行时验证**:

   - 打开浏览器控制台

   ```javascript
   typeof t === 'function' && t('dashboard.welcome')
   # 应返回 "Overview of agent activity"
   ```

3. **视觉验证**:

   - 访问 http://localhost:3000
   - 检查仪表板欢迎语

### ⚠️ 常见陷阱与解决

| 陷阱                 | 症状                   | 解决                                    |
| -------------------- | ---------------------- | --------------------------------------- |
| 未重新构建           | 欢迎语仍是中文         | `npm run build`                         |
| EnvironmentFile 无效 | 环境变量未加载         | 创建无注释 `.env.minimal`               |
| 浏览器缓存           | 服务已更新但仍显示中文 | 强制刷新或使用无痕窗口                  |
| 路径错误             | 修改了错误项目的配置   | 确认在 `workspace-tech/mission-control` |

### 📊 性能数据

- 构建时间: ~11.8s (Turbopack)
- 静态页面生成: 60/60 页面, ~707ms
- 服务重启: ~2s
- 总耗时: ~15s (不含浏览器缓存)

### 🎓 核心要点

1. **编译时 vs 运行时**: Next.js 的 `NEXT_PUBLIC_*` 是编译时注入，修改需重建
2. **环境变量优先级**: `.env.local` > `.env.minimal` > systemd EnvironmentFile
3. **systemd 限制**: EnvironmentFile 不支持注释，需纯净版
4. **验证链**: 构建文件 → 服务环境 → 浏览器缓存 → 最终用户

---

## 🔗 相关条目

### 强关联
- [[docker-compose]] - Mission Control使用Docker Compose部署
- [[openclaw-control-center-dashboard]] - Control Center与Mission Control同为Dashboard
- [[2026-04-01]] - Mission Control安装部署
- [[2026-04-04]] - 服务迁移标准化

### 中关联
- [[bash-deploy]] - 部署脚本开发
- [[memory-system]] - Mission Control监控记忆系统状态

### 弱关联
- [[2026-03-31]] - 备份体系涉及Mission Control

---
*图谱关联最后更新: 2026-05-07*
