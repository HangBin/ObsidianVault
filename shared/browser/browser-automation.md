---
author: tech agent
created: 2026-04-14 09:34:12
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
tags:
  - experience
  - knowledge
  - shared
  - cdp
  - 浏览器
---

# 🌐 Chromium CDP 有头浏览器自动化专项经验（2026-04-23最终版）

## 📋 核心要点 - 一学就会

### 端口用途速查表（最重要！）
| 端口 | 类型 | 用途 | 适用场景 |
|------|------|------|----------|
| 9222 | 有界面 | 用户已登录会话 | 小红书、淘宝等需要登录的网站 |
| 9223 | 无头 | 自动化测试 | 简单访问、批量操作 |



### 宿主机启动命令（复制即用）

#### 方式一：【推荐】有界面浏览器（保持用户登录状态）

创建启动脚本（如 `start-chrome-debug.sh`）

```bash
nano ~/start-chrome-debug.sh
```

内容：

```bash
#!/bin/bash
/usr/bin/chromium-browser \
  --remote-debugging-port=9222 \
  --remote-allow-origins=http://127.0.0.1:9222 \
  --password-store=basic \
  --no-sandbox \
  --user-data-dir=/home/bill/snap/chromium/common/chromium
```

赋予执行权限：

```bash
chmod +x ~/start-chrome-debug.sh
```

在宿主机上运行脚本启动 Chrome：

```bash
./start-chrome-debug.sh
```

#### 方式二：【备选】无头浏览器（自动启动）

```bash
chromium --headless --remote-debugging-port=9223 --no-sandbox about:blank
```



### 连接方式与命令（直接复制）

```bash
# 【首选】有界面浏览器连接
agent-browser --cdp 9222 open "https://www.xiaohongshu.com/explore"
agent-browser --cdp 9222 screenshot "/tmp/xiaohongshu.png"

# 【备选】无头浏览器连接  
agent-browser --cdp 9223 open "https://www.baidu.com"
agent-browser --cdp 9223 screenshot "/tmp/baidu.png"

# 【验证】连接状态检查
curl -s http://127.0.0.1:9222/json | jq '.[] | {title, url}'

# 浏览器状态
openclaw browser status

# 查看端口是否监听
netstat -tlnp | grep 9222
# 或
ss -tlnp | grep 9222
```

### 适用场景（一看就懂）
✅ **需要登录的网站**：小红书、淘宝、知乎（保持登录状态）  
✅ **热点数据抓取**：社交媒体榜单、电商搜索（避免风控）  
✅ **动漫资源查询**：6v520电影网、磁力链接提取  
✅ **任意有界面会话**：用户已登录的任何网站



### 📸 截图分享规范（必须遵守）
1. **先启动HTTP服务**：`python3 -m http.server 8888 --bind 0.0.0.0 --directory /tmp/ &`
2. **获取本机IP**：```hostname -I | awk '{print $1}'```
3. **拼接完整链接**：格式：`http://宿主机IP:8888/截图名.png`（如`http://192.168.1.210:8888/xianni_detail.png`）
4. **验证链接**：`curl -I http://192.168.1.210:8888/xianni_detail.png`，必须返回 HTTP/1.0 200 OK 才能分享
5. **分享格式**：`http://192.168.1.x:8888/文件名.png`（必须是可点击链接，验证链接200后再发链接）
6. **文件存储**：所有截图保存到`/tmp/`目录
7. **命名规范**：`内容_时间戳.png`（如：xiaohongshu_hot_20260423.png）



### 📸 **分步截图规范（必须遵守）**

#### **基本流程要求**

每个操作都应该包含以下截图步骤：

- **步骤1**: 操作前状态截图
- **步骤2**: 操作执行后截图
- **步骤3**: 跳转/变化后截图
- **步骤4**: 最终结果截图

#### **具体操作截图规范**

**网站打开操作截图**：

```bash
agent-browser --cdp 9222 screenshot "/tmp/before_open.png"
agent-browser --cdp 9222 open "https://www.xiaohongshu.com/explore"
agent-browser --cdp 9222 screenshot "/tmp/after_open.png"
```

**搜索操作截图**：

```bash
agent-browser --cdp 9222 screenshot "/tmp/before_search.png"
agent-browser --cdp 9222 eval 'document.querySelector("input[type=\"search\"]").value = "仙逆"'
agent-browser --cdp 9222 screenshot "/tmp/search_results.png"
```

