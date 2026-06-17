---
title: 闲鱼自动化经验指南
date: 2026-06-10
last_updated: 2026-06-16 12:26
tags:
  - xianyu
  - goofish
  - publish
  - experience
  - cdp
  - browser-automation
  - xvfb
  - automation
  - cookies
  - product-catalog
author: media
---

# 闲鱼自动化经验指南

> **⚡ 快速开始：每次发布只需一条命令：**
> ```bash
> bash /home/bill/run.sh /root/.openclaw/workspace-media/xianyu-products/test-item-001
> ```
> 先检查登录态：`bash /home/bill/run.sh --check`

---

## 1. 快速启动指南（⭐ 每次必读）

### 1.1 标准发布流程（3 步）

```
Step 1: 检查登录态
  bash /home/bill/run.sh --check

Step 2a: 登录态正常 → 从商品目录发布（推荐）
  bash /home/bill/run.sh /root/.openclaw/workspace-media/xianyu-products/test-item-001

Step 2b: 登录态失效 → 截图二维码 → 发给用户扫码 → 等确认 → 再发布
```

**铁律：先检查 → 失效就发二维码 → 不做多余分析**

### 1.1.1 防重复造轮子清单（⭐ 每次必读）

> **先读这个清单，不要做多余的事。所有"不要做"都有已验证的替代方案。**

| ❌ 不要做 | ✅ 正确做法 |
|-----------|----------|
| 自己写 CDP 脚本分析 fiber 树 | 直接跑 `run.sh` |
| 自己写代码检测登录态 | `run.sh --check` |
| 自己写截图+OCR+发送代码 | 截图后在回复中写 `MEDIA:/path/to/img.png` |
| 截图后直接发送不验证 | 先 OCR + innerText 检查"二维码已失效"，确认有效再发 |
| 自己尝试刷新 cookies | 发二维码让用户扫码 |
| 在 product.json 里写 category 字段 | **不写 category**，让闲鱼自动识别分类（2026-06-17 验证：不写分类比写"手机"更稳定） |
| 用 `message` 工具的 `media`/`filePath` 发图 | 在回复中写 `MEDIA:/path/to/img.png` |
| 重新分析 ant-select 操作 | 用 dispatchKeyEvent（已验证） |
| 尝试 API 方式发布 | 用 CDP 浏览器自动化（API 有风控） |
| 每次手动传 `--image --desc --price` | 用商品目录：`run.sh /root/.openclaw/workspace-media/xianyu-products/xxx`（绝对路径） |
| 自己写 cookies 提取脚本 | 用 `extract_xianyu_cookies.py`（CDP 优先） |

### 1.2 run.sh 命令速查

```bash
# 从商品目录发布（推荐 ⭐）
bash /home/bill/run.sh /root/.openclaw/workspace-media/xianyu-products/test-item-001

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

商品统一存放在工作区的 `xianyu-products/` 目录下，每个商品一个子目录：

```
/root/.openclaw/workspace-media/xianyu-products/
└── test-item-001/
    ├── product.json       # 商品信息（名称、描述、价格、分类）
    └── image.png          # 商品图片
```

> ⚠️ **2026-06-16 修正**：商品目录实际路径为 `/root/.openclaw/workspace-media/xianyu-products/`，不在 `/home/bill/` 下。run.sh 支持商品目录参数，会自动查找 `product.json`。

**product.json 格式：**
```json
{
  "name": "商品名称",
  "desc": "商品描述（用于发布）",
  "price": 0.01,
  "status": "draft|published|failed",
  "created": "2026-06-15T11:50:00+08:00",
  "image": "image.png"
}
```

> ⚠️ **字段名是 `desc` 不是 `description`**！run.sh 的 `load_config()` 只读 `cfg.get('desc','')`，写 `description` 会导致描述为空白。

> ⚠️ **2026-06-17 更新：不需要 `category` 字段！** 不指定分类让闲鱼自动识别，发布更稳定。指定分类（如 `"手机"`）反而可能导致"网页版不支持该分类"错误。run.sh 不传 `--category` 时 `xianyu_publish.py` 自动跳过分类选择。

> run.sh 会自动在商品目录下查找图片文件（支持 png/jpg/jpeg/webp），
> 无需在 product.json 中写完整路径，只需写文件名。

### 1.4 快速创建新商品

```bash
# 1. 创建商品目录
mkdir -p /root/.openclaw/workspace-media/xianyu-products/my-item-002

