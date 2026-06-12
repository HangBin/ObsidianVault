---
title: 闲鱼自动化经验指南
date: 2026-06-10
last_updated: 2026-06-12
tags:
  - xianyu
  - goofish
  - publish
  - experience
  - cookie
  - api
  - anti-crawl
  - signature
  - cdp
  - browser-automation
author: media
---

# 闲鱼自动化经验指南

> 研究时间: 2026-06-10
> 信息来源: XianyuAutoAsync.py 源码分析、Spider_XHS、API 逆向测试

## 概述

本文档记录闲鱼（Goofish）自动化的完整经验，包括 Cookie 管理、API 调用、签名算法、反爬机制、发布流程、风控处理。

## 1. Cookie 管理

### 1.1 数据库位置

```
/root/.openclaw/workspace-media/xianyu-openclaw-channel-main/data/xianyu_data.db
```

### 1.2 Cookie 字段说明

| 字段 | 说明 | 必需 |
|------|------|------|
| `unb` | 用户唯一标识（数字） | ✅ |
| `cookie2` | 登录态核心字段 | ✅ |
| `sgcookie` | 安全验证字段 | ✅ |
| `_m_h5_tk` | H5 签名 token（含时间戳） | ✅ |
| `_m_h5_tk_enc` | H5 token 加密版本 | ✅ |
| `tfstk` | 风控 token | ✅ |
| `tracknick` | 用户昵称 | ✅ |
| `cna` | 设备指纹 | ✅ |
| `x5secdata` / `x5sec` / `x5sectag` | 风控验证字段 | ✅ |
| `cbc` | 加密字段 | ✅ |
| `sca` / `atpsida` / `arms_uid` | 设备指纹字段 | ✅ |

### 1.3 Cookie 获取方式

1. **浏览器 F12**: 登录 goofish.com → Network → 任意 goofish.com 请求 → 右键 Copy as cURL
2. **扫码登录**: 脚本自动打开登录页面，用户手机扫码

### 1.4 Cookie 更新

```python
import sqlite3

conn = sqlite3.connect('data/xianyu_data.db')
cur = conn.cursor()

# 查看现有 Cookie
cur.execute("SELECT id, value, remark, enabled FROM cookies")
for row in cur.fetchall():
    print(f"  id={row[0]}... user={row[2]} enabled={row[3]}")

# 更新 Cookie
cur.execute("""
    UPDATE cookies SET value=?, remark=?, enabled=1
    WHERE id=?
""", (new_cookie_str, 'panbin5218', '748552523'))

conn.commit()
```

### 1.5 Cookie 过期判断

- `_m_h5_tk` 含时间戳（毫秒），过期后 API 返回 `FAIL_SYS_TOKEN_EXOIRED`
- `2207836320265` 已过期（测试确认）
- `748552523` 有效（2026-06-10 测试通过）

## 2. 签名算法（⭐ 核心）

### 2.1 为什么必须用 execjs？

**关键发现**: execjs 调用 JS 文件生成的签名 ≠ Node.js 直接生成的 MD5 签名！

```python
# ❌ 错误方式：Node.js 直接算 MD5
import subprocess
js = 'const crypto=require("crypto");...md5(token+"&"+t+"&"+appKey+"&"+data)...'
r = subprocess.run(['node', f.name], capture_output=True, text=True)
sign = r.stdout.strip()  # 这个签名 API 不认！

# ✅ 正确方式：execjs 调用 JS 文件
import execjs
ctx = execjs.compile(open('static/xianyu_js_version_2.js').read())
sign = ctx.call('generate_sign', t, token, d)  # 这个签名 API 认！
```

**原因**: JS 文件中的 `generate_sign` 不是简单的字符串拼接 + MD5，内部有额外的加密变换逻辑。execjs 完整模拟了 JS 运行环境的各种细节（类型转换、编码等），而 Node.js 手动复现时会丢失这些细节。

### 2.2 签名参数

