---
title: 小红书发布经验指南
date: 2026-06-10
last_updated: 2026-06-15 (10:59)
tags:
  - xiaohongshu
  - publish
  - experience
  - cookie
  - xhs-cli
  - anti-crawl
author: media
---

# 小红书发布经验指南

> **⚡ 快速开始：**
> ```bash
> xhs post --title "标题" --body "正文" --images /path/to/img.jpg --json
> ```
> Cookie 检查：`xhs my-notes --json`（能返回笔记列表 = 登录态有效）

---

## 1. Cookie 管理

### 1.1 Cookie 文件位置

**xhs CLI 实际读取路径**: `~/.xiaohongshu-cli/cookies.json`（不是工作区的 `.config/xiaohongshu-cli/`）

```bash
# 正确路径
/root/.xiaohongshu-cli/cookies.json

# 错误路径（xhs 不读这里）
~/.openclaw/workspace-media/.config/xiaohongshu-cli/cookies.json
```

### 1.2 Cookie 字段说明

| 字段 | 说明 | 必需 |
|------|------|------|
| `a1` | 主认证 token（52字符） | ✅ |
| `web_session` | 会话 token（38字符） | ✅ |
| `id_token` | ID token（136字符） | ✅ |
| `x-rednote-datactry` | 地区代码 | ✅ |
| `x-rednote-holderctry` | 持有地区 | ✅ |
| `saved_at` | 保存时间戳（自动管理） | ✅ |

### 1.3 Cookie 更新

```python
import json, time

cookies_path = "/root/.xiaohongshu-cli/cookies.json"
with open(cookies_path) as f:
    cookies = json.load(f)

cookies["a1"] = "新的a1值"
cookies["web_session"] = "新的web_session值"
cookies["saved_at"] = int(time.time())

with open(cookies_path, "w") as f:
    json.dump(cookies, f, indent=2)
```

### 1.4 Cookie 过期判断

- Cookie TTL 为 7 天
- 过期后 API 调用报"登录已过期"（错误码 `-100`）
- **写操作对 Cookie 更敏感**，读操作可能过期后仍能工作

### 1.5 获取新 Cookie

```bash
# 方式1: 扫码登录
xhs login

# 方式2: 从浏览器提取
# 打开 https://www.xiaohongshu.com → F12 → Application → Cookies → 复制 a1 和 web_session
```

---

## 2. 发布流程

### 2.1 CLI 发布

```bash
# 基本发布
xhs post --title "笔记标题" --body "笔记正文" --images /path/to/image.jpg --json

# 带话题
xhs post --title "标题" --body "正文" --images /path/to/img.jpg --topic "话题关键词" --json

# 私密发布
xhs post --title "标题" --body "正文" --images /path/to/img.jpg --private --json
```

### 2.2 发布返回值

```json
{
  "ok": true,
  "data": { "id": "6a267d1a...", "score": 10 }
}
```

### 2.3 Python API 发布

```python
import json, sys
sys.path.insert(0, "/root/.agent-reach-venv/lib/python3.11/site-packages")
from xhs_cli.client import XhsClient
from xhs_cli.cookies import get_cookies

browser, cookies = get_cookies("saved")
client = XhsClient(cookies, timeout=30.0, request_delay=0.5)

# 先上传图片获取 file_id
permit = client.get_upload_permit()
client.upload_file(permit["fileId"], permit["token"], "/path/to/image.jpg")

# 发布
result = client.create_image_note(
    title="笔记标题", desc="笔记正文",
    image_file_ids=[permit["fileId"]], topics=[], is_private=False,
)
```

---

## 3. 阅读笔记

### 3.1 CLI 读取（必须加 --xsec-token）

```bash
# ❌ 不加 --xsec-token 返回空数据
xhs read "笔记ID" --json

# ✅ 加 --xsec-token
xhs read "笔记ID" --xsec-token "xsec_token值" --json

# 从 my-notes 获取 xsec_token
xhs my-notes --json
```

### 3.2 搜索获取 xsec_token

