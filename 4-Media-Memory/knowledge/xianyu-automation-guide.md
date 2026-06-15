---
title: 闲鱼自动化经验指南
date: 2026-06-10
last_updated: 2026-06-15 (10:44)
tags:
  - xianyu
  - goofish
  - publish
  - experience
  - cdp
  - browser-automation
  - xvfb
  - automation
author: media
---

# 闲鱼自动化经验指南

> **⚡ 快速开始：每次发布只需一条命令：**
> ```bash
> bash /home/bill/run.sh --image /path/to/img.png --desc '描述' --price 0.01
> ```
> 先检查登录态：`bash /home/bill/run.sh --check`

---

## 1. 快速启动指南（⭐ 每次必读）

### 1.1 标准发布流程（3 步）

```
Step 1: 检查登录态
  bash /home/bill/run.sh --check

Step 2a: 登录态正常 → 直接发布
  bash /home/bill/run.sh --image /path/to/img.png --desc '描述' --price 0.01

Step 2b: 登录态失效 → 截图二维码 → 发给用户扫码 → 等确认 → 再发布
```

**铁律：先检查 → 失效就发二维码 → 不做多余分析**

### 1.2 run.sh 命令速查

```bash
# 发布商品
bash /home/bill/run.sh --image /path/to/img.png --desc '商品描述' --price 0.01

# 仅检查登录态
bash /home/bill/run.sh --check

# 使用配置文件（/home/bill/config.json）
bash /home/bill/run.sh --config product.json

# 批量发布
bash /home/bill/run.sh --batch products.json
```

### 1.3 配置文件示例

```json
{
  "image": "/path/to/img.png",
  "desc": "商品描述",
  "price": 99
}
```

---

## 2. 脚本架构

| 文件 | 功能 | 说明 |
|------|------|------|
| `/home/bill/run.sh` | **一键入口** | 启动 Chrome → 注入 cookies → 检查登录态 → 发布 |
| `/home/bill/xianyu_start.sh` | Chrome 启动脚本 | xvfb-run 启动 Chrome（被 run.sh 内部调用） |
| `/home/bill/xianyu_publish.py` | 发布核心 | CDP 自动化：上传图片 → 填写信息 → 发布 |

**run.sh 自动完成全流程，不需要单独跑 xianyu_start.sh 或 xianyu_publish.py。**

---

## 3. 登录态管理

### 3.1 登录态检查

```bash
bash /home/bill/run.sh --check
```

输出：
- `✅ 登录态正常` → 直接发布
- `⚠️ 需要登录` → 需要用户扫码

### 3.2 登录态恢复（自动）

run.sh 启动 Chrome 时会自动注入 session cookies（从 `/tmp/xianyu_cookies.txt`）。
**大部分情况下 cookies 注入即可恢复登录态，不需要用户扫码。**

### 3.3 登录态过期（需用户扫码）

当 cookies 彻底过期时：

1. run.sh 已自动启动 Chrome（CDP 端口 9222）
2. 导航到登录页并截图二维码
3. 用 `message` 工具发送截图给用户
4. 等待用户扫码确认
5. 刷新页面验证登录态 → 继续发布

### 3.4 截图二维码标准方式

```python
python3 << 'PYEOF'
import json, websocket, urllib.request, base64, time

tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read())
page_tab = [t for t in tabs if t.get("type") == "page"][0]
ws = websocket.create_connection(page_tab["webSocketDebuggerUrl"], timeout=15)

# 导航到登录页
ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://www.goofish.com/login"}}))
ws.recv()
time.sleep(5)

# 截图（二维码在右侧，clip x 从 250 开始，scale=2 放大）
ws.send(json.dumps({"id":2,"method":"Page.captureScreenshot","params":{
    "format": "png",
    "clip": {"x": 250, "y": 100, "width": 500, "height": 600, "scale": 2}
}}))
resp = json.loads(ws.recv())
img_data = base64.b64decode(resp["result"]["data"])
with open("/tmp/xianyu_qrcode.png", "wb") as f:
    f.write(img_data)
ws.close()
PYEOF
```

```python
# 发送给用户
message(action="send", message="🔑 请用闲鱼 APP 扫码登录\n\nMEDIA:/tmp/xianyu_qrcode.png")
```

