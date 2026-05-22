# 邮件发送技能配置指南

> 最后更新：2026-05-22

## 一、文件结构

```
/root/.openclaw/share/send-email/
├── recipients.yaml          # 收件人配置（to/cc/bcc 分离）
├── send_email_multi.py      # 多收件人发送脚本
└── md_to_html.py            # Markdown → HTML 邮件转换
```

## 二、收件人配置 (recipients.yaml)

### 格式

```yaml
groups:
  all:
    description: "全部联系人"
    to:
      - panbin521@sina.com
    # cc:  # 不需要抄送时注释或删除此字段
    #   - example@xxx.com
    # bcc:  # 同上
```

### ⚠️ 抄送规则（核心！）

1. **有 cc 配置 → 抄送给指定人**
2. **无 cc 配置（字段不存在或为空列表）→ 不抄送**
3. **不要在 cc 下留空行**（如 `cc:\n  - `），YAML 会解析为 `[None]`，导致 `TypeError`
4. **永远不要用发件箱地址作为收件人**
5. 发件箱: `panbin5218@163.com`（仅用于 SMTP 发信）

### 当前配置

- 组 `all`：主送 `panbin521@sina.com`，无抄送

### 如何添加抄送

编辑 `recipients.yaml`，取消 cc 注释并填入地址：

```yaml
    cc:
      - 29464262@qq.com
```

或者通过命令行临时指定：

```bash
python3 send_email_multi.py --group all --cc 29464262@qq.com --subject "标题" --html-file report.html
```

## 三、发送命令

```bash
cd /root/.openclaw/share/send-email

# 从配置文件读取收件人组（自动区分 to/cc/bcc）
python3 send_email_multi.py --group all --subject "标题" --html-file /path/to/report.html

# 命令行指定收件人
python3 send_email_multi.py --to user@a.com --subject "标题" --html-file report.html

# 命令行指定主送 + 抄送
python3 send_email_multi.py --to user@a.com --cc cc_user@b.com --subject "标题" --html-file report.html

# 配置文件组 + 额外抄送
python3 send_email_multi.py --group all --extra-cc extra@c.com --subject "标题" --html-file report.html

# 列出所有收件人组
python3 send_email_multi.py --list-groups
```

## 四、md_to_html.py 使用

```bash
python3 md_to_html.py <input.md> <output.html>
```

### 预处理规则（Python markdown 库要求）

| 场景 | 规则 | 原因 |
|------|------|------|
| 加粗行 + 列表 | 之间必须有空行 | 否则列表被吸收为段落文本 |
| 嵌套列表 | 4空格缩进（相对列0） | Python markdown 要求4空格 |
| blockquote + 列表 | blockquote 内列表前加空行 | 否则列表不被识别 |
| 斜体行 | `*文字*` 的 `*` 后不能有空格 | 否则被识别为无序列表 |
| 列表项内加粗 | `- **xxx**` 必须保持空格 | 正则修复时不能吃掉 `- ` 和 `**` 之间的空格 |
| 临时文件 | 任务完成后立即删除中间迭代版本 | 防止 /tmp/ 堆积 |

## 五、常见问题

### Q1: cc 配置为空但发送时报 TypeError

**原因**: `recipients.yaml` 中 `cc:` 下有空行，YAML 解析为 `[None]`
**修复**: 删除空的 `cc:` 字段或注释掉；`send_email_multi.py` 的 `load_group()` 已增加 `if x` 过滤

### Q2: 邮件排版中列表不渲染为 `<ul>` / `<ol>`

**原因**: Python markdown 严格要求段落与列表间有空行
**修复**: 在 md_to_html.py 的 `preprocess_md()` 中，检测加粗行/普通段落后紧跟列表时插入空行

### Q3: 嵌套列表不生效

**原因**: 缩进不足4空格
**修复**: 子列表项使用4空格缩进（相对列0）

### Q4: `- **加粗**` 列表项渲染错误

**原因**: 基础格式修复的正则 `re.sub(r'([^\n]) +(\*\*), ...)` 会吃掉 `- **` 中的空格，导致 `-**` 无法被识别为列表项
**修复**: 正则排除 `-` 和 `*` 字符：`re.sub(r'([^\s*-]) +(\*\*), ...)`

## 六、修改记录

| 日期 | 修改内容 |
|------|---------|
| 2026-05-21 | 初始配置，收件人 panbin521@sina.com |
| 2026-05-22 | 移除抄送 29464262@qq.com；修复 cc 空值 TypeError；md_to_html.py 迭代至 v16 |
| 2026-05-22 | 修复 `- **` 空格被正则吃掉的问题；修复列表项内加粗排版；更新经验文档 |