```bash
xhs search "关键词" --json
# 返回的 items[0].xsec_token 可用于 read
```

---

## 4. 其他操作

```bash
xhs search "关键词" --json    # 搜索
xhs hot --json                 # 热门
xhs feed --json                # 推荐
xhs comments "笔记ID" --json   # 评论
xhs my-notes --json            # 我的笔记
```

---

## 5. 错误码与排查

| 错误码 | 消息 | 原因 | 解决方案 |
|--------|------|------|----------|
| `-100` | 登录已过期 | Cookie 失效 | 更新 a1 + web_session |
| `-9150` | 技术升级中 | 平台维护 | 等待后重试 |
| `-9110` | 图片无法访问 | image_file_ids 无效 | 先上传图片获取有效 file_id |
| `Captcha` | 验证码触发 | IP 被风控 | 降低频率 / 使用代理 |

---

## 6. 反爬机制（2026-06-10）

### 6.1 五层防线

| 层级 | 机制 | 绕过方案 |
|------|------|---------|
| 1️⃣ TLS 指纹 | JA3/JA4 识别 Python | `curl_cffi` 伪装 Chrome |
| 2️⃣ 请求签名 | x-s / x-t / x-s-common | `xhshow` 库生成 |
| 3️⃣ IP 限流 | 数据中心 IP 拦截 | 住宅代理 |
| 4️⃣ SPA 渲染 | 需浏览器执行 JS | Playwright / 补环境 |
| 5️⃣ 登录墙 | xsec_token / web_session | 登录态 Cookie |

### 6.2 xhs-cli 绕过策略

| 操作 | 是否需要签名 |
|------|-------------|
| 搜索 | ✅ 需要 x-s |
| 读取笔记 | ❌ 走 HTML 解析完全绕过 |
| 发布笔记 | ✅ 需要创作者签名 |
| 点赞/收藏 | ✅ 需要 x-s |

**关键**: 读取笔记走 HTML 解析（SSR 渲染），完全绕过 API 签名！

### 6.3 反检测措施

1. **TLS 指纹**: `pip install curl_cffi` → `impersonate="chrome120"`
2. **请求间隔**: 2-3 秒/请求（搜索），10-20 请求/分钟/IP
3. **住宅代理**: 中国地理位置住宅 IP

---

## 7. 注意事项

### 7.1 IP 风控

- 服务器 IP 可能触发验证码
- 写操作（post/like/comment）更容易触发
- 控制操作频率，避免短时间内大量调用

### 7.2 Cookie 安全

- 文件权限: `chmod 600`
- 不要在日志中暴露完整 Cookie 值
- 定期更新（建议每 7 天）

### 7.3 发布限制

- 发布间隔 > 60 秒
- 图片需先上传到小红书 CDN 再发布
- 草稿箱 API 与发布 API 不同

---

## 8. 环境信息

| 项目 | 值 |
|------|-----|
| xhs CLI 路径 | `/root/.agent-reach-venv/bin/xhs` |
| xhs 版本 | 0.6.4 |
| Cookie 路径 | `/root/.xiaohongshu-cli/cookies.json` |
| Python 包路径 | `/root/.agent-reach-venv/lib/python3.11/site-packages/xhs_cli/` |
| MCP server | `/root/.openclaw/workspace-media/xhs-mcp-server/server.mjs` |
| MCP 注册名 | `xhs-mcp` |
| 当前用户 | 小红薯65103A5F (red_id: 5173229140) |

---

## 9. 经验教训

### ✅ 已验证

1. Cookie 必须更新到 `~/.xiaohongshu-cli/cookies.json`，不是 `.config/` 目录
2. `read` 必须加 `--xsec-token`，否则返回空数据
3. CLI 和 Python API 结果一致

### 🚨 踩坑记录

1. **误判发布失败**: read 不加 xsec-token 返回空，误以为发布失败
2. **Cookie 路径错误**: 更新到 `.config/` 目录无效
3. **草稿箱 API 不同**: `_creator_post` 和 `_main_api_post` 认证方式不同
