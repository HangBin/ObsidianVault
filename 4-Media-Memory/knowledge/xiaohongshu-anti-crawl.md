---
title: 小红书反爬机制研究
date: 2026-06-10
tags:
  - xiaohongshu
  - anti-crawl
  - reverse-engineering
  - xhs-cli
  - spider-xhs
author: media
---

# 小红书反爬机制研究

> 研究时间: 2026-06-10
> 信息来源: Spider_XHS GitHub、xhs-cli 源码、dev.to 2026爬虫文章、CSDN逆向教程

## 一、反爬五层防线

| 层级 | 机制 | 严重程度 | 绕过方案 |
|------|------|---------|---------|
| 1️⃣ TLS 指纹检测 | JA3/JA4 识别 Python requests | 中 | curl_cffi 伪装 Chrome 指纹 |
| 2️⃣ 请求签名 | x-s / x-t / x-s-common | 高 | xhshow 库 / execjs 调用 JS |
| 3️⃣ IP 级限流 | 数据中心 IP 直接拦截 | 高 | 住宅代理（中国地理位置） |
| 4️⃣ SPA 动态渲染 | 部分接口需浏览器执行 JS | 中 | Playwright / 补环境 |
| 5️⃣ 登录墙 | xsec_token / web_session | 中 | 登录态 Cookie |

## 二、签名算法核心（xhshow 库）

### 2.1 x-s 签名流程

```
1. content_string = METHOD + URI + params/payload
2. d_value = encrypt(content_string)  // 加密变换
3. payload_array = [d_value, a1, xsec_appid, content_string, timestamp]
4. xor_result = XOR_transform(payload_array)
5. x3 = base64(xor_result[:PAYLOAD_LENGTH])
6. signature_data = {x0: SDK_VERSION, x1: APP_ID, x2: PLATFORM, x3: x3, ...}
7. x-s = XYS_PREFIX + base64(json(signature_data))
```

### 2.2 请求头要求

| Header | 说明 | 生成方式 |
|--------|------|---------|
| `x-s` | 主签名 | xhshow 动态生成 |
| `x-t` | Unix 毫秒时间戳 | int(time.time() * 1000) |
| `x-s-common` | 公共签名 | 基于 Cookie 生成 |
| `x-b3-traceid` | 追踪 ID | 随机生成 |
| `x-xray-traceid` | 追踪 ID | 随机生成 |

### 2.3 必需 Cookie 字段

- `a1`: 用户唯一标识（必需，用于签名）
- `web_session`: 会话 ID（必需，用于 x-s-common）

## 三、xhs-cli 绕过策略（⭐ 最佳实践）

### 3.1 搜索（需要签名）

```python
# xhs-cli 使用 xhshow 库生成完整签名
from xhshow import Xhshow, CryptoConfig

config = CryptoConfig().with_overrides(
    PUBLIC_USERAGENT="Mozilla/5.0 ...",
    SIGNATURE_DATA_TEMPLATE={...},
)
xhshow = Xhshow(config)
headers = xhshow.sign_headers_post(
    uri="/api/sns/web/v1/search/notes",
    cookies=cookies_dict,
    payload={"keyword": "搜索词", ...}
)
```

### 3.2 读取笔记（绕过签名）

**关键发现**: xhs-cli 读取笔记不走 API，直接请求 HTML 页面：

```python
# 有 xsec_token
url = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed"

# 无 xsec_token（也能用）
url = f"https://www.xiaohongshu.com/explore/{note_id}"
```

HTML 页面中包含完整的笔记数据（SSR 渲染），直接解析即可，**完全绕过 API 签名**。

### 3.3 创作者平台签名

创作者平台（creator.xiaohongshu.com）用不同的签名函数：

```python
from xhs_cli.creator_signing import sign_creator
sign = sign_creator(f"url={full_uri}", None, cookies["a1"])
# 返回 {"x-s": ..., "x-t": ...}
```

## 四、签名算法变化频率

- 约每月更新一次（重大版本如 xs version56）
- 每次更新后旧签名失效（返回 406 错误）
- Spider_XHS 项目持续跟踪：https://github.com/cv-cat/Spider_XHS
- MediaCrawler 项目：https://github.com/NanmiCoder/MediaCrawler

## 五、项目架构参考

### Spider_XHS（推荐）

```
Spider_XHS/
├── apis/
│   ├── xhs_pc_apis.py          # PC端完整API（采集）
│   ├── xhs_creator_apis.py     # 创作者平台API（上传发布）
│   ├── xhs_pc_login_apis.py    # PC端登录（二维码/手机验证码）
│   └── ...
├── xhs_utils/
│   ├── xhs_util.py             # PC端签名算法
│   ├── xhs_creator_util.py     # 创作者平台签名算法
│   └── ...
├── static/
│   ├── xhs_main_260411.js      # PC端签名核心JS（最新版）
│   ├── xhs_rap.js              # x-rap-param JSVMP 补环境
│   └── ...
```

### xhs-cli（轻量级）

```
xhs_cli/
├── signing.py                  # 签名适配层（调用 xhshow）
├── client.py                   # API 客户端
├── client_mixins.py            # 业务逻辑 mixin
└── ...
```

## 六、实战建议

### 6.1 采集（读）操作

1. **搜索笔记**: 使用 xhshow 库生成签名，调用 `/api/sns/web/v1/search/notes`
2. **读取笔记**: 走 HTML 解析（`xiaohongshu.com/explore/{note_id}`），完全绕过签名
3. **获取评论**: 需要签名，调用 `/api/sns/web/v2/comment/page`

### 6.2 发布（写）操作

1. **上传图片**: 需要创作者平台签名
2. **创建笔记**: 需要创作者平台签名
3. **注意**: 写操作风控更严格，建议用浏览器自动化

### 6.3 反检测措施

1. **TLS 指纹**: `pip install curl_cffi` → `impersonate="chrome120"`
2. **请求间隔**: 2-3 秒/请求（搜索），10-20 请求/分钟/IP
3. **住宅代理**: 中国地理位置住宅 IP
4. **浏览器指纹**: 完整 sec-ch-ua / sec-fetch 头

## 七、关键资源

| 资源 | 链接 | 说明 |
|------|------|------|
| Spider_XHS | github.com/cv-cat/Spider_XHS | 最完整的开源爬虫框架 |
| xhs-cli | github.com/jackwener/xiaohongshu-cli | CLI 工具，HTML 解析绕过 |
| MediaCrawler | github.com/NanmiCoder/MediaCrawler | 多平台爬虫 |
| xhshow | PyPI | 签名算法库 |
| Spider_XHS JS | static/xhs_main_260411.js | 最新签名核心 JS |

## 八、闲鱼 vs 小红书反爬对比

| 维度 | 闲鱼 | 小红书 |
|------|------|--------|
| 签名算法 | MD5（简单） | x-s 多层加密（复杂） |
| 签名入口 | execjs 调用 JS | xhshow 库 / JS |
| Cookie 要求 | cookie2 + sgcookie | a1 + web_session |
| 变化频率 | 低 | 约每月一次 |
| 绕过方案 | execjs 正确调用 | HTML 解析绕过 |
| IP 风控 | 中 | 高（需住宅IP） |
| 写操作风控 | 高 | 极高 |
