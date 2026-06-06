<!--
作者: tech agent
修改时间: 2026-06-06 12:10 GMT+8
版本号: v1.0.0
-->

# 技能开发规范

## 概述

本文档定义 tech agent 的技能（Skill）开发标准，确保技能质量和可维护性。

**关键词**: #skill #技能开发 #规范 #最佳实践

---

## 技能结构标准

每个技能必须包含以下文件：

```
skills/<name>/
├── SKILL.md          # 必需：YAML frontmatter + 使用说明
├── index.js          # 必需：主入口，working exports
├── scripts/          # 可选：可执行脚本
└── references/       # 可选：详细文档（按需加载）
```

### SKILL.md 规范

```markdown
---
name: skill-name
description: 一句话描述技能做什么、什么时候使用。至少20字符。
---

# 技能名称

## 使用方法
（具体指令和步骤）
```

**规则**：
- description 必须清晰、完整，是触发机制
- 正文控制在 500 行以内
- 详细内容放 references/，不在 SKILL.md 里堆砌

### 命名规范

- ✅ 描述性 kebab-case：`log-rotation`、`retry-handler`、`cache-manager`
- ❌ 禁止：时间戳、随机数、工具名、UUID、无意义名称
- 2-6 个描述性单词，连字符分隔

### 导出验证

```bash
node -e "const s = require('./skills/<name>'); console.log(Object.keys(s))"
```

---

## 开发流程

### 1. 问题识别
- 3+ 次手动操作 = 需要工具化
- 重复性任务 = 技能候选

### 2. 设计原则
- **原子性**：一个技能做一件事
- **可复用**：参数化，不硬编码
- **可测试**：每个功能都有验证命令
- **幂等**：多次执行结果一致

### 3. 实现标准
- `set -e` 快速失败
- 路径动态检测（`SCRIPT_DIR`）
- `--dry-run` 和 `--verbose` 支持
- 错误输出到 stderr

### 4. 测试验证
```bash
# 测试导出
node -e "require('./skills/<name>').main ? require('./skills/<name>').main() : console.log('ok')"

# 测试脚本
bash scripts/test.sh
```

### 5. 文档同步
- 技能文档放入 `skills/<name>/references/`
- 经验提炼到专项经验文档
- 更新 MEMORY.md 专项经验表格

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 文件名用 experience- | 不符合规范 | 用 kebab-case |
| description 太模糊 | 无法触发 | 写清楚 WHAT + WHEN |
| 不测试就提交 | 技能不可用 | 先验证 exports |
| 硬编码路径 | 跨环境失败 | 用 SCRIPT_DIR 动态检测 |
| 缺少 set -e | 错误被吞 | 所有脚本加 set -e |

---

## 已有技能清单

| 技能 | 用途 | 位置 |
|------|------|------|
| capability-evolver | 自我进化 | ~/.openclaw/skills/ |
| baidu-web-search | 中文搜索 | ~/.openclaw/skills/ |
| multi-search-engine | 多引擎搜索 | ~/.openclaw/skills/ |
| tavily-search | 国际搜索 | ~/.openclaw/skills/ |
| self-improvement | 学习改进 | ~/.openclaw/skills/ |
| browser-automation | 浏览器自动化 | ~/.openclaw/plugin-skills/ |
| diagram-maker | 图表制作 | /usr/lib/node_modules/openclaw/skills/ |

---

## 更新记录
- 2026-06-06: 初始版本，从 MEMORY.md 4-23 章节提炼
