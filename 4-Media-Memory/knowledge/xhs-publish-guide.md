---
title: 小红书发布经验指南
date: 2026-06-08
tags:
  - xiaohongshu
  - publish
  - experience
  - cookie
  - api
---

# 小红书发布经验指南

## 概述

本文档记录小红书发布的完整经验，包括 Cookie 管理、API 调用、CLI 使用、常见问题排查。

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

### 1.3 Cookie 更新方式

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

- xhs 的 Cookie TTL 为 7 天（`_COOKIE_TTL_SECONDS = 7 * 86400`）
- 过期后 xhs 会尝试从浏览器刷新（`browser_cookie3`）
- 刷新失败则仍然使用旧 Cookie，但 API 调用会报"登录已过期"
- **写操作（发布/草稿）对 Cookie 更敏感**，读操作可能在 Cookie 过期后仍能工作

### 1.5 获取新 Cookie

```bash
# 方式1: 扫码登录
xhs login

# 方式2: 从浏览器提取
# 在浏览器打开 https://www.xiaohongshu.com
# F12 → Application → Cookies → 复制 a1 和 web_session
```

## 2. 发布流程

### 2.1 CLI 发布（推荐）

```bash
# 基本发布
xhs post \
  --title "笔记标题" \
  --body "笔记正文内容" \
  --images /path/to/image.jpg \
  --json

# 带话题
xhs post \
  --title "笔记标题" \
  --body "笔记正文内容" \
  --images /path/to/image.jpg \
  --topic "话题关键词" \
  --json

# 私密发布
xhs post \
  --title "笔记标题" \
  --body "笔记正文内容" \
  --images /path/to/image.jpg \
  --private \
  --json
```

### 2.2 发布返回值

```json
{
  "ok": true,
  "schema_version": "1",
  "data": {
    "id": "6a267d1a0000000021021fca",
    "score": 10
  }
}
```

- `data.id`: 笔记 ID
- `data.score`: 质量评分

### 2.3 Python API 发布

```python
import json, sys
sys.path.insert(0, "/root/.agent-reach-venv/lib/python3.11/site-packages")
from xhs_cli.client import XhsClient
from xhs_cli.cookies import get_cookies

browser, cookies = get_cookies("saved")
client = XhsClient(cookies, timeout=30.0, request_delay=0.5)

# 需要先上传图片获取 file_id
permit = client.get_upload_permit()
client.upload_file(permit["fileId"], permit["token"], "/path/to/image.jpg")

# 发布
result = client.create_image_note(
    title="笔记标题",
    desc="笔记正文",
    image_file_ids=[permit["fileId"]],
    topics=[],
    is_private=False,
)
```

## 3. 阅读笔记

### 3.1 CLI 读取（必须加 --xsec-token）

```bash
# ❌ 错误：不加 --xsec-token 返回空数据
xhs read "笔记ID" --json

# ✅ 正确：加 --xsec-token
xhs read "笔记ID" --xsec-token "xsec_token值" --json

# 从 my-notes 获取 xsec_token
xhs my-notes --json
# 返回中的 xsec_token 字段即可用于 read
```

### 3.2 Python API 读取

```python
# 需要 xsec_token
result = client.get_note_detail(
    "笔记ID",
    xsec_token="xsec_token值",
    xsec_source="pc_feed"
)
```

### 3.3 搜索获取 xsec_token

```bash
# 搜索结果的 items 中包含 xsec_token
xhs search "关键词" --json
# 返回的 items[0].xsec_token 可用于 read
```

## 4. 其他操作

### 4.1 搜索

```bash
xhs search "关键词" --json
xhs hot --json
xhs feed --json
```

### 4.2 评论

```bash
xhs comments "笔记ID" --json
```

### 4.3 我的笔记

```bash
xhs my-notes --json
```

### 4.4 用户信息

```bash
# Python API
info = client.get_self_info()
# 返回: nickname, user_id, red_id, desc 等
```

## 5. 错误码与排查

### 5.1 常见错误码

| 错误码 | 消息 | 原因 | 解决方案 |
|--------|------|------|----------|
| `-100` | 登录已过期 | Cookie 失效 | 更新 a1 + web_session |
| `-9150` | 技术升级中，暂时无法发布 | 小红书平台维护 | 等待后重试 |
| `-9110` | 笔记图片无法正常访问 | image_file_ids 无效 | 先上传图片获取有效 file_id |
| `Captcha` | 验证码触发 | 服务器 IP 被风控 | 降低频率 / 使用代理 |

### 5.2 排查流程

```
发布失败 →
  1. 检查 Cookie 是否过期 → 更新 a1 + web_session
  2. 检查 API 返回错误码 → -100 需刷新 Cookie，-9150 需等待
  3. 检查 image_file_ids 是否有效 → 先 upload_file 获取有效 ID
  4. 检查是否触发 Captcha → 降低频率
```

## 6. 注意事项

### 6.1 IP 风控

- 服务器 IP 访问小红书 API 可能触发验证码
- 读操作（search/hot/feed）一般不受影响
- 写操作（post/like/comment）更容易触发
- **控制操作频率**，避免短时间内大量调用

### 6.2 Cookie 安全

- Cookie 文件权限: `chmod 600`
- 不要在日志或输出中暴露完整 Cookie 值
- 定期更新 Cookie（建议每 7 天）

### 6.3 发布限制

- 自动发布存在平台反机器人检测
- 建议发布间隔 > 60 秒
- 图片需先上传到小红书 CDN 再发布
- 草稿箱 API (`/api/galaxy/creator/note/draft`) 与发布 API 不同，需要额外参数

### 6.4 数据读取

- `read` 命令必须加 `--xsec-token`，否则返回空数据
- `my-notes` 返回的列表包含 `xsec_token`，可直接用于 `read`
- `search` 返回的 items 也包含 `xsec_token`

## 7. 环境信息

| 项目 | 值 |
|------|-----|
| xhs CLI 路径 | `/root/.agent-reach-venv/bin/xhs` |
| xhs 版本 | 0.6.4 |
| Cookie 路径 | `/root/.xiaohongshu-cli/cookies.json` |
| Python 包路径 | `/root/.agent-reach-venv/lib/python3.11/site-packages/xhs_cli/` |
| MCP server | `/root/.openclaw/workspace-media/xhs-mcp-server/server.mjs` |
| MCP 注册名 | `xhs-mcp` |
| 当前用户 | 小红薯65103A5F (red_id: 5173229140) |

## 8. 经验教训

### ✅ 已验证

1. **Cookie 更新到正确路径**: 必须更新 `~/.xiaohongshu-cli/cookies.json`，不是工作区的 `.config/` 目录
2. **read 必须加 xsec-token**: 这是最容易被忽略的参数
3. **发布是真实成功的**: CLI 返回的 ID 和 my-notes 确认一致
4. **Python API 和 CLI 结果一致**: 同样的 Cookie 在两种方式下行为一致

### 🚨 踩坑记录

1. **误判发布失败**: 因为 read 不加 xsec-token 返回空数据，误以为发布失败
2. **Cookie 路径错误**: 更新到工作区的 `.config/` 目录无效
3. **草稿箱 API 不同**: `_creator_post` 和 `_main_api_post` 的认证方式不同