**点击操作截图**：

```bash
agent-browser --cdp 9222 screenshot "/tmp/before_click.png"
agent-browser --cdp 9222 eval 'document.querySelector(".anime-list a").click()'
agent-browser --cdp 9222 screenshot "/tmp/post_click_state.png"
```

#### **可点击链接分享格式**

```bash
python3 -m http.server 8888 --bind 192.168.1.x --directory /tmp/ &
echo "[点击查看](http://192.168.1.x:8888/filename.png)"
```

#### **命名规范增强版**

```
{操作类型}_{时间戳}.png
例如: before_open_20260423.png, after_open_20260423.png
```

这个详细的截图规范确保了每个操作步骤都有完整的截图记录，并且提供可点击的链接形式。



### 网站查询经验（完整流程）

#### 6v520电影网查询（带集数）

```bash
# 1. 打开动漫页面(使用已启动的有界面浏览器（9222端口）)
agent-browser --cdp 9222 open "https://www.6v520.com/zydy/"
# 打开页面截图
agent-browser --cdp 9222 screenshot "/tmp/6v520_home.png"

# 2. 搜索流程: 
# 步骤1：在搜索框输入关键词
# 注意：必须使用 @ref 格式定位元素
#      e20 是站内搜索输入框的 ref
agent-browser --cdp 9222 fill @e20 "仙逆"
# 输入搜索词后截图
agent-browser --cdp 9222 screenshot "/tmp/xianni_search.png"
# 步骤2：点击提交按钮
# 注意：e22 是"提交"按钮的 ref
agent-browser --cdp 9222 click @e22
# 搜索结果截图
agent-browser --cdp 9222 screenshot "/tmp/xianni_search_result.png"

# 3. 查看详情获取下载链接
# 步骤1：点击目标动漫的详情链接
# 注意：ref e80 是搜索结果中"《仙逆》更新138"的链接
agent-browser --cdp 9222 click @e80
# 步骤2：详情页截图
agent-browser --cdp 9222 screenshot "/tmp/xianni_detail.png"
# 步骤3：用curl直接提取磁力链接（两种方法）
# 获取页面HTML
curl -s "https://www.6v520.com/zydy/2023-09-26/42788.html" > /tmp/page.html
# 提取所有磁力链接
curl -s "https://www.6v520.com/zydy/2023-09-26/42788.html" | grep -o "magnet:?xt=[^\"<>]*"
# 提取特定集数（如138集）的链接

---

## 扩展经验（2026-04-27 补充）

### agent-browser ref 格式规范
- **必须加 @ 前缀**
  - ✅ `agent-browser --cdp 9222 fill @e20 "关键词"`
  - ❌ `agent-browser --cdp 9222 fill e20 "关键词"`（会报错）
- **snapshot 获取 ref**: 使用 `agent-browser snapshot @e20` 获取元素引用
- **适用场景**: 所有 agent-browser 的 fill/click/select 操作

### 截图分享规范（重要！）
- ❌ 错误：只用 localhost
  - `http://127.0.0.1:8888/xxx.png` — 用户打不开！
- ✅ 正确：获取真实 IP
  ```bash
  hostname -I | awk '{print $1}'  # → 192.168.1.210
  http://192.168.1.210:8888/xxx.png  # 验证200 OK后再分享
  ```

### sed 转义问题（易错！）
- ❌ 错误：单引号不转义
  - `sed 's/&amp;/\&/g'` → 输出 `\&` 而非 `&`
- ✅ 正确：双引号正确转义
  - `sed "s/&amp;/\&/g"` → 输出 `&`

---

---

## 闲鱼(goofish.com) CDP 自动化发布经验（2026-06-12 补充）

### 闲鱼登录 & Cookie 提取

#### 核心流程
1. **启动有界面浏览器**（用户需要手动登录）
   ```bash
   google-chrome --no-sandbox --disable-gpu --no-dev-shm-usage \
     --remote-debugging-port=9222 --remote-allow-origins=* \
     "https://www.goofish.com"
   ```
2. **用户手动登录**后，通过 CDP 提取完整 cookies（含 httpOnly）
   ```python
   ws.send(json.dumps({"id":1,"method":"Network.getAllCookies"}))
   ```
