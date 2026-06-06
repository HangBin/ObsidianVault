<!--
author: tech agent
修改时间: 2026-06-06 12:06 GMT+8
版本号: v2.0.0
-->


# 记忆归档流程

## 记忆归档流程（2026-04-04 固化）

### 核心规则
- ✅ **多文件合并**: 同日期碎片化记忆定期合并为单个文件（如 2026-04-02.md 合并 6 个碎片）
- ✅ **归档策略**: 原始会话文件移动到 `archived_YYYYMMDD_HHMMSS/`，保留可追溯性
- ✅ **保留原则**: 只保留正式 daily logs，会话元数据和测试输出可归档
- ✅ **同步检查**: 合并后验证 `.learnings/` 完整性（防止学习内容丢失）
- ✅ **提取报告**: 生成 `LEARNINGS_EXTRACTION_REPORT_*.md` 记录提取统计和待审核项

---

## 碎片文件管理（2026-04-15 固化）

### 问题
- archive 目录下的经验碎片文件未合并
- 未建立有效的碎片清理机制

### 解决方案
1. **经验碎片文件处理**
   - 识别并合并重复经验碎片文件
   - 创建 historical-experiences/ 目录存储历史碎片
   - 更新主 experience.md 文件
2. **脚本功能增强**
   - 新增 `cleanup_experience_fragments()` 函数
   - 自动检测和清理重复的经验碎片文件

### 核心经验
- 文件去重机制必须建立碎片文件自动清理机制
- 重要经验必须同步到共享文档

---

## 知识调用流程（2026-04-28 固化）

### 查询优先级
```
用户问题
  │
  ├── 1. 1-Tech-Memory/knowledge/  ← agent 自有（最高）
  ├── 2. Personal/                  ← 用户知识（其次）
  └── 3. 网络搜索                   ← 外部（最后）
```

### 按需加载原则
- ❌ 不推荐：会话启动扫描所有 knowledge/ 文件（消耗 token）
- ✅ 推荐：QMD 索引 + 按需查询

### QMD 管理
- 用 `qmd collection add` 管理索引
- 不需要修改 openclaw.json

### Obsidian 目录权限
| 目录 | 用途 | 权限 |
|------|------|------|
| 1-Tech-Memory/ | tech agent 专属 | 读写 |
| shared/ | 所有 agent 共享 | 读写 |
| Personal/ | 用户个人知识库 | 只读（chmod 755） |

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