# 2. 放入图片
cp ~/my-photo.png /root/.openclaw/workspace-media/xianyu-products/my-item-002/image.png

# 3. 创建 product.json
cat > /root/.openclaw/workspace-media/xianyu-products/my-item-002/product.json << 'EOF'
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
bash /home/bill/run.sh /root/.openclaw/workspace-media/xianyu-products/my-item-002
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

### 2.1 商品目录

```
/root/.openclaw/workspace-media/xianyu-products/
├── README.md              # 目录规范说明
├── test-item-001/         # 每个商品一个子目录
│   ├── product.json       # 商品信息
│   └── image.png          # 商品图片
└── ...
```

- **绝对路径**：`/root/.openclaw/workspace-media/xianyu-products/`（工作区内）
- **发布时传参**：必须传绝对路径，因为 run.sh 在 `/home/bill/` 执行，相对路径会解析到 `/home/bill/xianyu-products/`（不存在）
- 命名规范：`{类型}-{序号}`（如 `test-item-001`、`product-001`）
- 发布时 run.sh 自动在目录下查找图片，支持 png/jpg/jpeg/webp
- 详细规范见 `/root/.openclaw/workspace-media/xianyu-products/README.md`

---

## 3. 登录态管理

### 3.1 登录态检查

```bash
bash /home/bill/run.sh --check
```

输出：
- `✅ 登录态正常` → 直接发布
- `⚠️ 需要登录` → 需要用户扫码

> ⚠️ **2026-06-16 补充**：run.sh 的 `check_login()` 比上述流程更复杂：
> 1. 检测关键词：`立即登录`/`登录后可以更懂你` → NEED_LOGIN，`宝贝描述`/`描述一下` → READY，`panbin5218`/`订单` → LOGGED_IN_HOME
> 2. 如果未登录 → **自动尝试注入 cookies + 刷新重试**（不是直接报失败）
> 3. 注入失败才最终报 `❌ 登录态恢复失败`

### 3.2 登录态恢复（自动）

run.sh 启动 Chrome 时会自动注入 session cookies（从持久化路径 `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt` 读取）。
**大部分情况下 cookies 注入即可恢复登录态，不需要用户扫码。**

> ⚠️ **2026-06-17 修正**：`COOKIES_FILE` 已从 `/tmp/xianyu_cookies.txt`（重启会丢）改为持久化路径 `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt`，重启后不丢失。

⚠️ **踩坑提醒**：
- Cookie 必须包含完整字段（cookie2、sgcookie、_m_h5_tk 等），缺少字段会导致所有 API 返回 `FAIL_SYS_ILLEGAL_ACCESS`
- **不要 kill 已有 Chrome**：Chrome 里有 session cookies（httpOnly），重启后会丢失。直接用 CDP 连接复用登录态
- 如果 Chrome 已自动重启（crash watchdog），session cookies 会丢失 → 通过 CDP `Network.setCookie` 注入之前保存的 cookies（见 §5.4）
- ⚠️ **2026-06-17 新增：run.sh 检测 UNKNOWN 但实际已登录** — 发布商品后页面会跳转到 `/item?id=xxx`（商品详情页），此时 run.sh 的 `check_login()` 在首页找不到 `panbin5218`/`订单` 关键词，返回 `UNKNOWN`。**实际登录态正常**，直接调 `python3 xianyu_publish.py publish --image ... --desc ... --price ...` 即可绕过检测正常发布。不需要重启 Chrome 或重新扫码。

### 3.2.1 Cookies 持久化存储

> **2026-06-16 新增**：Cookies 默认存储在 `/root/.openclaw/workspace-media/.config/`（工作区持久化目录）。

| 文件 | 说明 |
|------|------|
| `xianyu_cookies_latest.txt` | 最新提取的 cookies（每次更新） |
| `xianyu_cookies.txt` | 持久化副本 |

**自动备份机制**：
- `extract_cookies.py` 提取 cookies 后自动备份到工作区 `.config/`
- `run.sh` 的 `inject_session_cookies()` 注入成功后，自动从 Chrome 提取最新 cookies 并备份
- `/tmp/xianyu_cookies.txt` 仅作为临时读取文件，**重启后会丢失**

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

⚠️ **铁律：在回复中直接写 `MEDIA:/path/to/image.png`，Gateway 会自动注入图片到 webchat 回复！**

