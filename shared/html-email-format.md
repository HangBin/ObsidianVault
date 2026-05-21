---
created: 2026-05-21T19:18:00
modified: 2026-05-21 21:11 GMT+8
tags: [experience, knowledge, shared, html, email, 邮件格式]
aliases: [HTML邮件格式美化经验, 邮件模板经验, html-email-format]
---

# 📧 HTML 邮件格式美化经验
> 独立经验文档，记录邮件 HTML 模板设计与格式优化的完整经验

> 场景：优化 A 股分析报告邮件的 HTML 排版，参考招商银行、新浪邮箱等正规金融机构邮件样式
> 日期：2026-05-21
> 相关文件：[[mail-skill-setup-guide]]（邮件发送配置经验）

---

## 一、参考样本分析

分析了 5 个真实邮件样本，提取可借鉴的排版经验：

| 邮件 | 来源 | 可借鉴点 |
|------|------|---------|
| 每日信用管家 | 招商银行 | 清爽专业、信息密度高 |
| 信用卡电子账单 | 招商银行 | 简洁排版、固定宽度表格 |
| 防范钓鱼邮件 | 新浪邮箱 | 圆角卡片、渐变色标题、清晰视觉层次 |
| 沟通记录 | 猎聘 | 紧凑布局、信息分组清晰 |
| 自己发的尾盘报告（原版） | — | 发现标题英文堆砌、表格简陋、状态标记纯文本等问题 |

---

## 二、设计原则

1. **清爽专业** — 不过度设计，参考金融机构邮件风格
2. **信息层次清晰** — 视觉分组明确，标题/正文/数据一目了然
3. **表格自适应** — 手机上可横向滚动，不挤在一起
4. **A 股惯例** — 红涨绿跌
5. **邮件客户端兼容** — 内联样式优先，不依赖外部 CSS

---

## 三、HTML 模板结构

### 3.1 整体布局

```
email-wrapper（圆角卡片 + 阴影）
├── email-header（渐变色标题栏）
│   ├── report-type（报告类型 badge）
│   ├── h1（报告标题）
│   └── divider（装饰分隔线）
├── email-body（内容区域）
│   └── MD → HTML 内容
└── email-footer（底部声明）
```

### 3.2 顶部标题栏

```css
.email-header {
  background: linear-gradient(135deg, #1a3a5c 0%, #2d6a9f 60%, #1a3a5c 100%);
  padding: 28px 36px 24px;
  text-align: center;
}
.report-type {
  display: inline-block;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 20px;
  padding: 4px 16px;
  font-size: 12px;
}
.divider {
  width: 40px; height: 3px;
  background: rgba(255,255,255,0.4);
  margin: 14px auto 0;
  border-radius: 2px;
}
```

### 3.3 章节标题

```css
h2 {
  color: #2d6a9f;
  padding-left: 12px;
  border-left: 4px solid #2d6a9f;  /* 左边框强调 */
}
```

### 3.4 状态标签

用彩色标签替代纯文本标记（`[红]`、`[OK]`、`[警告]`）：

```css
.tag-red    { background: #fce4ec; color: #c62828; border: 1px solid #ef9a9a; }
.tag-orange { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
.tag-green  { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
.tag-blue   { background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
.tag-gray   { background: #f5f5f5; color: #616161; border: 1px solid #e0e0e0; }
```

### 3.5 信息卡片

```css
.info-card { background: #f8fafb; border-radius: 8px; padding: 16px 20px; }
.info-card.highlight { background: linear-gradient(135deg, #f0f7ff, #e8f4fd); }  /* 蓝色-提示 */
.info-card.warning   { background: linear-gradient(135deg, #fff8f0, #fff3e0); }  /* 橙色-警告 */
.info-card.danger    { background: linear-gradient(135deg, #fff5f5, #fce4ec); }  /* 红色-危险 */
```

---

## 四、md_to_html.py 关键处理逻辑

路径：`/root/.openclaw/share/send-email/md_to_html.py`

### 4.1 预处理（MD → HTML 之前）

#### 修复加粗标题直接跟列表

```python
# 模式：**xxx**：\n- xxx → 插入空行让 md 正确解析为列表
md_text = re.sub(r'(\*\*[^*]+\*\*[：:])\n(- )', r'\1\n\n- ', md_text)
md_text = re.sub(r'(\d+\.\s+\*\*[^*]+\*\*[：:])\n(- )', r'\1\n\n- ', md_text)
```

**问题**：`**盘中走势特征**：\n- xxx` 会被 markdown 合并成 `<p>` 而非 `<ul>`
**解决**：在 `**xxx**：` 和 `- ` 之间插入空行

#### 去掉 emoji

```python
# 所有 emoji 替换为文字标签，避免邮件客户端显示 ???
emoji_map = {'📊': '[图表]', '🔴': '[紧急]', '✅': '[OK]', '⚠️': '[警告]', ...}
```

