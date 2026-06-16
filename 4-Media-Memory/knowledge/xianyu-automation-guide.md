---
title: 闲鱼自动化经验指南
date: 2026-06-10
last_updated: 2026-06-15 18:36
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
> bash /home/bill/run.sh xianyu-products/test-item-001
> ```
> 先检查登录态：`bash /home/bill/run.sh --check`

---

## 1. 快速启动指南（⭐ 每次必读）

### 1.1 标准发布流程（3 步）

```
Step 1: 检查登录态
  bash /home/bill/run.sh --check

Step 2a: 登录态正常 → 从商品目录发布（推荐）
  bash /home/bill/run.sh xianyu-products/test-item-001

Step 2b: 登录态失效 → 截图二维码 → 发给用户扫码 → 等确认 → 再发布
```

**铁律：先检查 → 失效就发二维码 → 不做多余分析**

### 1.2 run.sh 命令速查

```bash
# 从商品目录发布（推荐 ⭐）
bash /home/bill/run.sh xianyu-products/test-item-001

# 命令行指定（临时/测试用）
bash /home/bill/run.sh --image /path/to/img.png --desc '商品描述' --price 0.01

# 仅检查登录态
bash /home/bill/run.sh --check

# 使用配置文件（/home/bill/config.json）
bash /home/bill/run.sh --config product.json

# 批量发布
bash /home/bill/run.sh --batch products.json
```

### 1.3 商品目录结构（推荐方式）

商品统一存放在 `xianyu-products/` 目录下，每个商品一个子目录：

```
xianyu-products/
└── test-item-001/
    ├── product.json       # 商品信息（名称、描述、价格、分类）
    └── image.png          # 商品图片
```

**product.json 格式：**
```json
{
  "name": "商品名称",
  "description": "商品描述（用于发布）",
  "price": 0.01,
  "category": "分类名称",
  "status": "draft|published|failed",
  "created": "2026-06-15T11:50:00+08:00",
  "image": "image.png"
}
```

> run.sh 会自动在商品目录下查找图片文件（支持 png/jpg/jpeg/webp），
> 无需在 product.json 中写完整路径，只需写文件名。

### 1.4 快速创建新商品

```bash
# 1. 创建商品目录
mkdir -p xianyu-products/my-item-002

# 2. 放入图片
cp ~/my-photo.png xianyu-products/my-item-002/image.png

# 3. 创建 product.json
cat > xianyu-products/my-item-002/product.json << 'EOF'
{
  "name": "我的商品",
  "description": "商品描述信息",
  "price": 99,
  "category": "其他服务",
  "status": "draft",
  "created": "2026-06-15T12:00:00+08:00",
  "image": "image.png"
}
EOF

# 4. 发布
bash /home/bill/run.sh xianyu-products/my-item-002
```

---

## 2. 脚本架构

| 文件 | 功能 | 说明 |
|------|------|------|
| `/home/bill/run.sh` | **一键入口** | 启动 Chrome → 注入 cookies → 检查登录态 → 发布 |
| `/home/bill/xianyu_start.sh` | Chrome 启动脚本 | xvfb-run 启动 Chrome（被 run.sh 内部调用） |
| `/home/bill/xianyu_publish.py` | 发布核心 | CDP 自动化：上传图片 → 填写信息 → 发布 |
| `/home/bill/extract_xianyu_cookies.py` | Cookies 提取 | CDP 优先获取明文 cookies，SQLite 降级 |

**run.sh 自动完成全流程，不需要单独跑 xianyu_start.sh 或 xianyu_publish.py。**

### 2.1 商品目录（xianyu-products/）

```
xianyu-products/
├── README.md              # 目录规范说明
├── test-item-001/         # 每个商品一个子目录
│   ├── product.json       # 商品信息
│   └── image.png          # 商品图片
└── ...
```

- 命名规范：`{类型}-{序号}`（如 `test-item-001`、`product-001`）
- 发布时 run.sh 自动在目录下查找图片，支持 png/jpg/jpeg/webp
- 详细规范见 `xianyu-products/README.md`

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

当 cookies 彻底过期时，执行以下**完整标准流程**：

#### ⭐ 完整登录恢复流程（每次照做，不要自己思考）

**Step 1: 启动 Chrome**
```bash
cd /home/bill && bash xianyu_start.sh
```
脚本会自动检测 CDP 端口就绪（最多 20s）并检测登录态。

**Step 2: 检查登录态输出**
- `✅ 闲鱼已登录，发布页面就绪！` → **跳到 Step 6（直接发布）**
- `⚠️ 首页已加载但未登录` → 继续 Step 3
- `❌ 需要登录` → 继续 Step 3

**Step 3: 获取二维码截图（CDP + PIL 裁剪）**

通过 CDP 找到登录页面的二维码区域（在 iframe `passport.goofish.com/mini_login.htm` 中），裁剪并保存：

```python
python3 << 'PYEOF'
import json, urllib.request, asyncio, websockets, base64
from io import BytesIO
from PIL import Image

