---
created: 2026-05-20T22:20:00
modified: 2026-05-20 23:31 GMT+8
tags:
  - experience
  - mail
  - skill
  - smtp
  - 邮件发送
aliases:
  - 邮件Skill安装配置经验
  - Mail Skill Setup Guide
---

# 📧 邮件 Skill 安装配置完整经验

> 日期：2026-05-20
> 场景：安装 ClawHub 邮件 skill、配置 163 邮箱发信、编写多收件人发信脚本

---

## 一、Skill 安装

### 1.1 搜索邮件 skill

```bash
clawhub search email
clawhub search mail
```

找到 3 个候选：
- `generic-mail-client` — 功能最全（IMAP/POP3 + SMTP，多账号，附件）
- `email` — 仅支持读取/搜索/转发
- `simple-mail-client` — 功能类似 generic-mail-client

**选择**：`generic-mail-client`（功能最全，支持发送+接收+附件）

### 1.2 安全审查

安装前先审查源码（skill-vetting 流程）：

```bash
# 下载到 /tmp 审查
cd /tmp
curl -L -o skill.zip "https://clawhub.ai/api/v1/download?slug=generic-mail-client"
mkdir skill-generic-mail-client && cd skill-generic-mail-client
unzip -q ../skill.zip

# 审查重点文件
cat config.yaml          # 检查是否有真实凭据（模板文件含 test-password 是正常的）
cat src/mailClient.ts    # 检查是否有恶意代码、隐蔽外发
cat src/index.ts         # 检查 prompt 注入
```

**审查结论**：
- ✅ 无 prompt 注入
- ✅ 无恶意代码
- ✅ config.yaml 中的 `test-password` 是模板示例，不是真实凭据
- ⚠️ 安全扫描标记 SUSPICIOUS（误报，因为 config.yaml 含 password 字样）

### 1.3 安装

```bash
cd ~/.openclaw
clawhub install generic-mail-client
```

安装路径：`~/.openclaw/workspace/skills/generic-mail-client/`

### 1.4 移动到全局 Skill 目录

全局 skill 目录：`~/.openclaw/skills/`（workspace 内的 skills 目录是工作区级）

```bash
cp -r ~/.openclaw/workspace/skills/generic-mail-client ~/.openclaw/skills/generic-mail-client
rm -rf ~/.openclaw/workspace/skills/generic-mail-client  # 清理旧目录
```

---

## 二、邮箱配置

### 2.1 核心认知：发信只需 SMTP

| 协议 | 用途 | 发信需要？ |
|------|------|-----------|
| **SMTP** | 发送邮件 | ✅ 必须 |
| **IMAP** | 接收邮件 | ❌ 不需要 |
| **POP3** | 接收邮件（旧协议） | ❌ 不需要 |

**结论**：如果只需要发信，只需要配置 SMTP 参数，IMAP/POP3 可以留空。

### 2.2 163 邮箱配置

**前提**：在 163 邮箱网页版开启 IMAP/SMTP 服务，并获取**授权码**（不是登录密码！）

获取授权码步骤：
1. 登录 https://mail.163.com
2. 设置 → POP3/SMTP/IMAP
3. 开启 IMAP/SMTP 服务
4. 生成授权码（类似 `ABCDEFG123456`）

**配置格式**（`config.yaml`）：

```yaml
mailAccounts:
  - id: "163-main"
    displayName: "163邮箱"
    smtp:
      host: "smtp.163.com"
      port: 465
      useTLS: true
    auth:
      username: "panbin5218@163.com"
      password: "授权码"    # 不是登录密码！
```

### 2.3 常见邮箱 SMTP 参数速查

| 邮箱 | SMTP 服务器 | 端口 | 加密 |
|------|------------|------|------|
| 163 | smtp.163.com | 465 | TLS |
| QQ | smtp.qq.com | 465 | TLS |
| 新浪 | smtp.sina.com | 465 | TLS |
| Gmail | smtp.gmail.com | 465 | TLS |
| Outlook | smtp.office365.com | 587 | STARTTLS |

> ⚠️ 所有邮箱都使用**授权码**而非登录密码。

---

## 三、发信脚本

### 3.1 为什么用 Python 而不是 Node.js？