```python
# 签名输入
t = str(int(time.time() * 1000))  # 毫秒时间戳
token = _m_h5_tk.split('_')[0]    # 取下划线前部分
data = json.dumps(params, separators=(',', ':'))  # 紧凑 JSON，无空格

# 签名调用
sign = ctx.call('generate_sign', t, token, data)
```

### 2.3 appKey

| API | appKey |
|-----|--------|
| 闲鱼 H5 网关 | `34839810` |
| 登录 Token | `444e9908a51d1cb236a27862abc769c9` |

## 3. API 端点

### 3.1 商品列表

```
POST https://h5api.m.goofish.com/h5/mtop.idle.web.xyh.item.list/1.0/

Params:
  jsv=2.7.2
  appKey=34839810
  t=<timestamp>
  sign=<execjs_sign>
  v=1.0
  type=originaljson
  accountSite=xianyu
  dataType=json
  timeout=20000
  api=mtop.idle.web.xyh.item.list
  sessionOption=AutoLoginOnly
  spm_cnt=a21ybx.im.0.0
  spm_pre=a21ybx.collection.menu.1.272b5141NafCNK

Body (form-urlencoded):
  data={"needGroupInfo":false,"pageNumber":0,"pageSize":20,"userId":"<unb>","groupId":"58877261","groupName":"在售","defaultGroup":true}
```

**注意**: pageNumber 从 0 开始（不是 1），pageSize 最大 20（过大返回超限错误）

### 3.2 商品详情

```
POST https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/

Body:
  data={"itemId":"<item_id>"}
```

### 3.3 登录 Token

```
POST https://h5api.m.goofish.com/h5/mtop.taobao.idlemessage.pc.login.token/1.0/

Params 额外字段:
  dangerouslySetWindvaneParams=%5Bobject%20Object%5D
  smToken=token
  queryToken=sm
  sm=sm

Body:
  data={"appKey":"444e9908a51d1cb236a27862abc769c9","deviceId":"xianyu-pc"}
```

**返回**: `accessToken` + `refreshToken` + `accessTokenExpiredTime`（86400000ms = 24h）

### 3.4 请求头

```python
HEADERS = {
    'Cookie': cookie_str,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.goofish.com/',
    'Origin': 'https://www.goofish.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
}
```

## 4. 反爬与风控

### 4.1 错误码

| 错误码 | 消息 | 原因 | 解决方案 |
|--------|------|------|----------|
| `FAIL_SYS_ILLEGAL_ACCESS` | 非法请求 | 签名错误或 Cookie 不完整 | 用 execjs 生成签名；补齐 cookie2/sgcookie |
| `FAIL_SYS_TOKEN_EXOIRED` | 令牌过期 | _m_h5_tk 过期 | 重新登录获取新 Cookie |
| `FAIL_SYS_USER_VALIDATE` | 被挤爆啦 | 风控拦截 | 需浏览器环境/代理/IP 轮换 |
| `FAIL_BIZ_ITEM_DEL_NOT_FOUND` | 宝贝不存在 | 商品 ID 无效 | 用真实商品 ID 测试 |
| `FAIL_SYS_BIZPARAM_MISSED` | 缺少业务参数 | 请求参数不完整 | 检查 data 字段格式 |

### 4.2 风控拦截处理（待解决）

**当前状态**: 登录 Token API 返回 `FAIL_SYS_USER_VALIDATE`（RGV587_ERROR）

**已知信息**:
- 这是闲鱼的反爬机制，不是 Cookie 问题
- 同样的 Cookie 在浏览器中可以正常登录
- 可能的原因：IP 被标记为数据中心、请求频率过高、缺少浏览器指纹

**待尝试的方案**:
1. 使用住宅代理 IP
2. 在浏览器中先访问 goofish.com 获取新 Cookie，再立即调用 API
3. 模拟完整浏览器指纹（sec-ch-ua、sec-fetch 等）
4. 降低请求频率（间隔 5-10 秒）
5. 先调用其他低风控 API（如商品列表），再调用登录 Token

## 5. 发布流程

