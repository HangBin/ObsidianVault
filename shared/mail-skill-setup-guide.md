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
    # cc: 为空时直接删除该字段，不要留空行
    # bcc: 同上
```

### ⚠️ 关键规则

1. **cc/bcc 为空时，直接删除该字段**，不要留 `cc:\n  - ` 这样的空行
   - YAML 会把空行解析为 `[None]`，导致 `TypeError: sequence item 0: expected str instance`
2. **永远不要用发件箱地址作为收件人**
3. 发件箱: `panbin5218@163.com`（仅用于 SMTP 发信）

### 当前配置

- 组 `all`：主送 `panbin521@sina.com`，无抄送

## 三、发送命令

```bash
cd /root/.openclaw/share/send-email

# 从配置文件读取收件人组
python3 send_email_multi.py --group all --subject "标题" --html-file /path/to/report.html

# 命令行指定收件人
python3 send_email_multi.py --to user@a.com --subject "标题" --html-file report.html

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
| 临时文件 | 任务完成后立即删除中间迭代版本 | 防止 /tmp/ 堆积 |

## 五、常见问题

### Q1: cc 配置为空但发送时报 TypeError

**原因**: `recipients.yaml` 中 `cc:` 下有空行，YAML 解析为 `[None]`
**修复**: 删除空的 `cc:` 字段；同时在 `send_email_multi.py` 的 `load_group()` 中增加 `if x` 过滤

### Q2: 邮件排版中列表不渲染为 `<ul>` / `<ol>`

**原因**: Python markdown 严格要求段落与列表间有空行
**修复**: 在 md_to_html.py 的 `preprocess_md()` 中，检测加粗行/普通段落后紧跟列表时插入空行

### Q3: 嵌套列表不生效

**原因**: 缩进不足4空格
**修复**: 子列表项使用4空格缩进（相对列0）

## 六、修改记录

| 日期 | 修改内容 |
|------|---------|
| 2026-05-21 | 初始配置，收件人 panbin521@sina.com |
| 2026-05-22 | 移除抄送 29464262@qq.com；修复 cc 空值 TypeError；md_to_html.py 迭代至 final 版 |