`generic-mail-client` skill 的 Node.js 依赖（`nodemailer` + `imapflow`）需要 `npm install`，但服务器 npm 网络可能有问题（镜像源不可达）。

Python 的 `smtplib` 是标准库，无需额外安装，更稳定。

### 3.2 基础发信脚本

路径：`/root/.openclaw/share/send-email/send_email.py`

```python
#!/usr/bin/env python3
"""邮件发送工具 - 基于 SMTP"""

import smtplib
import argparse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

# 发信配置
SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SMTP_USER = "panbin5218@163.com"
SMTP_PASS = "授权码"

def send_email(to, subject, body=None, body_html=None, body_file=None,
               html_file=None, attachments=None, cc=None, bcc=None):
    """发送邮件，支持多收件人、附件、抄送、密送"""
    if isinstance(to, str):
        to = [to]

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(to)
    msg['Subject'] = subject

    # 正文
    if body_file:
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
    if body:
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
    if body_html:
        msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    # 附件
    if attachments:
        for filepath in attachments:
            filename = os.path.basename(filepath)
            mime_type, _ = mimetypes.guess_type(filepath)
            main_type, sub_type = mime_type.split('/', 1)
            with open(filepath, 'rb') as f:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)

    # 发送
    all_recipients = to[:]
    if cc: all_recipients += cc
    if bcc: all_recipients += bcc

    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, all_recipients, msg.as_string())
    server.quit()
    print(f"✅ 发送成功！收件人: {msg['To']}")
```

### 3.3 多收件人发信脚本

路径：`/root/.openclaw/share/send-email/send_email_multi.py`

支持从 `recipients.yaml` 读取收件人组：

```bash
# 从配置文件读取收件人组
python3 send_email_multi.py --group daily-report --subject "报告" --body "正文"

# 命令行指定收件人
python3 send_email_multi.py --to user1@a.com user2@b.com --subject "标题" --body "正文"

# 配置文件组 + 额外收件人
python3 send_email_multi.py --group daily-report --extra-to extra@c.com --subject "标题" --body "正文"

# 列出所有收件人组
python3 send_email_multi.py --list-groups
```

---

## 四、多收件人配置

### 4.1 配置文件方式（`recipients.yaml`）

适合固定收件人群组的重复发送：

```yaml
groups:
  daily-report:
    description: "每日分析报告收件人"
    recipients:
      - panbin521@sina.com
      - 29464262@qq.com

  all:
    description: "全部联系人"
    recipients:
      - panbin521@sina.com
      - 29464262@qq.com
```

### 4.2 命令行方式

适合临时发送：

```bash
python3 send_email.py --to user1@a.com user2@b.com user3@c.com --subject "标题" --body "正文"
```

### 4.3 混合方式

配置文件组 + 临时追加：

```bash
python3 send_email_multi.py --group daily-report --extra-to boss@company.com --subject "报告" --body "正文"
```

---

## 五、目录结构

```
~/.openclaw/skills/generic-mail-client/    # Skill（全局）
├── SKILL.md                               # Skill 说明
├── config.yaml                            # 邮箱账号配置
├── config.example.yaml                    # 配置模板
├── src/                                   # TypeScript 源码
└── dist/                                  # 编译产物

/root/.openclaw/share/send-email/           # 发信工具（共享）
├── README.md                              # 完整使用文档
├── send_email.py                          # 基础发信脚本
├── send_email_multi.py                    # 多收件人发信脚本
├── recipients.yaml                        # 收件人组配置
└── config.yaml                            # 邮箱账号配置（副本）
```

---

## 六、踩坑记录

### 坑 1：npm 网络问题

**现象**：`npm install` 报错 `ENOTFOUND mirrors.tencentyun.com`

**原因**：服务器 npm 镜像源不可达

**解决**：用 Python `smtplib`（标准库）替代 Node.js 依赖

### 坑 2：163 IMAP "不安全登录"

**现象**：IMAP 登录报错 `SELECT Unsafe Login. Please contact kefu@188.com for help`

**原因**：163 邮箱需要在设置中开启"IMAP/SMTP 客户端授权"

**解决**：如果只需要发信，不需要 IMAP，忽略此错误即可

### 坑 3：Python imaplib 兼容性问题