async def get_qrcode():
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    pages = json.loads(resp.read())
    goofish = [p for p in pages if "goofish.com" in p.get("url","") and "xdomain" not in p.get("url","")][0]
    async with websockets.connect(goofish["webSocketDebuggerUrl"]) as ws:
        # 点击登录按钮（顶部导航栏的登录按钮，class=item--m9jSTUup）
        # ⚠️ 有两个登录元素：<a class="item--m9jSTUup"> 是顶部栏按钮（正确的），<a href="...login"> 是链接
        await ws.send(json.dumps({"id":1,"method":"Runtime.evaluate","params":{"expression":
            """(() => {
                // 优先选顶部导航栏的登录按钮
                const navBtn = document.querySelector('a.item--m9jSTUup');
                if (navBtn) { navBtn.click(); return 'clicked_nav_login'; }
                // 备选：有 href 的登录链接
                const linkBtn = document.querySelector('a[href*="goofish.com/login"]');
                if (linkBtn) { linkBtn.click(); return 'clicked_link_login'; }
                return 'no_login_button';
            })()"""}}))
        await ws.recv()
        await asyncio.sleep(5)  # iframe 需要 3-5 秒加载

        # 找到 passport iframe 位置
        await ws.send(json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression":
            """(() => {
                const iframes = document.querySelectorAll('iframe');
                for (const iframe of iframes) {
                    if (iframe.src.includes('passport.goofish.com')) {
                        const rect = iframe.getBoundingClientRect();
                        return JSON.stringify({x: rect.x, y: rect.y, width: rect.width, height: rect.height});
                    }
                }
                return 'no iframe';
            })()"""}}))
        r = json.loads(await ws.recv())
        info = json.loads(r["result"]["result"]["value"])

        # 截图
        await ws.send(json.dumps({"id":3,"method":"Page.captureScreenshot","params":{"format":"png"}}))
        r = json.loads(await ws.recv())
        img = Image.open(BytesIO(base64.b64decode(r["result"]["data"])))

        # 裁剪二维码区域
        # ⚠️ 先截整个 iframe 放大 3x 发原图，确保二维码完整
        ix = int(info['x'])
        iy = int(info['y'])
        iw = int(info['width'])
        ih = int(info['height'])
        crop = img.crop((ix, iy, ix + iw, iy + ih))
        crop = crop.resize((iw * 3, ih * 3), Image.LANCZOS)
        crop.save("/tmp/xianyu_qrcode_login.png")
        print(f"二维码截图已保存: {crop.size}")
        print(f"二维码截图已保存: {crop.size}")

asyncio.run(get_qrcode())
PYEOF
```

**Step 4: 验证二维码有效性（⭐ 2026-06-15 新增，发送前必做）**

⚠️ **铁律：发送前必须先验证二维码是否有效！** 不要直接截图就发。

验证方法（两步）：
1. **OCR 识别**：对截图运行 OCR，检查是否包含"二维码已失效"文字
2. **innerText 检查**：通过 CDP 执行 `document.body.innerText.includes('二维码已失效')`

```python
# OCR 验证
result = subprocess.run(
    ['tesseract', '/tmp/xianyu_qrcode_login.png', 'stdout', '-l', 'chi_sim+eng', '--psm', '6'],
    capture_output=True, text=True, timeout=30
)
if '二维码已失效' in result.stdout:
    print("❌ 二维码已失效，需要重启 Chrome")
    # 执行重启流程（见 Step 4.5）
```

```python
# innerText 双重检查
await ws.send(json.dumps({"id":4,"method":"Runtime.evaluate","params":{
    "expression": "document.body.innerText.includes('二维码已失效')"
}}))
r = json.loads(await ws.recv())
if r["result"]["result"]["value"]:
    print("❌ 二维码已失效")
