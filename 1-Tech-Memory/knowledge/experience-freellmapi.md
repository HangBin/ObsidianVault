---
author: tech agent
created: 2026-06-20 16:15:00 GMT+8
modified: 2026-06-20 16:15:00 GMT+8
version: v1.0.0
source: tech agent memory/2026-06-20.md
tags: [tech-agent, experience, knowledge, freellmapi, install, nodejs, gcc]
---

# FreeLLMAPI 安装部署经验

> **项目地址**: https://github.com/tashfeenahmed/freellmapi
> **安装路径**: `/home/freellmapi`
> **版本**: v0.2.1
> **日期**: 2026-06-20

---

## 1. 项目概述

FreeLLMAPI 是一个 OpenAI 兼容的 LLM 代理聚合工具，将 16 个免费 Provider 的 API 聚合到一个 `/v1/chat/completions` 端点。

**核心功能：**
- OpenAI 兼容 API（`/v1/chat/completions`、`/v1/models`）
- 智能路由 + 自动故障转移
- 16 个免费 Provider（~1.7B tokens/月）
- 加密密钥存储（AES-256-GCM）
- React + Vite Dashboard
- 健康检查 + 分析统计

---

## 2. 安装方式选择

### Docker 方式（推荐，如果已安装 Docker）
```bash
curl -fsSL https://freellmapi.co/install.sh | bash
```
或手动：
```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
ENCRYPTION_KEY="$(openssl rand -hex 32)"
printf "ENCRYPTION_KEY=***\nPORT=3001\n" "$ENCRYPTION_KEY" > .env
docker compose up -d
```

### npm 源码方式（本环境使用）
```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
npm install
cp .env.example .env
ENCRYPTION_KEY="$(node -e 'console.log(require("crypto").randomBytes(32).toString("hex"))')"
printf "ENCRYPTION_KEY=***\nPORT=3001\n" "$ENCRYPTION_KEY" > .env
npm run dev
```

---

## 3. 编译踩坑：better-sqlite3 + GCC

### 问题
`better-sqlite3` 需要 C++20 编译，系统自带 GCC 9.4 不支持：
```
g++: error: unrecognized command line option '-std=c++20'; did you mean '-std=c++2a'?
```

### 解决方案
安装 GCC 10 并用环境变量指定编译器：
```bash
apt-get install -y gcc-10 g++-10
cd /home/freellmapi
CC=gcc-10 CXX=g++-10 npm install
```

### 注意事项
- 无 Docker 时只能走 npm 源码方式
- 系统最高只有 GCC 10（apt 源里没有 GCC 12），但 GCC 10 已支持 C++20
- `npm install` 进程容易被超时 SIGKILL，需要给足够超时时间
- **不要用管道 `| tail -20`**，会导致 exit code 被掩盖，建议用 `2>&1; echo "EXIT_CODE=$?"` 方式

---

## 4. 依赖安装注意事项

### npm workspace 模式
项目使用 npm workspaces（`shared`、`server`、`client` 三个子包），`npm install` 会自动处理所有子包依赖。

### 安装超时处理
```bash
# 推荐：不用管道，直接运行
cd /home/freellmapi && CC=gcc-10 CXX=g++-10 npm install 2>&1; echo "EXIT=$?"
```

### 清理重试
```bash
rm -rf node_modules package-lock.json
CC=gcc-10 CXX=g++-10 npm install
```

---

## 5. .env 配置

```bash
ENCRYPTION_KEY=<64位hex密钥>
PORT=3001
HOST_BIND=0.0.0.0           # 局域网访问需要
DASHBOARD_ORIGINS=http://192.168.1.210:5173  # 额外 CORS 白名单
```

### 生成加密密钥
```bash
node -e 'console.log(require("crypto").randomBytes(32).toString("hex"))'
```

---

## 6. 服务启动

### 开发模式
```bash
cd /home/freellmapi && npm run dev
```
- API: `http://[::]:3001`
- Dashboard: `http://localhost:5173`

### 端口冲突处理
```bash
fuser -k 3001/tcp 2>/dev/null
fuser -k 5173/tcp 2>/dev/null
```

### 生产构建
```bash
npm run build
node server/dist/index.js
```

---

## 7. Dashboard 配置

### 首次注册
```bash
curl -X POST http://localhost:3001/api/auth/setup \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'
```
- 密码要求至少 8 位
- 返回 token 用于后续 API 调用