**现象**：`IMAP4_SSL('imap.163.com', 993, timeout=10)` 报错 `TypeError: __init__() got an unexpected keyword argument 'timeout'`

**原因**：Python 3.8 的 imaplib 不支持 timeout 参数

**解决**：去掉 timeout 参数

### 坑 4：config.yaml 中的占位符

**现象**：`password: "YOUR_AUTH_CODE_HERE"` 忘记替换

**后果**：发信认证失败

**建议**：配置完成后立即测试发信验证

### 坑 5：发信 vs 收信配置混淆

**误区**：以为发信需要配置收件人邮箱的密码

**正解**：发信只需要**发件人邮箱**的 SMTP 配置（host + port + 授权码），收件人地址直接 `--to` 指定即可，不需要任何密码

---

## 七、快速命令参考

```bash
# 发文本邮件
python3 /root/.openclaw/share/send-email/send_email.py \
  --to recipient@example.com --subject "标题" --body "正文"

# 发邮件（多收件人）
python3 /root/.openclaw/share/send-email/send_email.py \
  --to user1@a.com user2@b.com --subject "标题" --body "正文"

# 发邮件（带附件）
python3 /root/.openclaw/share/send-email/send_email.py \
  --to user@a.com --subject "报告" --body "正文" --attach report.pdf

# 发邮件（从文件读正文）
python3 /root/.openclaw/share/send-email/send_email.py \
  --to user@a.com --subject "报告" --body-file /path/to/report.md

# 多收件人（从配置文件）
python3 /root/.openclaw/share/send-email/send_email_multi.py \
  --group all --subject "报告" --body-file /path/to/report.md

# 列出收件人组
python3 /root/.openclaw/share/send-email/send_email_multi.py --list-groups
```

---

## 八、安全注意事项

1. **授权码不要泄露**：config.yaml 中的授权码相当于密码，不要上传到公开仓库
2. **使用授权码而非密码**：163/QQ/Gmail 等邮箱都支持生成应用专用授权码
3. **发送频率限制**：建议每分钟不超过 5 封，避免被识别为垃圾邮件
4. **附件大小限制**：163 邮箱单附件上限约 50MB
5. **不要在日志中输出邮件正文**：只记录发送结果和收件人地址

---

## 九、补充经验（2026-05-20 晚）

### 9.1 收件人角色分离

**误区**：把所有收件人都放在 `--to` 里，不区分主送/抄送。

**正解**：邮件协议支持三种收件人角色：
- **To（主送）**：主要收件人，邮件的直接目标
- **Cc（抄送）**：抄送收件人，知悉即可，不需要回复
- **Bcc（密送）**：密送收件人，其他收件人看不到

**配置方式**（`recipients.yaml`）：

```yaml
groups:
  all:
    description: "全部联系人"
    to:
      - panbin521@sina.com      # 主送
    cc:
      - 29464262@qq.com          # 抄送
```

**脚本支持**：`send_email_multi.py` 支持从配置文件读取 to/cc/bcc 分离的收件人组。

### 9.2 Emoji 在邮件客户端显示为 ???

**现象**：邮件标题或正文中的 emoji（如 📊、🔴、✅）在某些邮件客户端显示为 `???`。

**原因**：邮件客户端的字体不支持 Unicode emoji，或邮件编码问题。

**解决**：在 `md_to_html.py` 中将所有 emoji 替换为文字标签：
- `📊` → `[图表]`
- `🔴` → `[紧急]`
- `✅` → `[OK]`
- `❌` → `[NO]`
- `⚠️` → `[警告]`

### 9.3 PDF 无法直接嵌入邮件正文

**误区**：以为可以把 PDF 内容直接显示在邮件正文里。

**正解**：
- PDF 是二进制格式，邮件正文只能是文本/HTML
- **方案 A**：HTML 正文（把 MD 转成 HTML）+ PDF 附件（推荐）
- **方案 B**：只发 PDF 附件，正文写"请查看附件"

当前采用方案 A：`md_to_html.py` 生成 HTML 正文，`md_to_pdf.py` 生成 PDF 附件。

### 9.4 Cron 脚本中命令是给 AI 执行的

**场景**：`/root/.openclaw/share/final-analysis/*.cron` 脚本通过 heredoc 把 prompt 发给 AI，AI 再执行其中的命令。

