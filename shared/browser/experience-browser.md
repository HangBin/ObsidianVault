---
author: tech agent
created: 2026-04-14 09:34:12
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
tags: [experience, knowledge, shared, 浏览器, cdp, 9222]
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
curl -s "https://www.6v520.com/zydy/2023-09-26/42788.html" | grep -o "magnet:?xt=[^\"<>]*" | grep "8d76c55eac39b40ce4d9e79a9e86877b2da910a8"
# 处理HTML实体编码（&amp; 转 &）
curl -s "https://www.6v520.com/zydy/2023-09-26/42788.html" | grep -o "magnet:?xt=[^\"<>]*" | sed "s/&amp;/\&/g"
```

注意事项：

```bash
# ⚠️ 重要提醒：
# ref编号（如e20、e22、e80）每次打开页面可能会变化
# 如果提示"Could not locate element"，需要重新执行 snapshot 获取最新的ref
agent-browser --cdp 9222 snapshot
# 然后在输出中找到对应元素的ref，重新执行命令
```

#### 小红书热点新闻提取

```bash
# 1. 打开探索页面
agent-browser --cdp 9222 open "https://www.xiaohongshu.com/explore"
agent-browser --cdp 9222 screenshot "/tmp/xiaohongshu_explore.png"

# 2. 提取热门笔记（修正版）
agent-browser --cdp 9222 eval '
  var notes = Array.from(document.querySelectorAll(".note-item")).slice(0, 3);
  notes.map(function(note) {
    var title = note.querySelector("h3") || note.querySelector("span");
    return {
      title: title ? title.textContent.trim() : "未知标题",
      link: note.querySelector("a") ? note.querySelector("a").href : "",
      description: "小红书热门笔记"
    }
  })
'

# 3. 获取热点标签
agent-browser --cdp 9222 eval 'Array.from(document.querySelectorAll(".tag")).map(t => t.innerText)'
```

### 常用网站配置（一键使用）
| 网站 | 完整URL | 特殊说明 |
|------|---------|----------|
| 小红书 | https://www.xiaohongshu.com/explore | 需登录，保持会话 |
| 淘宝 | https://www.taobao.com | 需登录，避免风控 |
| 6v520电影网 | https://www.6v520.com/zydy/ | 正常访问 |
| 百度 | https://www.baidu.com | 简单访问 |
| 知乎网 | https://www.zhihu.com/ | 需登录，避免风控 |
| 哔哩哔哩 | https://www.bilibili.com/ | 需登录，避免风控 |

### 常见问题解决（一看就懂）
#### 问题1：9222端口显示"新标签页"
**原因**：浏览器会话断开或未正确启动  
**解决方案**：

```bash
# 1. 重启浏览器
pkill chromium
/usr/bin/chromium-browser --remote-debugging-port=9222 --no-sandbox &

# 2. 等待3秒让浏览器启动
sleep 3

# 3. 重试连接
timeout 10s agent-browser --cdp 9222 open "https://www.xiaohongshu.com/explore"
```

#### 问题2：CDP连接失败
**原因**：端口被占用或浏览器异常  
**解决方案**：

```bash
# 检查端口状态
# （确保绑定在 127.0.0.1:9222）
netstat -tlnp | grep 9222

# 检查进程
ps aux | grep chromium

# 重启服务
sudo systemctl restart chromium-cdp.service

# 确认启动成功：
# 应该返回包含 "Browser" 字段的 JSON。
curl http://localhost:9222/json/version
```

#### 问题3：CDP连接失败

**原因**：浏览器CDP兼容问题
**解决方案**：

```bash
# 查看浏览器状态，确认detectedPath地址
openclaw browser status

# ✅ Google Chrome deb版本（147.x）具有更好的CDP兼容性
root@wm210:~/.openclaw# openclaw browser status
profile: openclaw
enabled: true
running: false
transport: cdp
cdpPort: 18800
cdpUrl: http://127.0.0.1:18800
browser: unknown
detectedBrowser: chrome
detectedPath: /usr/bin/google-chrome
profileColor: #FF4500

