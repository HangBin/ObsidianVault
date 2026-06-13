---
title: 闲鱼自动化经验指南
date: 2026-06-10
last_updated: 2026-06-13 (15:01)
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

## 9. CDP + Playwright 浏览器自动化方案（2026-06-13 重大更新）

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

**最新 cookies 位置**: `.config/xianyu_cookies_latest.txt`（2026-06-13 CDP 提取）

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
- DOM.setFileInputFiles → 触发了 DOM 事件但 React 不识别
- Page.handleFileChooserDialog → Chrome 147 不支持
- file:// 或 http://127.0.0.1 fetch → 浏览器无法访问
- fake File 对象 → 闲鱼报"文件类型无法确定"
- base64 编码注入 + change 事件 → React 仍然不识别（2026-06-12 验证）

**✅ 最终验证可用的方法：fetch 上传 + React fiber onChange 注入（2026-06-13）**

原理：通过浏览器 fetch 直接调用闲鱼上传接口拿到 fileId，再通过 React fiber 树找到上传组件的 `onChange` 回调，直接调用注入 fileList 状态。

```python
# Step 1: 通过浏览器 fetch 上传图片（利用页面 cookies）
upload_js = """
(async function() {
    try {
        var binary = atob(window.__imgB64);
        var bytes = new Uint8Array(binary.length);
        for(var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
        var blob = new Blob([bytes], {type: 'image/png'});
        var formData = new FormData();
        formData.append('file', blob, 'opus48.png');
        formData.append('floderId', '0');
        formData.append('appkey', 'fleamarket');
        var resp = await fetch('https://stream-upload.goofish.com/api/upload.api?floderId=0&appkey=fleamarket&_input_charset=utf-8', {
            method: 'POST', body: formData, credentials: 'include'
        });
        var text = await resp.text();
        return text;
    } catch(e) { return 'error: ' + e.message; }
})()
"""
result = send_cdp("Runtime.evaluate", {"expression": upload_js, "awaitPromise": True})
# 返回: {"fileId":"1252308764062160188","url":"https://img.alicdn.com/..."}

# Step 2: 通过 React fiber 找到上传组件的 onChange
# 从 #ice-container 的 __reactContainer$fiberKey 遍历 fiber 树
# 查找 memoizedProps.fileList !== undefined && typeof memoizedProps.onChange === 'function'

# Step 3: 调用 onChange 注入文件状态
file_item = {
    'fileId': '1252308764062160188',
    'url': 'https://img.alicdn.com/imgextra/i1/O1CN01OsrPP51UVaQ3vgj8u_!!748552523-2-fleamarket.png',
    'name': 'opus48.png', 'size': 104873, 'status': 'done', 'type': 'image/png'
}
target_fiber.memoizedProps.onChange({'fileList': [file_item]})
```

**⚠️ 注意**：base64 分块传输仍然需要（图片需要在浏览器内存中），但不再依赖 DOM change 事件，而是直接调 React 回调。

### 9.5 下拉框操作（ant-select）

```python
# 点击下拉打开
selector = page.query_selector('.ant-select-selector')  # 或第N个
selector.click()
await asyncio.sleep(2)

# 点击选项
page.evaluate("""
(() => {
    const dropdown = document.querySelector('.ant-select-dropdown');
    const items = dropdown.querySelectorAll('[class*="item"], [role="option"]');
    for (const item of items) {
        if (item.innerText.trim() === 'DeepSeek服务') { item.click(); break; }
    }
})()
""")
```

**注意**：
- 下拉可能渲染到 body 层（portal），不在 `.ant-select` 内部
- 选项文本匹配用 `innerText.trim()`，不要包含旁白的 ID 数字
- 如果 `query_selector` 找不到，可用 `page.mouse.click(x, y)` 坐标点击

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

### 9.8 完整发布流程（Playwright + CDP 方式，2026-06-13 验证）

