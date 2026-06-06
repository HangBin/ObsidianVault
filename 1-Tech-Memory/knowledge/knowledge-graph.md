<!--
作者: tech agent
修改时间: 2026-05-08 18:00 GMT+8
版本号: v1.0.0
-->

# 图谱关联经验总结

> 本文档记录 Obsidian 知识库图谱关联的设计经验和踩坑教训

---

## 一、核心经验

### 1.1 不要在简单日志文件上强行添加关联章节

**教训来源**: 2026-05-07/08 为所有 daily/ 文件添加"相关条目"章节

- 简单日志文件（如只有几条心跳记录）不需要强制添加关联章节
- Obsidian 自带的反向链接和标签面板已经足够
- **正确做法**: 只有有实质内容的文件才建立图谱关联

### 1.2 图谱关联的正确方式：frontmatter tags + wikilink

**最佳实践**:
1. 在 frontmatter 的 `tags` 字段添加语义化标签
2. 在索引文件中用 `[[wikilink]]` 建立文件间关联
3. 让 Obsidian 的标签面板和 Graph View 自动形成图谱

**示例**:
```markdown
tags:
- main-agent
- daily-log
- qmd
- memory-system
```

### 1.3 索引文件结构（按月分组）

**推荐结构**:
1. 每日记忆文件（daily/）— 按月份分组表格
2. 专项经验（knowledge/）— 文件+主题表格
3. 时间线 — 按月份分组的 wikilink 链
4. 长期记忆 — MEMORY.md
5. 标签索引 — 按 frontmatter tags 分类

---

## 二、踩坑教训

### 2.1 frontmatter tags 格式必须是 YAML 列表

**错误格式**:
```yaml
tags: [main-agent, daily-log]
```

**正确格式**:
```yaml
tags:
- main-agent
- daily-log
```

> ⚠️ 单行数组格式 `[a, b, c]` 会导致 Obsidian 无法正确解析标签

### 2.2 git auto-sync 脚本要处理 pull 失败

**教训来源**: 2026-05-08 auto-sync.sh 覆盖远程更新

- `git pull --rebase` 可能因本地未暂存变更而失败
- 脚本必须检查 pull 的退出码，失败时 abort
- **正确逻辑**: stash → pull → stash pop → commit push

### 2.3 merge commit 可能丢失文件

**教训来源**: 2026-05-08 TortoiseGit merge 导致 portfolio-analysis 文件丢失

- TortoiseGit 的 merge 操作可能产生冲突解决，意外删除文件
- 重要文件在 merge 后要检查是否还在
- 服务器端和 GitHub 端要定期对比一致性

---

## 三、索引文件模板

### 3.1 Agent 知识库索引（main/proj/media/tech/final）

```markdown
# 🧠 [Agent] 图谱入口

## 一、每日记忆文件（daily/）
### YYYY-MM
| 日期 | 主题 |
|------|------|
| [[YYYY-MM-DD]] | ... |

## 二、专项经验（knowledge/）
| 文件 | 主题 |
|------|------|
| [[xxx]] | ... |

## 三、时间线
### N月
[[...]] → [[...]] → [[...]]

## 四、长期记忆
- [[MEMORY]]

## 五、标签索引
- **#tag**: [[...]] · [[...]]
```

### 3.2 个人知识库索引（Personal）

```markdown
# 🧠 Personal 图谱入口

## 目录名
| 文件 | 主题 |
|------|------|
| [[目录/文件名]] | ... |
```

---

## 四、操作规范

### 4.1 创建图谱索引
1. 扫描目标目录下所有 .md 文件
2. 读取每个文件的 frontmatter tags 和第一个 # 标题
3. 按目录/月份分组
4. 用 `[[wikilink]]` 关联所有文件
5. 只创建索引文件，**不修改其他文件**

### 4.2 修复 tags 格式
1. 检查所有文件的 frontmatter tags
2. 单行数组格式 `[a, b]` → YAML 列表格式 `- a\n- b`
3. 缺少 `- ` 前缀的标签行补上

### 4.3 维护原则
- 新增文件时同步更新索引文件
- 定期检查 tags 格式
- 索引文件与实际内容保持一致

---

*最后更新: 2026-05-08 18:00 GMT+8*