**注意**：
- 命令格式要清晰，AI 需要理解并执行
- 不要在 prompt 中写 shell 管道等复杂语法，AI 可能解析错误
- 每个步骤分开写，如：
  ```
  4. 发送邮件到收件人组（all）：
     a. 将报告 MD 转为 PDF：python3 /path/to/md_to_pdf.py input.md output.pdf
     b. 生成 HTML 邮件：python3 /path/to/md_to_html.py input.md output.html
     c. 发送：python3 /path/to/send_email_multi.py --group all --subject "标题" --html-file output.html --attach output.pdf
  ```

### 9.5 npm 网络可能不可用

**现象**：`npm install` 报错 `ENOTFOUND`。

**解决**：优先使用 Python 标准库：
- 发信：`smtplib`（标准库）替代 `nodemailer`
- 收信：`imaplib`（标准库）替代 `imapflow`
- MD 转 HTML：`markdown`（pip install markdown）
- MD 转 PDF：`reportlab`（pip install reportlab）

### 9.6 完整邮件发送流程（Cron 集成）

每份报告生成后的标准流程：

```
1. 保存报告 → report/YYYY-MM-DD.md
2. message 发送到 webchat
3. md_to_pdf.py → /tmp/report.pdf
4. md_to_html.py → /tmp/report.html（去 emoji）
5. send_email_multi.py --group all → 发送（HTML 正文 + PDF 附件）
```

---

## 十、邮件 HTML 格式美化经验（2026-05-21）

> 场景：优化报告邮件的 HTML 排版，参考招商银行、新浪邮箱等正规金融机构邮件样式

### 10.1 设计原则

参考了 5 个真实邮件样本：

| 邮件 | 来源 | 可借鉴点 |
|------|------|---------|
| 每日信用管家 | 招商银行 | 清爽专业、信息密度高 |
| 信用卡电子账单 | 招商银行 | 简洁排版、固定宽度表格 |
| 防范钓鱼邮件 | 新浪邮箱 | 圆角卡片、渐变色标题、清晰视觉层次 |
| 沟通记录 | 猎聘 | 紧凑布局、信息分组清晰 |
| 自己发的尾盘报告 | — | 发现了标题英文堆砌、表格简陋等问题 |

**核心原则**：
1. 清爽专业，不过度设计
2. 信息层次清晰，视觉分组明确
3. 表格自适应，手机上可横向滚动
4. 涨跌颜色遵循 A 股惯例（红涨绿跌）
5. 适配主流邮件客户端（内联样式优先）