```

**只有两步都确认没有"二维码已失效"，才能发送给用户。**

**Step 5: 发送二维码给用户**

⚠️ **铁律：用 `read` 工具读取图片文件，Gateway 会自动将图片注入到回复中！**

**发送步骤：**
1. 截图保存到任意位置
2. 用 `read` 工具读取截图文件：`read(path="/tmp/xianyu_qrcode_login.png")`
3. Gateway 会自动将图片上传到 outgoing media 目录
4. 在回复中写文字说明：`请用手机闲鱼 APP 扫码登录 ✅`
5. **⚠️ 不要在回复中写 `MEDIA:` 指令或图片路径！** 否则会渲染出重复图片（Gateway 自动注入 + 手动 MEDIA: 指令 = 双倍图片）
6. **⚠️ 不要在回复中写图片文件名或路径！** 任何图片路径都会被 Gateway 再次注入

**踩坑记录（2026-06-16）：**
- ❌ `MEDIA:/tmp/xxx.png` — webchat 不渲染 `/tmp/` 路径
- ❌ `MEDIA:/root/.openclaw/canvas/xxx.png` — 虽然能渲染，但和 Gateway 自动注入叠加导致重复图片
- ❌ 回复中写图片文件名/路径 — Gateway 会再次注入导致重复
- ✅ `read` 工具读取图片 + 回复中只写文字 — Gateway 自动注入一张图片（唯一正确方式）

**Step 4.5: 判断"快速进入"按钮（⭐ 2026-06-15 新增，截图后判断）**

⚠️ **关键限制**："快速进入"按钮在跨域 iframe (`passport.goofish.com`) 里，`document.body.innerText` 无法访问 iframe 内容（跨域限制）。必须通过**截图视觉识别**来判断。

判断流程（截图后观察）：
1. 查看 Step 3 截图的登录弹窗区域
2. **有账户名 + "快速进入"/"一键登录"按钮** → 点击快速进入：
   - 先尝试通过 CDP frameId 在 iframe context 中查找（可能因跨域失败）
   - 如果失败，用**坐标点击**（通过 OCR tsv 输出获取按钮精确坐标）
   - 等 5 秒，检查是否已登录
3. **只有二维码 + "其他账号登录"** → 截图发给用户扫码（Step 4）
4. **二维码已失效** → **重启 Chrome**（⭐ 2026-06-15 新增）：
   ```bash
   # ⚠️ 分三步执行，避免 pkill 误杀当前进程！
   # 第一步：清理锁文件
   rm -f /home/bill/.config/google-chrome/SingletonLock
   rm -f /home/bill/.config/google-chrome/SingletonSocket
   rm -f /home/bill/.config/google-chrome/SingletonCookie
   rm -f /home/bill/.config/google-chrome/DevToolsActivePort
   # 第二步：杀掉 Chrome（用 exec background 模式避免误杀）
   pkill -9 -f google-chrome
   sleep 3
   # 第三步：重新启动
   cd /home/bill && bash xianyu_start.sh
   ```
   ⚠️ **铁律：pkill 必须放在独立的 exec 步骤中执行，不要和启动命令放在同一个 shell 脚本里！** 否则当前进程会被 SIGKILL。
   然后重新走 Step 2-4。

⚠️ **iframe 跨域限制详情**：
- `contentDocument` / `contentWindow.document` 被跨域拦截
- `Runtime.evaluate` 的 `frameId` 参数在 Chrome 147 里对跨域 iframe 无效
- 唯一可靠方式是截图视觉识别

### 3.4 截图二维码标准方式（已合并到 3.3）

> **已整合到 §3.3「完整登录恢复流程」Step 3-4 中，不再单独使用。**
> 核心要点速查：
> - 二维码在 `passport.goofish.com` 的 iframe 中 → 用 PIL 裁剪（见 Step 3）
> - **用 `MEDIA:` 指令在回复中嵌入原图**，不用 `message` 工具
> - **先判断是否有"快速进入"按钮**（截图视觉识别，见 Step 4.5）
> - **iframe 跨域无法 DOM 访问**
> - **二维码失效时重启 Chrome**
> - **发送前必须验证二维码有效性**（OCR + innerText 双重检查）

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

⚠️ **已知限制**：
- `xvfb-run` 启动的 Chrome 被闲鱼风控检测虚拟桌面，**cookies 注入后仍可能无法登录**
- 如果 `xvfb-run` 方式无法登录，需要在 `:0` 真实桌面启动 Chrome
- `:0` 启动方式（在 pts/3 等有 DISPLAY 的终端执行）：
  ```bash
  export DISPLAY=:0
  /opt/google/chrome/chrome --remote-debugging-port=9222 --remote-allow-origins=* --no-sandbox --disable-gpu --password-store=basic --user-data-dir=/home/bill/.config/google-chrome https://www.goofish.com &
  ```
- CDP 连接后如果 `json/list` 返回空，确认 `--remote-allow-origins=*`（不能写 `http://127.0.0.1:9222`）

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
| 06-15 | message 工具 media/filePath 参数发图失败 | webchat/qqbot channel 不支持 | **用 MEDIA: 指令在回复中嵌入原图** |
| 06-15 | 截图裁剪区域错误（截到空白） | 没确认二维码位置 | 先打开登录页截图检查，确认二维码在右侧再裁剪 |
| 06-15 | 重复分析已有方案，浪费时间 | 没先读经验文档 | **先读 run.sh 再动手，不造轮子** |
| 06-15 | 分类"其他服务"不支持网页版发布 | 闲鱼网页版限制 | 用"手机"等支持的分类 |
| 06-15 | 描述中包含 emoji 被闲鱼拒绝 | 闲鱼不允许 emoji | **描述中不要包含 emoji** |
| 06-15 | run.sh 的 xvfb-run 被闲鱼检测 | 虚拟桌面被反爬拦截 | 用 `xianyu_start.sh`（xvfb-run）启动 Chrome，CDP 9222 端口通常可用 |
| 06-15 | 自己反复 kill Chrome 导致登录态丢失 | 不该动已有的 Chrome | **不要 kill 已有 Chrome**，直接用 CDP 连接 |
| 06-15 | 截图二维码发给用户但用户看不到 | 用了错误的方式发图 | **用 `MEDIA:` 指令在回复中直接嵌入原图** |
| 06-15 | 截图二维码已失效但直接发给了用户 | 没有先验证二维码有效性 | **发送前必须 OCR + innerText 双重检查"二维码已失效"** |
| 06-15 | 登录页面有"快速进入"按钮但没识别 | 没有检查快速进入按钮 | **先检查是否有账户名+快速进入按钮，有就直接点** |

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
| 自己写截图+OCR+发送代码 | 截图后在回复中直接写 `MEDIA:/path/to/img.png` |
| 截图后直接发送不验证 | 先 OCR + innerText 检查"二维码已失效"，确认有效再发 |
| 自己尝试刷新 cookies | 发二维码让用户扫码 |
| 用 `message` 工具的 `media`/`filePath` 发图 | **不支持，会返回 delivery-mirror** | 在回复中直接写 `MEDIA:/path/to/img.png` |
| 重新分析 ant-select 操作 | 用 dispatchKeyEvent（已验证） |
| 尝试 API 方式发布 | 用 CDP 浏览器自动化（API 有风控） |
| 每次手动传 `--image --desc --price` | 用商品目录：`run.sh xianyu-products/xxx` |
| 自己写 cookies 提取脚本 | 用 `extract_xianyu_cookies.py`（CDP 优先） |

---

## 11. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 一键发布脚本 | `/home/bill/run.sh` | 入口脚本 |
| Chrome 启动脚本 | `/home/bill/xianyu_start.sh` | xvfb-run 启动 |
| 发布核心脚本 | `/home/bill/xianyu_publish.py` | CDP 自动化核心 |
| Cookies 提取脚本 | `/home/bill/extract_xianyu_cookies.py` | CDP 优先，SQLite 降级 |
| 商品目录规范 | `xianyu-products/README.md` | 命名/结构/流程 |
| 浏览器自动化经验 | `/home/obsidian_vault/shared/browser/` | CDP 操作参考 |
| 每日日志 | `memory/2026-06-12.md` | CDP 发布实操 |
| 每日日志 | `memory/2026-06-13.md` | xvfb-run + CDP 实操 |
| 每日日志 | `memory/2026-06-15.md` | run.sh 验证 + 经验更新 + 商品目录迁移 |