### 4.2 后处理（HTML 生成之后）

#### 表格加 wrapper

```python
html = html.replace('<table>', '<div class="table-wrapper"><table>') \
           .replace('</table>', '</table></div>')
```

#### Blockquote 内信息换行

```python
def _fix_bq(m):
    inner = m.group(1)
    # 在每个 <strong> 前插入 <br>（排除 <p> 后的第一个）
    inner = re.sub(r'\s*<strong>', '\n<br><strong>', inner)
    inner = re.sub(r'(<p>)\n<br>', r'\1', inner, count=1)
    return '<blockquote>' + inner + '</blockquote>'
html = re.sub(r'<blockquote>(.*?)</blockquote>', _fix_bq, html, flags=re.DOTALL)
```

---

## 五、常见格式问题及解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 加粗标题后的 `- ` 列表显示为段落 | MD 解析器不识别无空行的列表 | 预处理插入空行 |
| 表格在手机上挤在一起 | 无自适应布局 | `table-wrapper` + `overflow-x: auto` + `table-layout: fixed` |
| 文件头多行信息挤在一段 | blockquote 内多个 `<strong>` 无换行 | 在 `<strong>` 前插入 `<br>` |
| emoji 显示为 `???` | 邮件客户端不支持 Unicode emoji | 替换为文字标签 `[图表]` 等 |
| 嵌套列表缩进丢失 | MD 嵌套列表需要 4 空格缩进 | 确保源文件格式正确 |

---

## 六、表格列宽最佳实践

| 列数 | 方案 |
|------|------|
| ≤ 5 列 | 直接用 `width: 100%`，手机可正常显示 |
| > 5 列 | 必须加 `table-wrapper`（`overflow-x: auto`），允许横向滚动 |
| 含长文本的列 | 加 `word-break: break-all` 防止撑破布局 |
| 均匀列宽 | `table-layout: fixed` 让列宽均匀分配 |
| 最小宽度 | `min-width: 520px` 防止压扁 |

---

## 七、字体选择

邮件客户端兼容的字体栈：

```css
font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
```

**避免使用**：
- 衬线字体（邮件中可读性差）
- 非系统字体（邮件客户端不支持加载外部字体）
- 字号小于 12px（手机上难以阅读）

---

## 八、颜色规范

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

## 九、关键经验速查

| # | 问题 | 解决方案 |
|---|------|----------|
| 1 | Emoji 显示为 `???` | 替换为文字标签（`📊`→`[图表]`、`🔴`→`[紧急]`、`⚠️`→`[警告]`） |
| 2 | 表格在手机上挤在一起 | 外层包 `<div class="table-wrapper">`（`overflow-x: auto`） <br/>`table-layout: fixed` + `word-break: break-all` <br/>`min-width: 520px` 防止压扁 |
| 3 | 加粗标题直接跟 `- ` 列表被合并成段落 | 预处理插入空行：`re.sub(r'(\*\*[^*]+\*\*[：:])\n(- )', r'\1\n\n- ', md_text)` |
| 4 | Blockquote 内多个 `<strong>` 挤在一段 | 在 `<strong>` 前插入 `<br>`（排除第一个） |
| 5 | 发件箱地址当收件人 | 发件箱仅用于 SMTP 发信，收件人配置到 `recipients.yaml`，区分 to/cc/bcc |

### 标准发送流程
```
1. 保存报告 → report/YYYY-MM-DD.md
2. md_to_html.py → /tmp/report.html（去 emoji + 格式美化）
3. send_email_multi.py --group all → 发送 HTML 邮件
```

### 核心文件路径
- 发送脚本：`/root/.openclaw/share/send-email/send_email_multi.py`
- HTML 模板：`/root/.openclaw/share/send-email/md_to_html.py`（v2 专业商务版）
- 收件人配置：`/root/.openclaw/share/send-email/recipients.yaml`
- Skill 配置经验：[[mail-skill-setup-guide]]

---

## 十、迭代记录

### v1 → v2（2026-05-21 18:34）
- 初始版本：深色 header + 基础表格
- 参考招商银行/新浪邮箱邮件后全面重构
- 改为渐变色 header + 圆角卡片 + 状态标签 + 信息卡片

### v2 → v3（2026-05-21 18:57）
- 修复表格在手机上挤在一起的问题
- 加 `table-wrapper` + `overflow-x: auto` + `table-layout: fixed`

### v3 → v4（2026-05-21 19:01）
- 修复文件头信息挤在一行的问题
- blockquote 内 `<strong>` 间插入 `<br>`

### v4 → v5（2026-05-21 19:18）
- 修复加粗标题直接跟 `- ` 列表被合并成段落的问题
- 预处理插入空行，正确渲染为 `<ul>/<ol>`
- 共修复 7 处列表格式问题

---

*最后更新：2026-05-21 22:12*