3. **关键 cookies**：
   - `havana_lgc2_77`（httpOnly）：base64 编码的用户信息，解码后有 hid、token、site
   - `sgcookie`（httpOnly）：会话标识
   - `cookie2`：用户标识哈希
   - `_tb_token_`：淘宝 token
   - `unb`：用户 ID（等同于 a1 的作用）
   - `tracknick`：用户名

#### ⚠️ 闲鱼没有直接的 a1 cookie
- `a1` 是淘宝 mtop SDK 在请求时动态计算的签名参数，不是静态 cookie
- 闲鱼用户唯一标识用 `unb`（如 748552523）
- `havana_lgc2_77` base64 解码后包含 hid（用户ID）和 token

#### Cookie 保存方式
- `.config/xianyu_cookies.txt` — 完整 cookie string
- `.config/xianyu_key_cookies.json` — 关键 cookies JSON
- `.config/xianyu_user_info.json` — 用户标识信息

### 闲鱼发布页面操作

#### 页面结构（2026-06-12 确认）
| 元素 | 类型 | 说明 |
|------|------|------|
| 图片上传 | input[type=file]（隐藏） | display:none，需通过 CDP 操作 |
| 宝贝描述 | contenteditable div | 最大 1500 字符，不支持 emoji |
| 价格 | input[type=text] | placeholder="0.00" |
| 原价 | input[type=text] | 可选 |
| 分类 | ant-select 下拉 | 如"DeepSeek服务" |
| 计价方式 | ant-select 下拉 | 元/次、元/时、元/课 |
| 服务类型 | ant-select 下拉 | 指令优化、模型搭建、本地部署、教学指导 |
| 发货设置 | ant-radio | 包邮/按距离计费/一口价/无需邮寄 |
| 所在地 | 自动填充 | 需提前在闲鱼设置常用地址 |
| 发布按钮 | button | 文本"发布" |

#### ⚠️ 闲鱼没有标题输入框！
- 商品标题自动从描述中提取

#### 图片上传的关键突破（重要！）
闲鱼上传组件是 React 组件，直接 DOM.setFileInputFiles 无法触发 React 事件。

**✅ 验证可用的方法：base64 编码注入**
```python
# 1. 读取图片文件并 base64 编码
with open("image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("ascii")

# 2. 分块传输到浏览器（避免单次表达式过大）
chunk_size = 50000
chunks = [img_b64[i:i+chunk_size] for i in range(0, len(img_b64), chunk_size)]
for i, chunk in enumerate(chunks):
    ws.send(json.dumps({"method":"Runtime.evaluate","params":{"expression":f"window.__imgB64='{chunk}';"}}))

# 3. 在浏览器内创建 Blob/File 并触发 change 事件
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

**❌ 失败的方法（不要再试）**
- DOM.setFileInputFiles → 触发 DOM.childNodeInserted 但闲鱼不识别
- Page.handleFileChooserDialog → Chrome 147 不支持此命令
- file:// 协议 fetch → 浏览器无法访问本地文件
- http://127.0.0.1 fetch → headless 模式下无法访问
- fake File 对象 → 闲鱼报"文件类型无法确定"

#### 下拉框操作
用 Input.dispatchMouseEvent 点击 ant-select-selector 打开下拉，然后用 .ant-select-item click() 选择选项。

#### 踩过的坑
1. **描述中不能包含 emoji** — 闲鱼会提示"商品描述不能包含emoji"
2. **httpOnly cookies 必须通过 CDP Network.getAllCookies 获取**
3. **端口冲突** — snap 版 Chromium(9223)和 google-chrome(9222)可能同时存在
4. **DOM 节点不稳定** — 关闭弹窗后 nodeId 会变，每次操作前重新获取
5. **wait_until='networkidle'** 在闲鱼 SPA 上永远等不到，必须用 'domcontentloaded'
6. **服务器 IP 被闲鱼风控** — 机房 IP 无法登录，必须用住宅 IP

### 完整发布流程
1. CDP 连接已登录的浏览器（9222端口）
2. 导航到 https://www.goofish.com/publish
3. 等待 8 秒 SPA 渲染
4. base64 注入图片 → 触发 change 事件 → 等待 8 秒上传
5. 填写描述（无 emoji）
6. 选择分类、计价方式、服务类型
7. 填写价格
8. 点击发布 → 等待 8 秒 → 确认结果

**最后更新**: 2026-06-12
**更新者**: media agent
**验证状态**: ✅ 已验证可用（成功发布"DeepSeek V4 API 包月畅用"）