### 登录
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'
```
返回 `token`，用于 `/api/*` 路由的认证。

---

## 8. 上游 Provider Key 管理

### 添加 Key（通过 API）
```bash
curl -X POST http://localhost:3001/api/keys \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <login-token>" \
  -d '{"platform":"openrouter","key":"sk-or-...","label":"My Key"}'
```

### 平台枚举值
`cerebras`, `cloudflare`, `cohere`, `github`, `google`, `groq`, `huggingface`, `kilo`, `llm7`, `mistral`, `nvidia`, `ollama`, `opencode`, `openrouter`, `pollinations`, `zhipu`

### Keyless Provider（无需 API Key）
以下 Provider 支持匿名访问，但仍需在 `api_keys` 表插入 sentinel 记录：
- **Pollinations** — `openai-fast`（GPT-OSS 20B），匿名但有并发限制（1 并发/IP）
- **LLM7** — `codestral-latest` 等，匿名
- **Kilo Gateway** — `poolside/laguna-m.1:free` 等，匿名

### Keyless Sentinel 插入方法
由于 API 认证限制，需要通过 Node.js 脚本直接操作数据库：
```javascript
const db = require("better-sqlite3")("server/data/freeapi.db");
const crypto = require("crypto");
// 读取 .env 中的 ENCRYPTION_KEY
const ENCRYPTION_KEY = "..."; // 从 .env 读取

function encrypt(text) {
  const ALGORITHM = "aes-256-gcm";
  const key = Buffer.from(ENCRYPTION_KEY, "hex");
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  const authTag = cipher.getAuthTag().toString("hex");
  return { encrypted, iv: iv.toString("hex"), authTag };
}

for (const platform of ["pollinations", "llm7", "kilo"]) {
  const e = encrypt("no-key");
  db.prepare(
    "INSERT INTO api_keys (platform, label, encrypted_key, iv, auth_tag, status, enabled) VALUES (?, ?, ?, ?, ?, ?, ?)"
  ).run(platform, platform + "-keyless", e.encrypted, e.iv, e.authTag, "healthy", 1);
}
```

### 验证 Key 有效性
```bash
# 直接调用 Provider API 验证
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer <your-key>"
```

---

## 9. 局域网访问配置

### Vite Dashboard 局域网访问
修改 `client/vite.config.ts`：
```typescript
server: {
  host: '0.0.0.0',    // 监听所有接口
  port: 5173,
  proxy: { ... }
}
```

### API 服务局域网监听
在 `.env` 中添加：
```
HOST_BIND=0.0.0.0
```

### CORS 白名单
在 `.env` 中添加：
```
DASHBOARD_ORIGINS=http://192.168.1.210:5173
```

### 验证
```bash
curl -4 http://localhost:5173/          # IPv4
curl -4 http://192.168.1.210:5173/    # 局域网 IP
curl -s -I -H "Origin: http://192.168.1.210:5173" http://localhost:3001/api/auth/status \
  | grep access-control-allow-origin
```

---

## 10. API 使用示例

### Python
```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="freellmapi-...",
)
resp = client.chat.completions.create(
    model="auto",  # 自动路由
    messages=[{"role": "user", "content": "你好"}]
)
print(resp.choices[0].message.content)
```

### curl
```bash
curl http://localhost:3001/v1/chat/completions \
  -H "Authorization: Bearer <unified-key>" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"hi"}]}'
```

### 可用模型列表
```bash
curl http://localhost:3001/v1/models \
  -H "Authorization: Bearer <unified-key>"
```

---

## 11. 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `g++: error: unrecognized command line option '-std=c++20'` | GCC 版本过低 | 安装 gcc-10/g++-10 |
| npm install 超时 | 下载依赖慢 | 增大超时，不用管道 |
| `EADDRINUSE: address already in use` | 端口被残留进程占用 | `fuser -k <port>/tcp` |
| `All models rate-limited` | 所有 Provider Key 无效或无限 keyless sentinel | 禁用无效 Key，添加 keyless sentinel |
| `Invalid API key` | 统一 Key 不匹配 | 检查 settings 表的 unified_api_key |
| Dashboard 无法局域网访问 | Vite 默认只监听 localhost | 添加 `host: '0.0.0.0'` |
| `Better-sqlite3` 目录不存在 | 编译时目录创建失败 | 手动创建或重 npm install |

---

## 12. 关键路径速查

| 项目 | 路径 |
|------|------|
| 项目根目录 | `/home/freellmapi` |
| 数据库 | `/home/freellmapi/server/data/freeapi.db` |
| 加密密钥 | `.env` 中的 `ENCRYPTION_KEY` |
| 统一 API Key | DB `settings` 表 `unified_api_key` |
| Dashboard 端口 | 5173 (dev) / 3001 (prod) |
| API 端口 | 3001 |
| 日志 | `npm run dev` 控制台输出 |
| 模型目录 | DB `models` 表 |
| Fallback 配置 | DB `fallback_config` + `profile_models` 表 |