**发送方式（3种，按优先级排序）：**

| 方式 | 写法 | webchat 显示 | 浏览器打开 | 推荐 |
|------|------|-------------|-----------|------|
| **方式1** | 回复中写 `MEDIA:/tmp/xxx.png` | ✅ 直接显示 | ✅ 能打开 | ⭐ **首选** |
| **方式2** | `read` 工具读图片 | ❌ 不注入 | — | ❌ 不用 |
| **方式3** | `assistant-media` ticket URL | ❌ 需登录 | ✅ 能打开 | ⚠️ 备选 |

**正确写法（方式1）：**
```
🔑 请用闲鱼 APP 扫码登录

MEDIA:/tmp/xianyu_qrcode.png
```

**⚠️ 注意事项：**
1. **只写一行 `MEDIA:`！** 不要同时用 `read` 工具读图片（会叠加导致重复）
2. **不要写图片的 ticket URL + MEDIA: 同时** = 重复图片
3. **MEDIA: 后面跟的是服务器本地路径**（`/tmp/`、`/root/` 等），不是 URL
4. **Gateway 会自动把图片注入到 webchat 回复中**，用户直接看到图片

**踩坑记录（2026-06-16 验证）：**
- ❌ `read` 工具读取图片 — webchat 里 Gateway 不自动注入，看不到
- ❌ `assistant-media` ticket URL — webchat 里需要登录才能打开
- ❌ `message` 工具的 `MEDIA:` 参数 — webchat 里报 "requires target" 错误
- ✅ `MEDIA:/tmp/xxx.png` 写在回复里 — webchat 直接显示图片（2026-06-16 验证通过）

**Step 4.5: 判断"快速进入"按钮（⭐ 2026-06-15 新增，截图后判断）**

⚠️ **关键限制**："快速进入"按钮在跨域 iframe (`passport.goofish.com`) 里，`document.body.innerText` 无法访问 iframe 内容（跨域限制）。必须通过**截图视觉识别**来判断。

判断流程（截图后观察）：
1. 查看 Step 3 截图的登录弹窗区域
2. **有账户名 + "快速进入"/"一键登录"按钮** → 点击快速进入：
   ```python
   # 通过 OCR tsv 获取按钮坐标（tsv 输出第12-15列是 x1,y1,x2,y2）
   result = subprocess.run(
       ['tesseract', '/tmp/xianyu_qrcode_login.png', 'stdout',
        '-l', 'chi_sim+eng', '--psm', '6', 'tsv'],
       capture_output=True, text=True, timeout=30
   )
   for line in result.stdout.split('\n'):
       cols = line.split('\t')
       if len(cols) >= 15 and '快速进入' in cols[11]:
           x1, y1, x2, y2 = int(cols[12]), int(cols[13]), int(cols[14]), int(cols[15])
           cx, cy = (x1+x2)//2, (y1+y2)//2
           await ws.send(json.dumps({"id:99,"method":"Input.dispatchMouseEvent","params":{
               "type":"mousePressed","x":cx,"y":cy,"button":"left","clickCount":1
           }}))
           await ws.recv()
           await ws.send(json.dumps({"id:100,"method":"Input.dispatchMouseEvent","params":{
               "type":"mouseReleased","x":cx,"y":cy,"button":"left","clickCount":1
           }}))
           await ws.recv()
           print(f"✅ 已点击快速进入按钮 ({cx},{cy})")
           break
   else:
       print("⚠️ 未找到快速进入按钮，尝试 frameId 方式")
       # 备选：通过 CDP frameId（可能因跨域失败）
       # 如果失败，直接截图发给用户扫码
   ```
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

⚠️ **踩坑提醒**：
- **截图裁剪区域**：二维码在右侧（x 从 250 开始），不在左侧。裁剪前先看截图确认位置
- **重复分析已有方案**：run.sh 已验证可用，不需要自己写 CDP 脚本从头分析
- **xvfb-run 被闲鱼检测**：虚拟桌面可能被反爬拦截，导致二维码立即失效。如果多次重启仍失效，考虑用真实桌面 Chrome

### 3.5 Cookie 文件位置

| 文件 | 说明 |
|------|------|
| `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt` | **主文件**（持久化，run.sh 注入来源） |
| `/root/.openclaw/workspace-media/.config/xianyu_cookies_latest.txt` | 最新提取备份 |