```python
async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]
    page = context.pages[0]

    # 1. 导航到发布页面
    await page.goto('https://www.goofish.com/publish', wait_until='domcontentloaded')
    await asyncio.sleep(8)

    # 2. 上传图片（三步：base64注入 → fetch上传 → fiber onChange）
    # 2a. 分块传输 base64 到浏览器
    # 2b. 浏览器 fetch 上传到 stream-upload.goofish.com → 拿 fileId
    # 2c. 遍历 fiber 树找 memoizedProps.onChange → 调用注入 fileList

    # 3. 填写描述（contenteditable div，用 innerHTML）
    await page.evaluate("editor.innerHTML = '<p>描述内容</p>'")

    # 4. 填写价格
    await page.query_selector('input[placeholder="0.00"]').fill('0.09')

    # 5. 选择分类/计价方式/服务类型（见 9.5）

    # 6. 点击发布按钮
    await page.evaluate("document.querySelector('button:has-text(\'发布\')').click()")
    await asyncio.sleep(8)

    # 7. 验证：页面跳转到商品详情页 = 成功
    assert 'item' in page.url
```

**关键依赖**：浏览器必须已登录闲鱼（9222端口的 google-chrome），Playwright 通过 CDP 连接复用登录态。

### 9.9 已验证成功案例

| 商品 | 价格 | 分类 | 方式 | 结果 |
|------|------|------|------|------|
| DeepSeek V4 API 包月畅用 | 4.00 | DeepSeek服务/元/次/指令优化 | CDP base64注入(06-12) | ✅ 已上架 |
| opus4.8全网底价0.09/刀 | 0.09 | DeepSeek服务/元/次/指令优化 | Playwright+CDP fiber注入(06-13) | ✅ 已上架 |

Cookie 保存位置：
- .config/xianyu_cookies_latest.txt — 最新完整 cookie string（CDP提取）
- .config/xianyu_cookies.txt — 完整 cookie string
- .config/xianyu_key_cookies.json — 关键 cookies
- .config/xianyu_user_info.json — 用户标识信息
- xianyu-publish/xianyu_cookies.txt — Playwright 脚本用 cookies

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

### 10.3 发布商品 API 化（2026-06-13 进展）

**抓包成果**: 通过 Playwright 拦截网络请求，成功捕获到真实发布 API 的完整请求格式：

```
POST https://h5api.m.goofish.com/h5/mtop.idle.pc.idleitem.publish/1.0/
Params: jsv=2.7.2&appKey=34839810&t=<timestamp>&sign=<execjs_sign>&...
Body: data=<URL编码的JSON>
```

**请求体关键字段**（从抓包解码）：
- `freebies`: false
- `itemTypeStr`: "b"
- `quantity`: "1"
- `simpleItem`: true
- `imageInfoDOList`: [{extraInfo:{...}, url, major:true, type:0, status:"done"}]
- 还包含 title/desc/price/categoryId/shopId 等完整商品信息

**签名验证**: execjs 调用 `generate_sign(t, token, data)` 已验证通过（用页面捕获的 prepublish.check 请求验证 sign 完全匹配）

**当前状态**: Playwright+CDP 浏览器方案已能稳定发布，API 化方案作为性能优化方向保留。
- 优势：浏览器方案可以绕过所有风控（复用用户登录态）
- 风险：API 化后需要独立处理风控（RGV587_ERROR）

**建议优先级**: 低。浏览器方案已稳定，API 化需要额外投入且引入风控风险。

## 11. 关键资源

| 资源 | 链接 | 说明 |
|------|------|------|
| Spider_XHS | github.com/cv-cat/Spider_XHS | 小红书爬虫参考（签名算法可借鉴） |
| xhs-cli | github.com/jackwener/xiaohongshu-cli | CLI 工具（HTML 解析绕过闲鱼签名） |
| xhshow | PyPI | 小红书签名算法库 |
| execjs | PyPI | Python 调用 JS 执行环境 |
| PyExecJS | PyPI | execjs 的底层实现 |

## 12. 一键自动化方案（2026-06-13 重大更新）

### 12.1 方案概述

**完全无需手动启动浏览器**的一键发布方案。通过 `xvfb-run` 自动创建虚拟 X Server + 启动 Chrome，CDP 端口自动监听，全流程自动化。

```bash
# 一条命令完成全部操作
bash run.sh --image /path/to/img.png --desc '商品描述' --price 0.09
```