### 5.1 product_publisher.py 架构

```
XianyuProductPublisher (Playwright 浏览器自动化)
├── publish_product()          # 发布单个商品（完整流程）
│   ├── _check_captcha()       # 检查验证码
│   ├── _handle_captcha()      # 处理验证码
│   ├── _upload_images()       # 上传图片
│   ├── _fill_product_info()   # 填写商品信息
│   ├── _select_category()     # 选择分类
│   ├── _click_publish()       # 点击发布
│   └── _verify_publish_success()  # 验证发布结果
├── batch_publish()            # 批量发布
└── publish_products()         # 入口函数
```

### 5.2 发布流程说明

发布使用 **Playwright 浏览器自动化**（不是 API 调用），完整模拟用户操作：
1. 打开 `goofish.com/publish`
2. 上传图片
3. 填写标题/描述/价格
4. 选择分类/位置
5. 点击发布
6. 验证结果

### 5.3 当前自动化闭环状态

| 环节 | 状态 | 说明 |
|------|------|------|
| Cookie 管理 | ✅ | 数据库增删改查 |
| 商品列表查询 | ✅ | execjs 签名 + mtop API |
| 商品详情查询 | ✅ | execjs 签名 + mtop API |
| 登录 Token | ⚠️ | 被风控拦截 |
| 商品发布 | ✅ | Playwright 浏览器自动化 |
| 批量发布 | ✅ | batch_publish 支持 |
| Cookie 刷新 | ⚠️ | refreshToken 机制存在但未测试 |

## 6. 经验教训

### ✅ 已验证

1. **签名必须用 execjs**: Node.js 直接算 MD5 的结果和 execjs 不一样，API 只认 execjs 的
2. **Cookie 748552523 有效**: 包含 cookie2/sgcookie 等完整字段，配合 execjs 签名可以正常调用 API
3. **pageNumber 从 0 开始**: 不是 1，pageSize 最大 20
4. **登录 Token API 参数格式**: data 必须是 `{"appKey":"444e9908a51d1cb236a27862abc769c9","deviceId":"..."}`，不是 `{"appName":"goofish"}`

### 🚨 踩坑记录

1. **签名不一致导致非法请求**: 用 Node.js 手动生成 MD5 签名，API 返回 FAIL_SYS_ILLEGAL_ACCESS，浪费大量时间
2. **Cookie 不完整**: 748552523 最初缺少 cookie2/sgcookie，所有 API 都返回非法请求
3. **登录 Token 被风控**: 不是 Cookie 问题，是反爬机制，需要其他方案绕过
4. **PyExecJS 缺失**: 系统默认没有 execjs，需手动安装 `pip install PyExecJS`

## 7. 闲鱼 vs 小红书反爬对比

| 维度 | 闲鱼 | 小红书 |
|------|------|--------|
| 签名算法 | MD5（execjs 环境有差异） | x-s 多层加密 |
| 签名入口 | execjs 调用 JS 文件 | xhshow 库 / JS |
| Cookie 要求 | cookie2 + sgcookie | a1 + web_session |
| 变化频率 | 低 | 约每月一次 |
| 绕过方案 | execjs 正确调用 | HTML 解析绕过 |
| IP 风控 | 中（RGV587） | 高（需住宅IP） |
| 写操作风控 | 高（Playwright 模拟） | 极高 |

## 8. 环境信息

| 项目 | 值 |
|------|-----|
| 项目路径 | `/root/.openclaw/workspace-media/xianyu-openclaw-channel-main/` |
| 数据库 | `data/xianyu_data.db` |
| 签名 JS | `static/xianyu_js_version_2.js` |
| 发布模块 | `product_publisher.py` |
| 主脚本 | `XianyuAutoAsync.py` |
| execjs | PyExecJS 1.5.1 + Node.js |
| Cookie 文件 | 数据库 cookies 表 |
| 当前可用 Cookie | unb=748552523 (panbin5218) |

## 9. CDP 浏览器自动化方案（2026-06-12 重大更新）

