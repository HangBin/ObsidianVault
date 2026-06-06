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

**最后更新**: 2026-04-27
**更新者**: tech agent
**验证状态**: ✅ 已验证可用