> ⚠️ **2026-06-17 修正**：run.sh 的 `COOKIES_FILE` 已改为持久化路径 `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt`，重启后不丢失。`/tmp/xianyu_cookies.txt` 不再作为读取路径。

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

⚠️ **踩坑提醒**：
- **部分分类不支持网页版发布**（如"其他服务"）：需用手机闲鱼 APP 完成，或选择"手机"等支持的分类
- **分类自动识别有延迟**：上传图片后需等 3 秒让页面完成识别
- **价格 React state 可能不同步**：DOM 设值后 React 可能未识别，但实际发布时以 DOM 值为准

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

**关键**：`xvfb-run --auto-servernum` 自动创建虚拟 X Server 并设置 `DISPLAY`（无需手动 export），这是唯一可行的方案。

> ⚠️ run.sh 中 `CHROME_BIN="/usr/bin/google-chrome"`（软链接），不是直接写 `/opt/google/chrome/chrome`。

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

⚠️ **踩坑提醒**：
- **fetch 返回的 fileId 可能嵌套在 `object` 字段中**：`data.get("fileId") or data.get("object",{}).get("fileId")`
- **描述中不要包含 emoji**：闲鱼会拒绝发布，提示"商品描述不能包含emoji"
- **wait_until='networkidle' 在闲鱼 SPA 上永远等不到**：用 `'domcontentloaded'`
- **fiber 树深度可达 71 层**：上传组件在更深位置，BFS 可能覆盖不全 → 直接用 run.sh 已验证的方案

### 5.3 Ant Design Select 操作

**唯一可行方案**：CDP `Input.dispatchKeyEvent` 逐字输入（Ant Design 5 拦截合成事件，click/insertText 均无效）

⚠️ **踩坑提醒**：
- **必须 focus 搜索框再 keyEvent**：否则 keyEvent 不会输入到搜索框
- **选项在 portal 渲染**：下拉菜单不在 Select DOM 内，而在 body 末尾
- **精确匹配选项**：用 `textContent.trim() === '目标' && children.length === 0` 避免误匹配

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

### 5.5 分类识别失败：网页版不支持该分类

**故障现象**：
```
📂 Step 8.5: 检查分类...
⚠️ 当前分类网页版不支持发布，需要修改分类
   当前分类: 其他服务
   网页版暂不支持发布此分类，请使用闲鱼APP扫码继续发布
```

**根因**：
闲鱼根据图片内容自动识别分类。如果图片特征不明显（如纯色图、非商品图片），会被归为"其他服务"分类，而"其他服务"在网页版不支持发布。

**案例 1：纯色图被识别为"其他服务"**
- 图片尺寸：800x800
- 颜色：纯橙色 (255, 87, 51)
- 识别结果：其他服务
- 尝试分类修正失败：下拉列表里只有"其他服务"的子分类，没有"手机"等主流分类

**解决方法 1：生成正确的商品图片**
```python
# 使用 PIL 生成手机特征图片
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 800), (240, 240, 245))
draw = ImageDraw.Draw(img)
# 画手机轮廓 + 屏幕内容
draw.rounded_rectangle([200, 100, 600, 700], radius=40, fill=(60, 60, 70))
draw.rounded_rectangle([220, 140, 580, 660], radius=20, fill=(135, 206, 235))
img.save("image.png")
```
重新上传后分类自动识别为"手机"，发布成功。

**解决方法 2：通过 CDP 手动修改分类**
在 `xianyu_publish.py` 的 Step 8（截图确认）和 Step 9（点击发布）之间插入分类检查和修正。

**发布成功验证**：
```
✅ 发布完成！
   最终页面: 测试_闲鱼 | https://www.goofish.com/item?id=1059579249693
```
商品ID: 1059579249693，链接: https://www.goofish.com/item?id=1059579249693

**经验教训**：
1. 图片内容决定分类识别——纯色图会被归为"其他服务"
2. 优先用正确的商品图片，手动修改分类是兜底方案

### 5.6 run.sh 配置加载失败：bash 内嵌 python 引号冲突

**故障现象**：
```bash
bash run.sh xianyu-products/test-item-001
# 输出：
Traceback (most recent call last):
  File "<string>", line 14
NameError: name 'desc' is not defined
```

**根因**：
run.sh 的 `load_config()` 函数用 `python3 -c "..."` 内嵌 python 代码，但 f-string 里的双引号在 bash 双引号中被截断。