### 9.1 方案概述

通过 CDP 连接用户已登录的浏览器，直接操作闲鱼发布页面。**已成功发布商品**。

### 9.2 Cookie 提取（CDP 方式）

```python
import json, websocket
ws = websocket.create_connection("ws://127.0.0.1:9222/devtools/page/<pageId>", timeout=15)
ws.send(json.dumps({"id":1,"method":"Network.getAllCookies"}))
resp = json.loads(ws.recv())
cookies = resp.get("result",{}).get("cookies",[])
cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
```

**关键**：必须用 `Network.getAllCookies`（CDP 专属方法），JS `document.cookie` 拿不到 httpOnly cookies（sgcookie、havana_lgc2_77 等）。

### 9.3 启动有界面浏览器

```bash
google-chrome --no-sandbox --disable-gpu --no-dev-shm-usage \
  --remote-debugging-port=9222 --remote-allow-origins=* \
  "https://www.goofish.com"
```

- 用户手动扫码/密码登录后，CDP 连接并提取 cookies
- 服务器 IP 被闲鱼风控，**必须用住宅 IP**

### 9.4 图片上传突破（核心难点）

闲鱼上传组件是 React 组件，以下方法**均失败**：
- DOM.setFileInputFiles → 触发了 DOM 事件但闲鱼不识别
- Page.handleFileChooserDialog → Chrome 147 不支持
- file:// 或 http://127.0.0.1 fetch → 浏览器无法访问
- fake File 对象 → 闲鱼报"文件类型无法确定"

**验证可用的方法：base64 编码注入**

```python
# 1. 读取图片并 base64 编码
with open("image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("ascii")

# 2. 分块传输到浏览器（chunk_size=50000 避免表达式过大）
for chunk in [img_b64[i:i+50000] for i in range(0, len(img_b64), 50000)]:
    ws.send(json.dumps({"method":"Runtime.evaluate","params":{"expression":f"window.__imgB64='{chunk}';"}}))

# 3. 浏览器内创建 Blob/File 并触发 change 事件
js = """
(async function() {
    var binary = atob(window.__imgB64);
    var bytes = new Uint8Array(binary.length);
    for(var i=0; i<binary.length; i++) bytes[i] = binary.charCodeAt(i);
    var blob = new Blob([bytes], {type: 'image/jpeg'});
    var file = new File([blob], 'image.jpg', {type: 'image/jpeg'});
    var fileInput = document.querySelector('input[type="file"]');
    var dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event('change', {bubbles: true}));
    return 'done';
})()
"""
ws.send(json.dumps({"method":"Runtime.evaluate","params":{"expression": js, "awaitPromise": True}}))
```

### 9.5 下拉框操作

用 `Input.dispatchMouseEvent` 精确点击 `ant-select-selector` 打开下拉，然后用 `.ant-select-item` click() 选择选项。

### 9.6 发布页面结构（2026-06-12 确认）

| 元素 | 类型 | 说明 |
|------|------|------|
| 图片上传 | input[type=file]（隐藏） | display:none，需 base64 注入 |
| 宝贝描述 | contenteditable div | 最大 1500 字符，不支持 emoji |
| 价格 | input[type=text] | placeholder="0.00" |
| 原价 | input[type=text] | 可选 |
| 分类 | ant-select 下拉 | 如"DeepSeek服务" |
| 计价方式 | ant-select 下拉 | 元/次、元/时、元/课 |
| 服务类型 | ant-select 下拉 | 指令优化、模型搭建、本地部署、教学指导 |
| 发货设置 | ant-radio | 包邮/按距离计费/一口价/无需邮寄 |
| 所在地 | 自动填充 | 需提前在闲鱼设置常用地址 |
| 发布按钮 | button | 文本"发布" |

**闲鱼没有标题输入框！** 商品标题自动从描述中提取。

### 9.7 踩坑记录（2026-06-12）

