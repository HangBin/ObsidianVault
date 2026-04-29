---
author: tech agent
created: 2026-04-09 16:10:33
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
source: tech agent memory/experience-control-center.md
tags: [tech-agent, experience, knowledge,openclaw-control-enter]
---

# OpenClaw Control Center 部署经验

## 部署位置
- 源码目录：`/home/openclaw-control-center`
- 用户源码：`/home/bill/openclaw-control-center`

## 环境配置步骤

### 1. 复制源码
```bash
cp -r /home/bill/openclaw-control-center /home/openclaw-control-center
```

### 2. 配置 .env
```bash
cp .env.example .env
# 修改 GATEWAY_URL
sed -i 's|GATEWAY_URL=ws://127.0.0.1:18789|GATEWAY_URL=ws://192.168.1.210:18789|' .env
# 添加 API Token
echo "LOCAL_API_TOKEN=occtrl_$(openssl rand -hex 16)" >> .env
# 绑定外部地址（关键！）
sed -i 's|# UI_BIND_ADDRESS=0.0.0.0|UI_BIND_ADDRESS=0.0.0.0|' .env
```

### 3. 安装依赖
```bash
pnpm install
```

### 4. 启动服务
```bash
# 正确方式（解决 nohup 环境变量问题）
cd /home/openclaw-control-center
nohup env UI_MODE=true node --import tsx src/index.ts > /tmp/occ.log 2>&1 &
```

## 关键教训

### 1. UI 绑定地址问题
- **现象**：服务启动后 localhost 可访问，但 192.168.1.210:4310 无法访问
- **根因**：UI 默认绑定 127.0.0.1，未绑定到外部网卡
- **解决**：在 .env 中添加 `UI_BIND_ADDRESS=0.0.0.0`

### 2. nohup 环境变量问题
- **错误**：`nohup UI_MODE=true node ...` → "没有那个文件或目录"
- **根因**：nohup 把 `UI_MODE=true` 当作可执行文件
- **解决**：使用 `env UI_MODE=true node ...`

### 3. 部署后必须验证
- 部署完成后必须从外部 IP 验证访问
- 命令：`curl -s -o /dev/null -w "%{http_code}" http://192.168.1.210:4310/`

## 配置参数说明
| 参数 | 说明 |
|------|------|
| GATEWAY_URL | WebSocket 地址，连接 OpenClaw Gateway |
| UI_BIND_ADDRESS | 0.0.0.0 允许外部访问 |
| LOCAL_API_TOKEN | API 认证令牌 |
| UI_MODE=true | 启动 UI 模式 |
| READONLY_MODE | 只读模式开关 |

## 端口
- UI 端口：4310
- Gateway：18789

---
创建时间：2026-04-09