**⚠️ 注意**：
- 用 `MEDIA:` 前缀发原图，**不要用 OCR 识别后再发**
- 截图区域要包含完整二维码（右侧弹窗区域，x 从 250 开始）

### 3.5 Cookie 文件位置

| 文件 | 说明 |
|------|------|
| `/tmp/xianyu_cookies.txt` | 最新完整 cookie string（CDP 提取） |
| `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt` | 持久化备份 |
| `/root/.openclaw/workspace-media/.config/xianyu_cookies_latest.txt` | 最新提取 |

---

## 4. 发布页面结构（2026-06-15 确认）

| 元素 | 类型 | 操作方式 |
|------|------|---------|
| 图片上传 | input[type=file]（隐藏） | fetch 上传 + React fiber onChange 注入 |
| 宝贝描述 | contenteditable div | innerHTML 注入（**无 emoji**，最大 1500 字符） |
| 价格 | input[placeholder="0.00"] | value setter + input/change 事件 |
| 原价 | input[placeholder="0.00"] | 可选 |
| 分类 | ant-select 下拉 | CDP dispatchKeyEvent 逐字输入 |
| 计价方式 | ant-select 下拉 | 同上 |
| 服务类型 | ant-select 下拉 | 同上 |
| 发货设置 | ant-radio | 点击 radio |
| 所在地 | 自动填充 | 需提前在闲鱼设置常用地址 |
| 发布按钮 | button | 文本"发布" |

**⚠️ 闲鱼没有标题输入框！** 商品标题自动从描述中提取。

---

## 5. 关键技术细节

### 5.1 Chrome 启动（xvfb-run）

```bash
xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24" \
  /opt/google/chrome/chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=http://127.0.0.1:9222 \
  --password-store=basic \
  --no-sandbox \
  --disable-gpu \
  --user-data-dir=/home/bill/.config/google-chrome \
  https://www.goofish.com &>/dev/null &
```

**关键**：`xvfb-run --auto-servernum` 自动创建虚拟 X Server 并设置 `DISPLAY`，这是唯一可行的方案。

### 5.2 图片上传（三步法，2026-06-13 验证）

1. **浏览器 fetch 上传**：通过页面 cookies 直接调用 `stream-upload.goofish.com` 获取 fileId
2. **React fiber onChange 注入**：遍历 fiber 树找到上传组件，调用 `onChange({fileList: [...]})`
3. **base64 分块传输**：图片需先分块注入到浏览器内存（chunk_size=50000）

**已验证失败的方法**（不要再试）：
- ❌ DOM.setFileInputFiles — React 不识别
- ❌ Page.handleFileChooserDialog — Chrome 147 不支持
- ❌ fake File 对象 — 闲鱼报"文件类型无法确定"
- ❌ base64 + change 事件 — React 不识别

### 5.3 Ant Design Select 操作

**唯一可行方案**：CDP `Input.dispatchKeyEvent` 逐字输入

```python
# 1. focus 搜索输入框
# 2. 逐字输入搜索关键词
for char in '关键词':
    cdp('Input.dispatchKeyEvent', {
        'type': 'keyDown', 'text': char, 'key': char, 'code': '',
        'windowsVirtualKeyCode': ord(char), 'nativeVirtualKeyCode': ord(char)
    })
    cdp('Input.dispatchKeyEvent', {
        'type': 'keyUp', 'key': char, 'code': '',
        'windowsVirtualKeyCode': ord(char), 'nativeVirtualKeyCode': ord(char)
    })
# 3. 等 2-3 秒，下拉菜单出现
# 4. 点击目标选项（textContent.trim() === '目标' && children.length === 0）
```

**已验证失败**：DOM click（Ant Design 5 拦截合成事件）、Input.insertText（不响应）

### 5.4 Session Cookies 恢复

Chrome 重启后 session cookies（`cookie2`、`XSRF-TOKEN` 等）会丢失。run.sh 通过 CDP `Network.setCookie` 自动注入恢复。

---

## 6. 已验证成功案例