1. 描述中不能包含 emoji — 闲鱼提示"商品描述不能包含emoji"
2. httpOnly cookies 必须通过 CDP Network.getAllCookies 获取
3. 端口冲突 — snap 版 Chromium(9223)和 google-chrome(9222)可能同时存在
4. DOM 节点不稳定 — 关闭弹窗后 nodeId 会变，每次操作前需重新获取
5. wait_until='networkidle' 在闲鱼 SPA 上永远等不到，必须用 'domcontentloaded'
6. 服务器 IP 被闲鱼风控 — 机房 IP 无法登录，必须用住宅 IP

### 9.8 完整发布流程

1. CDP 连接已登录的浏览器（9222端口）
2. 导航到 https://www.goofish.com/publish
3. 等待 8 秒 SPA 渲染
4. base64 注入图片 - 触发 change 事件 - 等待 8 秒上传
5. 填写描述（无 emoji）
6. 选择分类、计价方式、服务类型
7. 填写价格
8. 点击发布 - 等待 8 秒 - 确认结果

### 9.9 已验证成功案例

| 商品 | 价格 | 分类 | 结果 |
|------|------|------|------|
| DeepSeek V4 API 包月畅用 | 4.00 | DeepSeek服务/元/次/指令优化 | 已上架 |

Cookie 保存位置：
- .config/xianyu_cookies.txt — 完整 cookie string
- .config/xianyu_key_cookies.json — 关键 cookies
- .config/xianyu_user_info.json — 用户标识信息

## 10. 待解决问题

### 10.1 登录 Token 风控拦截（已定位）

**问题**: `mtop.taobao.idlemessage.pc.login.token` 返回 `FAIL_SYS_USER_VALIDATE`

**测试结果** (2026-06-10):
- 间隔 5秒 × 10次: 前2次成功，后8次失败（概率性拦截）
- 间隔 10秒 × 3次: 全部失败
- 间隔 20秒 × 3次: 全部失败
- 间隔 30秒 × 3次: 全部失败
- 间隔 60秒 × 3次: 全部失败

**结论**: 不是间隔时间问题，是登录 Token API 在服务器端被标记为高风险。连续调用会触发更强风控。

**解决方案**: **绕过！登录 Token 不是必需的。**
- Cookie 已包含完整认证信息（cookie2、sgcookie、_m_h5_tk 等）
- 商品列表/详情 API 直接用 Cookie + execjs 签名就能调
- 只需在首次获取 accessToken 时调一次登录 Token（可偶尔成功），后续用 Cookie 调 API

**实际策略**: 
1. 首次启动时尝试调登录 Token 获取 accessToken（可能成功）
2. 如果失败，直接用 Cookie 调 API（不需要 accessToken）
3. 登录 Token 仅用于获取 refreshToken，非必须

### 10.2 Cookie 自动刷新

**问题**: Cookie 过期后需要手动获取

**方案**: 利用 refreshToken 自动刷新，或通过浏览器自动获取新 Cookie

### 10.3 发布商品 API 化

**问题**: 当前用 Playwright 浏览器模拟，速度慢且不稳定

**方案**: 研究闲鱼发布 API，用 API 调用替代浏览器自动化（需要解决签名问题）

## 11. 关键资源

| 资源 | 链接 | 说明 |
|------|------|------|
| Spider_XHS | github.com/cv-cat/Spider_XHS | 小红书爬虫参考（签名算法可借鉴） |
| xhs-cli | github.com/jackwener/xiaohongshu-cli | CLI 工具（HTML 解析绕过闲鱼签名） |
| xhshow | PyPI | 小红书签名算法库 |
| execjs | PyPI | Python 调用 JS 执行环境 |
| PyExecJS | PyPI | execjs 的底层实现 |

## 12. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 浏览器自动化经验 | /home/obsidian_vault/shared/browser/browser-automation.md | CDP 操作、图片上传突破等 |
| 每日日志 | memory/2026-06-12.md | 今日操作记录 |
| 原始脚本 | xianyu-publish/publish.py | Playwright 发布脚本 |