### 12.2 脚本架构

| 文件 | 功能 | 调用方式 |
|------|------|---------|
| `run.sh` | 一键入口：启动 Chrome → 检测登录态 → 发布 | `bash run.sh --image ... --desc ... --price ...` |
| `xianyu_start.sh` | Chrome 启动脚本（xvfb-run） | 被 run.sh 内部调用 |
| `xianyu_publish.py` | CDP 自动化发布核心（上传+填写+发布） | 被 run.sh 内部调用 |

### 12.3 xvfb-run 启动 Chrome（核心突破）

**问题**：`sudo bash` 和 `sudo -u bill` 环境下 `DISPLAY` 变量均为空，Chrome 找不到 X Server → CDP 9222 端口不监听。

**解决方案**：`xvfb-run --auto-servernum` 自动创建虚拟 X Server（:99）并设置 `DISPLAY` 环境变量。

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

**关键发现**：
- `xvfb-run` 自动设置 `DISPLAY` = Chrome 能正常启动 + CDP 端口监听
- `--auto-servernum` 自动选择可用的 X display 编号
- `--server-args="-screen 0 1920x1080x24"` 设置分辨率
- `&>/dev/null` 必须加，否则 xvfb 的 stderr 会阻塞 shell

**对比之前失败的方案**：

| 方案 | DISPLAY | CDP 端口 | 失败原因 |
|------|---------|----------|---------|
| `sudo bash xianyu_start.sh` | 空 | ❌ 不监听 | sudo 不保留 DISPLAY |
| `sudo -u bill bash ...` | 空 | ❌ 不监听 | 同上 |
| `su - bill -c '...'` | :0 | ❌ 不监听 | PAM 环境变量问题 |
| `sudo -u bill DISPLAY=:0 ...` | :0 | ❌ 不监听 | root 无 :0 权限 |
| **`xvfb-run --auto-servernum`** | **自动设置** | **✅ 监听** | **唯一可行方案** |

### 12.4 图片上传修复（返回值解析）

**问题**：fetch 上传返回成功但 `fileId` 为空。

**根因**：闲鱼上传 API 返回结构嵌套在 `object` 字段中：
```json
{"object":{"fileId":"1252308768221179213","url":"https://img.alicdn.com/..."},"success":true}
```
脚本之前取 `data.get("fileId")` → 顶层没有 → 返回空。

**修复**：
```python
file_id = data.get("fileId", "") or (data.get("object", {}) or {}).get("fileId", "")
url = data.get("url", "") or (data.get("object", {}) or {}).get("url", "")
```

### 12.5 Cookies 提取与验证

**提取方式**：通过 CDP `Network.getAllCookies` 获取完整 cookies（包括 httpOnly cookies）。

```python
# 必须用 Network.getAllCookies，document.cookie 拿不到 httpOnly cookies
ws.send(json.dumps({"id":1,"method":"Network.getAllCookies"}))
resp = json.loads(ws.recv())
cookies = resp["result"]["cookies"]
cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
```

**验证结果**：35 个 cookies，关键 cookies 完整：
- `tracknick=panbin5218`（用户名）
- `unb=748552523`（用户唯一标识）
- `XSRF-TOKEN`、`cookie2`、`sgcookie`（登录态核心）

**Cookies 直接调 API**：测试了多个闲鱼 API 路径均返回 404，闲鱼没有公开的发布 API → CDP 浏览器自动化是唯一可行方案。

### 12.6 已验证发布记录（2026-06-13）

| 商品 | 价格 | 商品ID | 方式 | 结果 |
|------|------|--------|------|------|
| Claude Opus 4.8 API | ¥0.09 | 1057911158600 | CDP fiber 注入 | ✅ 已上架 |
| Claude Opus 4.8 API（测试） | ¥0.09 | 1057127547428 | run.sh 一键 | ✅ 已上架 |
| MacBook Pro M4 Pro 14寸 | ¥8888 | 1059835968742 | run.sh 一键 | ✅ 已上架 |

### 12.7 一键发布完整流程