| 商品 | 价格 | 商品ID | 日期 | 方式 |
|------|------|--------|------|------|
| DeepSeek V4 API 包月畅用 | ¥4.00 | — | 06-12 | CDP fiber 注入 |
| Claude Opus 4.8 API | ¥0.09 | 1057911158600 | 06-13 | run.sh 一键 |
| Claude Opus 4.8 API（测试） | ¥0.09 | 1057127547428 | 06-13 | run.sh 一键 |
| MacBook Pro M4 Pro 14寸 | ¥8888 | 1059835968742 | 06-13 | run.sh 一键 |
| 周杰伦签名专辑（测试） | ¥888,888 | 1059858208480 | 06-13 | run.sh 一键 |
| 测试商品 | ¥0.01 | — | 06-15 | run.sh 一键 |

---

## 7. 踩坑记录

| 日期 | 问题 | 根因 | 教训 |
|------|------|------|------|
| 06-10 | 签名不一致导致非法请求 | Node.js 手动算 MD5 ≠ execjs | 用 execjs 调用 JS 文件 |
| 06-10 | Cookie 不完整 | 缺少 cookie2/sgcookie | 确保所有字段齐全 |
| 06-12 | fiber 遍历不到上传组件 | 树深度 71 层，BFS 覆盖不全 | 不需要自己写，run.sh 已验证 |
| 06-12 | 描述中包含 emoji | 闲鱼不允许 | 去掉所有 emoji |
| 06-12 | wait_until='networkidle' 超时 | 闲鱼 SPA 永远等不到 | 用 'domcontentloaded' |
| 06-13 | fetch 上传 fileId 为空 | 返回结构嵌套在 object 字段 | `data.get("fileId") or data.get("object",{}).get("fileId")` |
| 06-13 | Ant Design Select 不响应 click | AD5 拦截合成事件 | 用 dispatchKeyEvent 逐字输入 |
| 06-15 | 自己写 CDP 脚本从头分析 | 没先读经验文档 | **先读 run.sh 再动手** |
| 06-15 | 截图没截到二维码 | 裁剪区域在左侧 | 二维码在右侧，x 从 250 开始 |
| 06-15 | 用 OCR 识别二维码再发 | 应该直接发原图 | 用 MEDIA: 发原图 |

---

## 8. 环境信息

| 项目 | 值 |
|------|-----|
| Chrome | google-chrome（非 snap chromium） |
| Chrome 路径 | `/opt/google/chrome/chrome` |
| Chrome Profile | `/home/bill/.config/google-chrome/` |
| CDP 端口 | 9222（google-chrome），9223（snap chromium，不要用） |
| xvfb-run | 已安装 |
| 当前用户 | panbin5218（unb=748552523） |
| 签名 JS | `static/xianyu_js_version_2.js`（API 方向，已弃用） |

---

## 9. 已知限制

1. **登录态会过期**：cookies 过期后需要用户扫码重新登录
2. **不支持批量上传不同图片**：每次发布一个商品，批量模式需要商品列表 JSON
3. **服务器 IP 风控**：机房 IP 可能被闲鱼风控，建议在住宅 IP 环境运行
4. **部分分类不支持网页版发布**：如"其他服务"，需用手机闲鱼 APP 完成

---

## 10. 防重复造轮子清单

> **每次发布前过一遍这个清单，不要做多余的事。**

| ❌ 不要做 | ✅ 正确做法 |
|-----------|-----------|
| 自己写 CDP 脚本分析 fiber 树 | 直接跑 `run.sh` |
| 自己写代码检测登录态 | `run.sh --check` |
| 自己写截图+OCR+发送代码 | 用 `message` + `MEDIA:` 发原图 |
| 自己尝试刷新 cookies | 发二维码让用户扫码 |
| 重新分析 ant-select 操作 | 用 dispatchKeyEvent（已验证） |
| 尝试 API 方式发布 | 用 CDP 浏览器自动化（API 有风控） |

---

## 11. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 一键发布脚本 | `/home/bill/run.sh` | 入口脚本 |
| Chrome 启动脚本 | `/home/bill/xianyu_start.sh` | xvfb-run 启动 |
| 发布核心脚本 | `/home/bill/xianyu_publish.py` | CDP 自动化核心 |
| 浏览器自动化经验 | `/home/obsidian_vault/shared/browser/` | CDP 操作参考 |
| 每日日志 | `memory/2026-06-12.md` | CDP 发布实操 |
| 每日日志 | `memory/2026-06-13.md` | xvfb-run + CDP 实操 |
| 每日日志 | `memory/2026-06-15.md` | run.sh 验证 + 经验更新 |
