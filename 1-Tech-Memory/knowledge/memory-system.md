---
author: tech agent
created: 2026-04-14 09:34:12
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
source: tech agent memory/experience-memory-system.md
tags: [tech-agent, experience, knowledge, memory]
---


# 记忆归档流程

## 记忆归档流程（2026-04-04 固化）

### 核心规则
- ✅ **多文件合并**: 同日期碎片化记忆定期合并为单个文件（如 2026-04-02.md 合并 6 个碎片）
- ✅ **归档策略**: 原始会话文件移动到 `archived_YYYYMMDD_HHMMSS/`，保留可追溯性
- ✅ **保留原则**: 只保留正式 daily logs，会话元数据和测试输出可归档
- ✅ **同步检查**: 合并后验证 `.learnings/` 完整性（防止学习内容丢失）
- ✅ **提取报告**: 生成 `LEARNINGS_EXTRACTION_REPORT_*.md` 记录提取统计和待审核项

---

## 📚 记忆体系

### 文件结构
- **MEMORY.md**: 长期宪法，主会话加载
- **memory/YYYY-MM-DD.md**: 每日原始日志，每次会话从零开始
- **专项经验**: `memory/experience-browser-shared.md`（Chromium CDP 自动化方案）
- **定期回顾**: 每次会话开始读取前一日日志，提炼信息沉淀到 MEMORY.md

### 归纳机制
- **触发条件**: 每 10 分钟 或 每 10 条记录
- **执行流程**:
  1. 读取当日 `memory/YYYY-MM-DD.md` 最近条目
  2. 提炼技术决策、架构变更、性能优化、问题根因
  3. 同步到 MEMORY.md 对应章节
  4. 归纳后 daily log 保持原样（原始记录不可篡改）

---

## 🧠 Self-Improvement 技能

### 目录结构
- **目录**: `~/.openclaw/workspace-tech/.learnings/`
- **内容**:
  - `LEARNINGS.md` - 经验与最佳实践（42+ entries）
  - `ERRORS.md` - 错误与失败（13+ entries）
  - `FEATURE_REQUESTS.md` - 功能请求（2+ entries）

### 触发时机
6种场景自动捕获：
1. 用户纠正你 → `.learnings/LEARNINGS.md`
2. 命令/操作失败 → `.learnings/ERRORS.md`
3. 用户想要缺失能力 → `.learnings/FEATURE_REQUESTS.md`
4. 你发现知识错误 → `.learnings/LEARNINGS.md`
5. 你发现更好方案 → `.learnings/LEARNINGS.md`
6. 工具异常 → `.learnings/ERRORS.md`

### 使用方式
- 工作前 review pending high-priority items
- recurring patterns 升迁到 `SOUL.md` / `AGENTS.md` / `TOOLS.md`
- 具体格式规则见技能文档 `~/.openclaw/skills/self-improving-agent/SKILL.md`

---

## 📂 相关文件
- 主脚本: `share/daily-organize-summarize/daily-memory-management.sh`
- 学习工作流: `/root/.openclaw/share/learning-workflow/`
- 提取报告: `.learnings/LEARNINGS_EXTRACTION_REPORT_*.md`

---

## 🔗 相关条目

### 强关联
- [[qmd-obsidian-system]] - QMD是记忆系统的搜索层
- [[2026-04-04]] - 记忆系统整理与服务迁移
- [[2026-04-05]] - 每日记忆管理系统上线
- [[2026-04-28]] - Obsidian归档方案与迁移
- [[2026-04-29]] - 记忆系统迁移与提示词设计

### 中关联
- [[bash-deploy]] - 记忆归档脚本使用Bash开发
- [[collaboration-patterns]] - 跨agent记忆同步
- [[backup-system]] - 记忆文件备份策略

### 弱关联
- [[2026-03-23]] - 记忆系统重构
- [[2026-03-27]] - 即时归档违规纠正

---
*图谱关联最后更新: 2026-05-07*