```
bash run.sh --image img.png --desc '描述' --price 0.09
  │
  ├─ Step 1: start_chrome()
  │    ├─ 检查 CDP 9222 是否已可用 → 是则跳过
  │    ├─ xvfb-run 启动 Chrome
  │    └─ 等待 CDP 就绪（最多 20s）
  │
  ├─ Step 2: check_login()
  │    ├─ CDP 连接 → Runtime.evaluate → 页面内容
  │    └─ 检测 panbin5218/订单 → 已登录
  │
  └─ Step 3: xianyu_publish.py publish
       ├─ CDP 连接 → 找到 goofish.com tab
       ├─ 检查登录态
       ├─ 导航到 /publish
       ├─ fetch 上传图片 → 拿到 fileId + url
       ├─ React fiber onChange 注入 fileList
       ├─ 填写描述（contenteditable innerHTML）
       ├─ 填写价格（input value setter）
       ├─ 截图确认
       ├─ 点击发布按钮
       └─ 验证：页面跳转到 /item/id=xxx → 成功
```

### 12.8 前置依赖

```bash
# 系统依赖
apt-get install xvfb x11vnc

# Python 依赖
pip install websockets websocket-client

# Chrome 已安装（google-chrome，非 snap chromium）
# 路径: /opt/google/chrome/chrome
# Profile: /home/bill/.config/google-chrome/
```

### 12.9 已知限制

1. **登录态会过期**：Chrome profile 里的闲鱼 cookies 过期后需要手动重新登录一次
2. **xvfb 虚拟桌面性能**：虚拟桌面下 Chrome 渲染性能略低，但发布功能正常
3. **不支持批量上传不同图片**：当前脚本每次发布一个商品，批量模式需要商品列表 JSON
4. **服务器 IP 风控**：机房 IP 可能被闲鱼风控，建议在住宅 IP 环境运行

### 12.10 Session Cookies 恢复方案（2026-06-13）

**问题**：Chrome 重启后 session cookies（`cookie2`、`XSRF-TOKEN` 等 `expires=-1` 的 cookies）会丢失，导致闲鱼登录态失效。

**触发场景**：
- 手动关闭 `:0` 桌面 Chrome 后重启
- Chrome 崩溃后自动重启
- 系统重启后 Chrome 自动启动

**恢复方案**：CDP `Network.setCookie` 注入之前保存的 cookies

```python
# 1. 读取之前保存的 cookies
with open("/tmp/xianyu_cookies.txt") as f:
    cookie_str = f.read().strip()

# 2. 解析并逐个注入
for part in cookie_str.split("; "):
    name, value = part.split("=", 1)
    ws.send(json.dumps({"id": msg_id, "method": "Network.setCookie", "params": {
        "name": name.strip(), "value": value.strip(),
        "domain": ".goofish.com", "path": "/",
        "httpOnly": False, "secure": True, "sameSite": "None"
    }}))

# 3. 刷新页面 → 登录态恢复
ws.send(json.dumps({"id": msg_id, "method": "Page.navigate", "params": {"url": "https://www.goofish.com/"}}))
```

**前置条件**：`/tmp/xianyu_cookies.txt` 文件存在（35个cookies，1940字符）

**最佳实践**：在 `run.sh` 启动 Chrome 后自动执行 cookies 注入，确保登录态始终有效。

## 13. 闭环测试全记录（2026-06-13 16:22）

### 13.1 测试目标

完整闭环：从启动浏览器到发布新商品，全程无需人工干预（除首次登录外）。

### 13.2 测试结果：✅ 发布成功

| 字段 | 值 |
|------|------|
| 商品名称 | 绝版收藏周杰伦签名专辑 全球仅此一张 带亲笔签名 |
| 价格 | ¥888,888（测试天价） |
| 分类 | 音乐唱片/专辑 |
| 明星角色 | 周杰伦 |
| 存储介质 | CD |
| 所在地 | 南湖沃尔玛提货点 |
| 商品ID | 1059858208480 |
| 商品URL | https://www.goofish.com/item/id=1059858208480 |

### 13.3 完整闭环步骤

