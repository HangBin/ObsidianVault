# HTML 邮件美化经验总结

> 创建时间：2026-05-22
> 来源：md_to_html.py 脚本迭代经验（v1-v21）

---

## 一、核心工具

**脚本位置**：`/root/.openclaw/share/send-email/md_to_html.py`

**用法**：
```bash
python3 md_to_html.py input.md output.html "邮件标题" "报告类型"
```

**发送邮件**：
```bash
cd /root/.openclaw/share/send-email
python3 send_email_multi.py --group all --subject "标题" --html-file output.html
```

---

## 二、Python markdown 库的关键规则

### 规则1：段落后的列表必须有空行

```markdown
# ❌ 错误：列表被当作段落内联文本
**加粗标题**：
- 列表项1
- 列表项2

# ✅ 正确：有空行分隔
**加粗标题**：

- 列表项1
- 列表项2
```

**HTML结果**：
- 错误：`<p><strong>加粗标题</strong>：\n- 列表项1\n- 列表项2</p>`
- 正确：`<p><strong>加粗标题</strong>：</p>\n<ul><li>列表项1</li><li>列表项2</li></ul>`

### 规则2：嵌套列表需要4空格缩进

```markdown
# ❌ 错误：2空格缩进，子列表被识别为同级
- 父项：
  - 子项1
  - 子项2

# ✅ 正确：4空格缩进
- 父项：
    - 子项1
    - 子项2
```

**注意**：缩进是相对于**列表标记**（`- ` 或 `1. `）的起始位置，不是相对于行首。

### 规则3：加粗行后的列表需要特殊处理

当加粗行以冒号结尾时，即使加粗标记不在行首，也需要在加粗行后插入空行：

```markdown
# ❌ 错误
**昨日（5月21日）主力资金流向**（来源：东方财富）：
- 全天主力净流出：**1251.41亿元**

# ✅ 正确
**昨日（5月21日）主力资金流向**（来源：东方财富）：

- 全天主力净流出：**1251.41亿元**
```

**检测方法**：行中包含 `**xxx**` 且以 `：` 或 `:` 结尾。

### 规则4：blockquote 内不支持列表

Python markdown **不支持** blockquote 内的有序/无序列表：

```markdown
# ❌ 列表被渲染为段落文本
> 操作原则：
> 1. 上午冲高不追涨
> 2. 午后若开始回落→提前设好止损

# ✅ 后处理方案：在HTML中转换
# 将 <p>操作原则：\n1. xxx\n2. xxx</p> 转换为
# <p>操作原则：</p><ol><li>xxx</li><li>xxx</li></ol>
```

**解决方案**：后处理HTML，用正则匹配 `<p>...1. xxx\n2. xxx</p>` 模式并转换为 `<ol><li>`。

### 规则5：斜体行的 `*` 不能跟空格

```markdown
# ❌ 错误：* 后跟空格，被识别为无序列表项
* 本报告基于盘前数据，仅供参考 *

# ✅ 正确：使用下划线斜体
_本报告基于盘前数据，仅供参考_

# ✅ 或者：* 后直接跟文字（无空格）
*本报告基于盘前数据，仅供参考*
```

### 规则6：连续斜体行需要空行分隔

```markdown
# ❌ 错误：被合并到一个 <p> 里
*第一行*
*第二行*
*第三行*

# ✅ 正确：每行之间有空行
*第一行*

*第二行*

*第三行*
```

---

## 三、预处理策略

### 预处理流程

```
原始MD → 删除emoji → 修复基础格式 → 逐行处理（列表缩进/空行插入） → 全局修复 → Python markdown → 后处理HTML
```

### 关键预处理操作

1. **删除emoji**：emoji会破坏加粗标记（如 `1. **` 代替 `1. **`)
2. **修复加粗**：`re.sub(r'(\*\*) +([^\n])', r'\1\2', md)` 去除 `**` 后的空格
3. **修复有序列表**：`re.sub(r'^(\d+)\.\*\*', r'\1. **', md)` 修复 `1.**` → `1. **`
4. **列表缩进**：逐行扫描，将子列表项缩进到正确位置
5. **空行插入**：在加粗行/冒号段落后的列表前插入空行

### 后处理操作

1. **表格wrapper**：`<table>` → `<div class="table-wrapper"><table>`
2. **列表项清理**：移除 `<li>` 内的 `<p>` 标签
3. **blockquote修复**：确保 `<strong>` 前有 `<br>`
4. **blockquote内列表**：将 `<p>...1. xxx\n2. xxx</p>` 转换为 `<ol><li>`
5. **临时文件清理**：任务完成后删除 `/tmp/` 下的中间迭代文件

---

## 四、CSS 邮件样式要点

### 兼容性

- **不使用** CSS Grid/Flexbox（邮件客户端支持差）
- **使用** `table-layout: fixed` + `word-break: break-all` 防止表格溢出
- **使用** `max-width: 780px` + `margin: 0 auto` 居中
- **媒体查询**：`@media (max-width: 600px)` 适配移动端

### 关键样式

```css
/* 表格防溢出 */
table {
  table-layout: fixed;
  word-break: break-all;
  overflow-wrap: break-word;
}

/* 列表嵌套 */
ul ul { list-style-type: circle; }
ol ol { list-style-type: lower-alpha; }

/* 引用块 */
blockquote {
  border-left: 4px solid #2d6a9f;
  background: #f0f7fb;
}
```

---

## 五、常见排版问题速查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 列表被渲染为 `<p>` | 段落和列表之间没有空行 | 预处理插入空行 |
| 嵌套列表变成同级 | 子列表缩进不足4空格 | 预处理缩进4空格 |
| 加粗行后列表失效 | `**` 和 `：` 之间有其他字符 | 用 `re.search` 代替 `re.match` |
| blockquote内列表失效 | Python markdown不支持 | 后处理HTML转换 |
| 斜体行被识别为列表 | `*` 后跟空格 | 改用 `_` 斜体或去掉空格 |
| 连续斜体行被合并 | 行间没有空行 | 预处理插入空行 |
| 有序列表项格式错误 | emoji删除后 `1.**` 无空格 | 预处理修复 `1.**` → `1. **` |
| 列表项加粗格式错误 | `-**xxx**` 无空格 | 预处理修复 `-**` → `- **` |

---

## 六、调试技巧

1. **保存预处理MD**：`debug_path = output_path.replace('.html', '-debug.md')`
2. **分段测试**：提取问题section单独测试Python markdown渲染
3. **统计标签**：检查 `<ol>`、`<ul>`、`<table>`、`<pre>` 数量是否符合预期
4. **检查 `<pre>` 标签**：出现 `<pre>` 说明有过度缩进（≥4空格被当代码块）

---

## 七、文件清单

| 文件 | 用途 |
|------|------|
| `/root/.openclaw/share/send-email/md_to_html.py` | MD→HTML转换脚本 |
| `/root/.openclaw/share/send-email/send_email_multi.py` | 邮件发送脚本 |
| `/root/.openclaw/share/send-email/recipients.yaml` | 收件人配置 |
| `/home/obsidian_vault/shared/html-email-format.md` | 本文档 |