**解决方法**：改用外部脚本 `_load_config.py`（详见 5.7 外部脚本文件说明）



> **补充 1：load_config 输出格式**
> - 旧：三行（img\\ndesc\\nprice），read 只读第一行
> - 新：一行空格分隔（img desc price）

> **补充 2：category 参数传递**
> ```bash
> local CAT=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('category',''))")
> publish "$IMAGE" "$DESC" "$PRICE" "$CAT"
> ```

> **补充 3：check_and_fix_category/select_category**
> 见 5.5 分类识别失败的代码示例。

> **补充 4：CDPSession.send_cdp → .send**
> ```python
> # ❌
> await session.send_cdp("Input.dispatchKeyEvent", {...})
> # ✅
> await session.send("Input.dispatchKeyEvent", {...})
> ```

> **补充 5：生成手机图片**
> ```python
> from PIL import Image, ImageDraw
> img = Image.new('RGB', (800, 800), (240, 240, 245))
> draw = ImageDraw.Draw(img)
> draw.rounded_rectangle([200, 100, 600, 700], radius=40, fill=(60, 60, 70))
> img.save("image.png")
> ```
### 5.7 发布成功案例（2026-06-16）

**商品**：test-item-001（测试商品）
**最终发布**：2026-06-16 13:10
**结果**：✅ 成功上架

**关键数据**：
- 商品ID: 1059579249693
- 链接: https://www.goofish.com/item?id=1059579249693
- 描述: 测试
- 价格: ¥0.01
- 分类: 手机
- 图片: 800x800 手机特征图（PIL 生成）

**修复链路**：
1. Cookies 自动备份 → 扫码后自动保存到工作区 `.config/`
2. run.sh 修复 → 支持从 product.json 读取 category 并传递
3. 图片生成 → 用 PIL 生成手机特征图代替纯色图
4. 分类修正 → 上传后自动识别为"手机"，无需手动修正
5. 发布成功 → 商品ID 1059579249693

**验证方式**：
- 浏览器访问 https://www.goofish.com/item?id=1059579249693
- 查看闲鱼个人中心"我发布的"页面

Chrome 重启后 session cookies（`cookie2`、`XSRF-TOKEN` 等）会丢失。run.sh 通过 CDP `Network.setCookie` 自动注入恢复。

---


**现象**：
`product.json` 有 `category` 字段，但 `xianyu_publish.py` 收不到分类参数。

**根因**：
`run.sh` 的 `publish()` 函数定义了 3 个参数（image、desc、price），没有 category。调用处也没传 category。

**解决方法**：
```bash
# run.sh 修改 publish() 函数
publish() {
    local image="$1" desc="$2" price="$3" category="$4"
    
    local cat_arg=""
    [ -n "$category" ] && cat_arg="--category $category"
    
    python3 "$SCRIPT_DIR/xianyu_publish.py" publish \
        --image "$image" \
        --desc "$desc" \
        --price "$price" $cat_arg
}

# 调用处从 product.json 读取 category
local CAT=""
if [ -n "$CONFIG" ]; then
    CAT=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('category',''))" 2>/dev/null)
fi
publish "$IMAGE" "$DESC" "$PRICE" "$CAT"
```



**新建文件**：
| 文件 | 路径 | 说明 |
|------|------|------|
| `_backup_cookies.py` | `/home/bill/_backup_cookies.py` | CDP 提取 cookies 并备份到工作区 `.config/` |
| `_load_config.py` | `/home/bill/_load_config.py` | 加载 product.json，输出空格分隔的 img/desc/price |

**为什么用外部脚本**：
1. **避免引号嵌套冲突**：bash `python3 -c "..."` 内嵌 python 代码时，f-string 的引号会被 bash 解析
2. **提高可维护性**：外部脚本可单独测试、调试
3. **避免语法错误**：bash 解析 `python3 -c` 时代码块必须完整，内部不能有 bash 命令



**商品**：test-item-001（测试商品）
**最终发布**：2026-06-16 13:10
**结果**：✅ 成功上架

**关键数据**：
- 商品ID: 1059579249693
- 链接: https://www.goofish.com/item?id=1059579249693
- 描述: 测试
- 价格: ¥0.01
- 分类: 手机
- 图片: 800x800 手机特征图（PIL 生成）