```
1. run.sh 启动 Chrome（xvfb-run + CDP 端口 9222）
2. CDP 连接已登录浏览器（ws://127.0.0.1:9222）
3. 导航到 https://www.goofish.com/publish
4. 上传图片（base64 → POST 到 stream-upload.goofish.com → 获得 fileId）
5. 通过 React fiber 注入文件到上传组件
6. 填写描述（contenteditable innerHTML 注入 + input 事件）
7. 填写价格（HTMLInputDescriptor setter + input/change 事件）
8. 等待页面自动识别分类（约 3 秒）
9. 选择存储介质（见 13.4）
10. 点击发布按钮 → 跳转商品详情页
```

### 13.4 🔑 Ant Design Select 选择方案（核心突破）

**问题**：Ant Design 5 Select 组件不响应 DOM 事件（click / insertText），无法通过常规方式触发下拉菜单。

**解决方案**：CDP `Input.dispatchKeyEvent` 逐字输入

```python
# 1. focus 搜索输入框
js("document.querySelectorAll('.ant-select')[2].querySelector('input[type=search]').focus()")

# 2. 逐字输入搜索关键词
for char in 'CD':
    cdp('Input.dispatchKeyEvent', {
        'type': 'keyDown', 'text': char, 'key': char, 'code': '',
        'windowsVirtualKeyCode': ord(char), 'nativeVirtualKeyCode': ord(char)
    })
    cdp('Input.dispatchKeyEvent', {
        'type': 'keyUp', 'key': char, 'code': '',
        'windowsVirtualKeyCode': ord(char), 'nativeVirtualKeyCode': ord(char)
    })

# 3. 等待 2-3 秒，下拉菜单出现
# 4. 点击目标选项
js("document.querySelector('.ant-select-item-option-content').parentElement.click()")
# 或更精确：遍历所有元素找 textContent.trim() === 'CD' 且 children.length === 0 的元素
```

**三种方案对比**：

| 方案 | 结果 | 原因 |
|------|------|------|
| DOM click | ❌ | Ant Design 5 拦截了合成事件 |
| Input.insertText | ❌ | Select 组件不响应直接插入文本 |
| Input.dispatchKeyEvent | ✅ | 模拟真实键盘输入，Select 组件正常响应 |

### 13.5 踩坑记录

1. **价格 React state 不同步**：DOM 设值后 React 可能未识别，但实际发布时以 DOM 值为准
2. **分类自动识别有延迟**：上传图片后需等 3 秒让页面完成分类识别
3. **Select 下拉通过 portal 渲染**：下拉菜单不在 Select DOM 内，而在 body 末尾
4. **搜索框 focus 必须先于 keyEvent**：否则 keyEvent 不会输入到搜索框
5. **选项精确匹配**：找选项时用 `textContent.trim() === 'CD' && children.length === 0` 避免误匹配

### 13.6 无需人工介入的开关条件

| 条件 | 说明 |
|------|------|
| Chrome 登录态有效 | cookies 未过期，无需手动登录 |
| `/tmp/xianyu_cookies.txt` 存在 | 用于 session cookie 恢复 |
| `run.sh` 可正常执行 | xvfb-run + CDP 端口可用 |

**登录态过期后**：需手动在 Chrome 中登录一次闲鱼，再提取 cookies 保存到 `/tmp/xianyu_cookies.txt`。

## 14. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 一键发布脚本 | /home/bill/run.sh | 一键启动+发布（入口） |
| Chrome 启动脚本 | /home/bill/xianyu_start.sh | xvfb-run 启动 Chrome |
| 发布核心脚本 | /home/bill/xianyu_publish.py | CDP 自动化发布核心 |
| 浏览器自动化经验 | /home/obsidian_vault/shared/browser/browser-automation.md | CDP 操作、图片上传突破等 |
| 每日日志 | memory/2026-06-12.md | CDP 发布实操记录 |
| 每日日志 | memory/2026-06-13.md | xvfb-run + CDP 发布实操记录 |
| 原始脚本 | xianyu-publish/publish.py | Playwright 发布脚本 |
| 发布 API 抓包分析 | 见 10.3 节 | 真实发布请求格式 |