### 10.2 邮件 HTML 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* 外层容器：圆角卡片 + 阴影 */
    .email-wrapper { max-width: 780px; margin: 20px auto; border-radius: 12px;
                     overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }

    /* 顶部标题栏：渐变色 + 报告类型 badge */
    .email-header { background: linear-gradient(135deg, #1a3a5c, #2d6a9f); padding: 28px 36px; }
    .report-type { display: inline-block; background: rgba(255,255,255,0.15);
                   border-radius: 20px; padding: 4px 16px; font-size: 12px; }
    .divider { width: 40px; height: 3px; background: rgba(255,255,255,0.4);
               margin: 14px auto 0; border-radius: 2px; }

    /* 表格：外层 wrapper 支持横向滚动 */
    .table-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
    table { table-layout: fixed; word-break: break-all; min-width: 520px; }

    /* 状态标签 */
    .tag-red { background: #fce4ec; color: #c62828; border: 1px solid #ef9a9a; }
    .tag-orange { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
    .tag-green { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }

    /* 信息卡片 */
    .info-card { background: #f8fafb; border-radius: 8px; padding: 16px 20px; }
    .info-card.warning { background: linear-gradient(135deg, #fff8f0, #fff3e0); }
    .info-card.danger { background: linear-gradient(135deg, #fff5f5, #fce4ec); }

    /* 响应式 */
    @media (max-width: 600px) {
      .email-wrapper { margin: 0; border-radius: 0; }
      .email-body { padding: 20px; }
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="email-header">
      <div class="report-type">Final 财务总监 · 尾盘分析</div>
      <h1>2026-05-21 尾盘分析报告</h1>
      <div class="divider"></div>
    </div>
    <div class="email-body">
      <!-- MD → HTML 内容 -->
    </div>
    <div class="email-footer">
      <p>Final 财务总监 · 仅供参考，投资需谨慎</p>
    </div>
  </div>
</body>
</html>
```

### 10.3 md_to_html.py 关键处理逻辑

路径：`/root/.openclaw/share/send-email/md_to_html.py`

**预处理（MD → HTML 之前）：**

1. **修复加粗标题直接跟列表**：
   ```python
   # 模式：**xxx**：\n- xxx → 插入空行让 md 正确解析为列表
   md_text = re.sub(r'(\*\*[^*]+\*\*[：:])\n(- )', r'\1\n\n- ', md_text)
   md_text = re.sub(r'(\d+\.\s+\*\*[^*]+\*\*[：:])\n(- )', r'\1\n\n- ', md_text)
   ```
   - 问题：`**盘中走势特征**：\n- xxx` 会被 md 合并成 `<p>` 而非 `<ul>`
   - 解决：在 `**xxx**：` 和 `- ` 之间插入空行

2. **去掉 emoji**：所有 emoji 替换为文字标签（`📊` → `[图表]`），避免邮件客户端显示 `???`

**后处理（HTML 生成之后）：**

3. **表格加 wrapper**：
   ```python
   html = html.replace('<table>', '<div class="table-wrapper"><table>')
               .replace('</table>', '</table></div>')
   ```

4. **blockquote 内信息换行**：
   ```python
   # 在 <strong> 标签前插入 <br>（排除第一个）
   def _fix_bq(m):
       inner = m.group(1)
       inner = re.sub(r'\s*<strong>', '\n<br><strong>', inner)
       inner = re.sub(r'(<p>)\n<br>', r'\1', inner, count=1)
       return '<blockquote>' + inner + '</blockquote>'
   html = re.sub(r'<blockquote>(.*?)</blockquote>', _fix_bq, html, flags=re.DOTALL)
   ```

### 10.4 常见格式问题及解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 加粗标题后的 `- ` 列表显示为段落 | MD 解析器不识别无空行的列表 | 预处理插入空行 |
| 表格在手机上挤在一起 | 无自适应布局 | `table-wrapper` + `overflow-x: auto` + `table-layout: fixed` |
| 文件头多行信息挤在一段 | blockquote 内多个 `<strong>` 无换行 | 在 `<strong>` 前插入 `<br>` |
| emoji 显示为 `???` | 邮件客户端不支持 Unicode emoji | 替换为文字标签 `[图表]` 等 |
| 嵌套列表缩进丢失 | MD 嵌套列表需要 4 空格缩进 | 确保源文件格式正确 |

### 10.5 表格列宽最佳实践

- 列数 ≤ 5：直接用 `width: 100%`，手机可正常显示
- 列数 > 5：必须加 `table-wrapper`（`overflow-x: auto`），允许横向滚动
- 含长文本的列：加 `word-break: break-all` 防止撑破布局
- 固定列宽：`table-layout: fixed` 让列宽均匀分配

### 10.6 字体选择

邮件客户端兼容的字体栈：
```css
font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
```

避免使用：
- 衬线字体（邮件中可读性差）
- 非系统字体（邮件客户端不支持加载外部字体）
- 字号小于 12px（手机上难以阅读）

### 10.7 颜色规范

```css
/* 主色调 */
--primary-dark: #1a3a5c;    /* 深蓝 - 标题栏、表头 */
--primary: #2d6a9f;         /* 中蓝 - 章节标题左边框 */
--bg-light: #f0f2f5;        /* 背景灰 */
--bg-card: #f8fafb;         /* 卡片背景 */
--text-main: #444;          /* 正文 */
--text-strong: #222;        /* 加粗文字 */

/* A 股涨跌色 */
--up: #e53935;              /* 红 - 涨 */
--down: #43a047;            /* 绿 - 跌 */

/* 状态标签色 */
--tag-red: #fce4ec;         /* 紧急/危险 */
--tag-orange: #fff3e0;      /* 警告/关注 */
--tag-green: #e8f5e9;       /* 安全/正常 */
--tag-blue: #e3f2fd;        /* 信息/提示 */
```

---

*最后更新：2026-05-21 19:18*