**修复链路**：
1. Cookies 自动备份 → 扫码后自动保存到工作区 `.config/`
2. run.sh 修复 → 支持从 product.json 读取 category 并传递
3. 图片生成 → 用 PIL 生成手机特征图代替纯色图
4. 分类修正 → 上传后自动识别为"手机"，无需手动修正
5. 发布成功 → 商品ID 1059579249693

**验证方式**：
- 浏览器访问 https://www.goofish.com/item?id=1059579249693
- 查看闲鱼个人中心"我发布的"页面
## 6. 消息读取（2026-06-17 新增）

### 6.1 消息入口

闲鱼网页版消息页面：`https://www.goofish.com/im`

> ⚠️ 需要有效 cookies 登录态。如果 cookies 过期，会跳转到登录页。

### 6.2 页面结构

| 区域 | 说明 |
|------|------|
| 左侧列表 | 联系人列表，每个联系人显示：昵称 + 最后消息预览 + 时间 |
| 右侧区域 | 当前选中联系人的完整聊天记录 |
| 顶部导航 | 搜索、消息、通知消息 |

### 6.3 读取消息列表的步骤

**Step 1: 确保登录态有效**
```bash
# 检查登录态
bash /home/bill/run.sh --check
# 如果 cookies 过期，先注入持久化 cookies
python3 -c "
import json, urllib.request, asyncio, websockets
async def inject():
    resp = urllib.request.urlopen('http://127.0.0.1:9222/json/list')
    pages = json.loads(resp.read())
    page = [p for p in pages if 'goofish.com' in p.get('url','') and 'xdomain' not in p.get('url','')][0]
    async with websockets.connect(page['webSocketDebuggerUrl']) as ws:
        with open('/root/.openclaw/workspace-media/.config/xianyu_cookies.txt') as f:
            cookies = [p.strip().split('=',1) for p in f.read().strip().split('; ') if '=' in p]
        for name, value in cookies:
            await ws.send(json.dumps({'id':1,'method':'Network.setCookie','params':{'name':name,'value':value,'domain':'.goofish.com','path':'/'}}))
            await ws.recv()
asyncio.run(inject())
"
```

**Step 2: 导航到消息页面**
```javascript
// 通过 CDP 执行
await ws.send(json.dumps({'id':1,'method':'Page.navigate','params':{'url':'https://www.goofish.com/im?spm=a21ybx.personal.sidebar.2.43346ac297N2Ah'}}))
```

**Step 3: 等待页面加载后读取联系人列表**
```javascript
// 读取左侧联系人列表
await ws.send(json.dumps({'id':2,'method':'Runtime.evaluate','params':{'expression':'''
(() => {
    const allDivs = document.querySelectorAll('div');
    const contacts = [];
    for (const div of allDivs) {
        if (div.children.length >= 2) {
            const rect = div.getBoundingClientRect();
            if (rect.width > 100 && rect.height > 30 && rect.height < 120) {
                const text = div.textContent.trim();
                if (text.length > 3 && text.length < 100) {
                    contacts.push({
                        text: text.substring(0, 60),
                        rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height}
                    });
                }
            }
        }
    }
    return JSON.stringify(contacts);
})()
'''}}))
```

**Step 4: 点击联系人读取详细对话**
```javascript
// 点击第 i 个联系人（从 0 开始）
// 先获取联系人坐标
const contact = contacts[i];
const cx = contact.x + contact.w / 2;  // 中心 x
const cy = contact.y + contact.h / 2;  // 中心 y

await ws.send(json.dumps({'id':3,'method':'Input.dispatchMouseEvent','params':{'type':'mousePressed','x':cx,'y':cy,'button':'left','clickCount':1}}))
await ws.recv()
await ws.send(json.dumps({'id':4,'method':'Input.dispatchMouseEvent','params':{'type':'mouseReleased','x':cx,'y':cy,'button':'left','clickCount':1}}))
await ws.recv()
await asyncio.sleep(2);  // 等待右侧聊天区域更新

// 读取右侧聊天内容
await ws.send(json.dumps({'id':5,'method':'Runtime.evaluate','params':{'expression':'document.body.innerText.substring(0, 2000)'}}))
```

### 6.4 注意事项