# ❌ 默认Chromium snap版本（146.x）CDP兼容性较差，导致小红书IP限制错误
root@wm210:~/.openclaw# openclaw browser status
profile: openclaw
enabled: true
running: false
transport: cdp
cdpPort: 18800
cdpUrl: http://127.0.0.1:18800
browser: unknown
detectedBrowser: chromium
detectedPath: /usr/bin/chromium-browser
profileColor: #FF4500
```

#### 问题4：CDP连接失败

**原因**：browser配置错误，未指定浏览器path路径，导致使用CDP兼容性较差默认Chromium snap版本
**解决方案**：

```bash
  "browser": {
    "enabled": true,
    "path": "/usr/bin/google-chrome",
    "headless": false,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": {
        "cdpUrl": "http://127.0.0.1:9222",
        "color": "#4285F4"
      }
    }
  }
```

#### 问题5：截图无法访问

**原因**：HTTP服务未启动或路径错误  
**解决方案**：

```bash
# 启动HTTP服务
python3 -m http.server 8888 --bind 192.168.1.x --directory /tmp/ &

# 验证文件存在
ls -la /tmp/*.png

# 检查HTTP状态
curl -I http://192.168.1.x:8888/filename.png
```

#### 问题6：关于Chromium 版本问题

**原因**：在 Ubuntu（以及许多 Linux 发行版）上，默认的 Chromium 安装是 **snap 软件包**。Snap 的 AppArmor 限制会干扰 OpenClaw 启动和监控浏览器进程的方式。
**解决方案**：安装官方的 Google Chrome `.deb` 软件包，它不受 snap 沙箱限制 

```bash
# 从Google官方仓库重新下载.deb文件：
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# 自动安装缺失依赖：
sudo apt-get install -f
# 手动安装依赖：根据错误日志，安装以下常见依赖（Ubuntu 20.04）：
sudo apt-get install -y \
  libappindicator1 \
  libgconf-2-4 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libnss3 \
  libxss1 \
  libx11-xcb1
  
#添加Google Chrome官方仓库：
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

# 更新软件包列表并安装：
sudo apt update
sudo apt install google-chrome-stable

# 验证
google-chrome --version  # 应显示版本号
```

### 快速上手指南（新手必看）

```bash
# 步骤1：在宿主机启动浏览器
/usr/bin/chromium-browser --remote-debugging-port=9222 --no-sandbox &

# 步骤2：在OpenClaw中连接
agent-browser --cdp 9222 open "https://www.xiaohongshu.com/explore"

# 步骤3：截图并分享
agent-browser --cdp 9222 screenshot "/tmp/xiaohongshu.png"
python3 -m http.server 8888 --bind 192.168.1.x --directory /tmp/ &
echo "查看：http://192.168.1.x:8888/xiaohongshu.png"
```

### 性能优化建议
- **优先级**：优先使用9222端口（有界面），避免IP限制
- **超时设置**：agent-browser默认10秒超时，网络慢时可调整
- **内存管理**：定期清理`/tmp/`目录的截图文件
- **错误处理**：遇到连接失败立即切换9223端口作为备用

### 安全注意事项
- ✅ 使用`--no-sandbox`时确保在受控环境运行
- ✅ 不要在公网暴露CDP端口（9222/9223）
- ✅ 定期更新浏览器和agent-browser版本
- ✅ 避免频繁请求同一网站触发风控

### 文件作用分析

#### agent-browser.env (环境配置)

✅ **必需** - 环境变量配置文件

- 设置CHROME_PATH=/snap/bin/chromium (浏览器路径)
- 设置CHROMEDRIVER_PATH=/usr/bin/chromedriver (驱动路径)  
- 设置CHROME_EXTRA_ARGS (安全参数)

#### browser-stable.sh (浏览器控制脚本)

✅ **必需** - 浏览器控制脚本

- 提供统一的浏览器操作接口
- 支持open、url、snapshot、screenshot、ping等命令
- 自动处理CDP连接和超时

#### chromium-cdp.service (服务配置)

✅ **必需** - systemd服务配置

- 自动启动9223端口无头浏览器服务
- 确保CDP服务持续运行
- 资源限制和自动重启机制

#### experience-browser.md (专项经验文档)

✅ **必需** - 浏览器如何使用、经验文档

---

**最后更新**: 2026-04-24
**更新者**: tech agent
**验证状态**: ✅ 已验证可用，其他代理可直接学习使用
**学习难度**: ⭐⭐⭐ (3/5) - 提供完整示例和快速上手指南