1. **需要有效 cookies**：消息页面需要登录态，cookies 过期会跳转登录页
2. **联系人列表 DOM 不稳定**：闲鱼 SPA 的 DOM 结构可能随时调整，选择器可能需要更新
3. **右侧聊天区域更新有延迟**：点击联系人后需等 1-2 秒让右侧区域加载完成
4. **不能自动回复**：读取消息可行，但发送消息需要模拟键盘输入，且闲鱼可能有反爬检测
5. **通知消息**："通知消息"是系统通知（如交易状态变化），不是用户私信

### 6.5 已验证结果（2026-06-17）

- ✅ 消息页面可正常加载
- ✅ 联系人列表可读取（6 个联系人）
- ✅ 每个联系人的最后消息预览可获取
- ⚠️ 右侧聊天区域在点击联系人后未完全切换（可能是 SPA 路由缓存），实际聊天内容需要进一步验证

---

## 7. 已验证成功案例

| 商品 | 价格 | 商品ID | 日期 | 方式 |
|------|------|--------|------|------|
| DeepSeek V4 API 包月畅用 | ¥4.00 | — | 06-12 | CDP fiber 注入 |
| Claude Opus 4.8 API | ¥0.09 | 1057911158600 | 06-13 | run.sh 一键 |
| Claude Opus 4.8 API（测试） | ¥0.09 | 1057127547428 | 06-13 | run.sh 一键 |
| MacBook Pro M4 Pro 14寸 | ¥8888 | 1059835968742 | 06-13 | run.sh 一键 |
| 周杰伦签名专辑（测试） | ¥888,888 | 1059858208480 | 06-13 | run.sh 一键 |
| 测试商品 | ¥0.01 | — | 06-15 | run.sh 一键 |
| 测试商品-001 | ¥0.01 | 1057980679964 | 06-17 | run.sh 一键（无category） |
| 测试商品-002 | ¥0.02 | 1057981571117 | 06-17 | xianyu_publish.py 手动（run.sh检测UNKNOWN） |

---

## 8. 环境信息

| 项目 | 值 |
|------|-----|
| Chrome | google-chrome（非 snap chromium） |
| Chrome 路径 | `/usr/bin/google-chrome`（软链接 → `/etc/alternatives/google-chrome`，实际指向 `/opt/google/chrome/chrome`） |
| Chrome 实际二进制 | `/opt/google/chrome/chrome` |
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
5. **pkill 误杀风险**：重启 Chrome 时 `pkill -9 -f google-chrome` 可能误杀当前 shell 进程（包括 run.sh 自身）。**铁律**：pkill 必须放在独立的 exec 步骤中，不要和启动命令在同一个 shell 里执行
6. **二维码有效期 > 60秒**：闲鱼登录二维码在 60 秒内未检测到失效，实际有效期可能更长。失效检测需要更长时间等待或依赖 innerText 判断
8. **"快速进入"按钮出现条件**：只有在 Chrome profile 中有历史登录记录（`tracknick`、`unb` 等 cookies 存在且有效）时才会出现。重启 Chrome + 清除 cookies 后只显示扫码登录。该按钮在跨域 iframe 中，只能通过截图视觉识别（OCR + tsv 坐标定位）
7. **run.sh cookies 注入时机**：run.sh 从持久化路径 `/root/.openclaw/workspace-media/.config/xianyu_cookies.txt` 读取 cookies。重启后 `/tmp/` 被清空不影响，持久化目录中的 cookies 始终可用。extract_cookies.py 提取后会自动备份到此路径
5. **run.sh 不支持 `--help`**：传 `--help` 会报"未知参数"并退出

---

## 10. 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 一键发布脚本 | `/home/bill/run.sh` | 入口脚本 |
| Chrome 启动脚本 | `/home/bill/xianyu_start.sh` | xvfb-run 启动 |
| 发布核心脚本 | `/home/bill/xianyu_publish.py` | CDP 自动化核心 |
| Cookies 提取脚本 | `/home/bill/extract_xianyu_cookies.py` | CDP 优先，SQLite 降级 |
| 商品目录规范 | `/root/.openclaw/workspace-media/xianyu-products/README.md` | 命名/结构/流程（工作区内） |
| 浏览器自动化经验 | `/home/obsidian_vault/shared/browser/` | CDP 操作参考 |
| 每日日志 | `memory/2026-06-12.md` | CDP 发布实操 |
| 每日日志 | `memory/2026-06-13.md` | xvfb-run + CDP 实操 |
| 每日日志 | `memory/2026-06-15.md` | run.sh 验证 + 经验更新 + 商品目录迁移 |


