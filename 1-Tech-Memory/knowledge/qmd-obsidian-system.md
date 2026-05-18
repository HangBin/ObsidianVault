---
author: tech agent
created: 2026-04-09 16:10:33
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
source: tech agent memory/experience-qmd-obsidian-system.md
tags: [tech-agent, experience, knowledge, qmd, obsidian, 记忆存储系统]
---

# QMD + Obsidian 记忆存储系统

<!--
作者: tech
修改时间: 2026-04-19 15:54 GMT+8
版本号: v1.0.0
-->

## 概述

QMD + Obsidian 构建的本地知识库系统，为 AI Agent 提供语义搜索和向量检索能力。

## 核心架构

```
Obsidian (本地知识库) ←→ QMD (向量检索) ←→ AI Agent
     ↓                        ↓
  /home/Obsidian_Vault    语义搜索
  可视化管理              快速加载
```

## QMD Collections 配置

### 设计原则
- 按工作区分集合：main/tech/proj/media/final
- 核心配置单独集合：MEMORY/SOUL/IDENTITY 等
- memory 每日对话独立管理
- experience*.md 经验汇总独立
- .learnings 单独管理（仅 tech 工作区）

### 集合配置命令

```bash
#!/bin/bash
#==========================================
# QMD 集合配置命令
#==========================================

# ---------- 1. 清空 ----------
rm -f /root/.cache/qmd/index.sqlite
qmd collection remove memory 2>/dev/null || true

# ---------- 2. main 核心配置 ----------
qmd collection add main-memory-root --path /root/.openclaw/workspace --pattern "MEMORY.md"
qmd collection add main-soul --path /root/.openclaw/workspace --pattern "SOUL.md"
qmd collection add main-identity --path /root/.openclaw/workspace --pattern "IDENTITY.md"
qmd collection add main-agents --path /root/.openclaw/workspace --pattern "AGENTS.md"
qmd collection add main-tools --path /root/.openclaw/workspace --pattern "TOOLS.md"
qmd collection add main-user --path /root/.openclaw/workspace --pattern "USER.md"

# ---------- 3. main memory 每日对话 ----------
qmd collection add main-memory --path /root/.openclaw/workspace/memory --pattern "*.md"

# ---------- 4. main 经验文档汇总 ----------
qmd collection add main-experience --path /root/.openclaw/workspace/memory --pattern "experience*.md"

# ---------- 5. tech 核心配置 ----------
qmd collection add tech-memory-root --path /root/.openclaw/workspace-tech --pattern "MEMORY.md"
qmd collection add tech-soul --path /root/.openclaw/workspace-tech --pattern "SOUL.md"
qmd collection add tech-identity --path /root/.openclaw/workspace-tech --pattern "IDENTITY.md"
qmd collection add tech-agents --path /root/.openclaw/workspace-tech --pattern "AGENTS.md"
qmd collection add tech-tools --path /root/.openclaw/workspace-tech --pattern "TOOLS.md"

# ---------- 6. tech memory + learnings + experience ----------
qmd collection add tech-memory --path /root/.openclaw/workspace-tech/memory --pattern "*.md"
qmd collection add tech-learnings --path /root/.openclaw/workspace-tech/.learnings --pattern "*.md"
qmd collection add tech-experience --path /root/.openclaw/workspace-tech/memory --pattern "experience*.md"

# ---------- 7. proj ----------
qmd collection add proj-memory-root --path /root/.openclaw/workspace-proj --pattern "MEMORY.md"
qmd collection add proj-soul-identity --path /root/.openclaw/workspace-proj --pattern "SOUL.md,IDENTITY.md"
qmd collection add proj-agents-tools --path /root/.openclaw/workspace-proj --pattern "AGENTS.md,TOOLS.md"
qmd collection add proj-memory --path /root/.openclaw/workspace-proj/memory --pattern "*.md"
qmd collection add proj-experience --path /root/.openclaw/workspace-proj/memory --pattern "experience*.md"

# ---------- 8. media ----------
qmd collection add media-memory-root --path /root/.openclaw/workspace-media --pattern "MEMORY.md"
qmd collection add media-soul-identity --path /root/.openclaw/workspace-media --pattern "SOUL.md,IDENTITY.md"
qmd collection add media-agents-tools --path /root/.openclaw/workspace-media --pattern "AGENTS.md,TOOLS.md"
qmd collection add media-memory --path /root/.openclaw/workspace-media/memory --pattern "*.md"
qmd collection add media-experience --path /root/.openclaw/workspace-media/memory --pattern "experience*.md"

# ---------- 9. final ----------
qmd collection add final-memory-root --path /root/.openclaw/workspace-final --pattern "MEMORY.md"
qmd collection add final-soul-identity --path /root/.openclaw/workspace-final --pattern "SOUL.md,IDENTITY.md"
qmd collection add final-agents-tools --path /root/.openclaw/workspace-final --pattern "AGENTS.md,TOOLS.md"
qmd collection add final-memory --path /root/.openclaw/workspace-final/memory --pattern "*.md"
qmd collection add final-experience --path /root/.openclaw/workspace-final/memory --pattern "experience*.md"
```

## 模型配置

### Embedding 模型
- 模型: `hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf`
- 缓存路径: `~/.cache/qmd/models/`
- 状态: ✅ 已缓存

### Reranker 模型
- 模型: `hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF`
- 缓存路径: `~/.cache/qmd/models/`
- 状态: ✅ 已缓存

## 常见问题

### Q1: embed 卡在 "Gathering information"
**原因**: 首次加载模型时触发下载
**解决**: 模型已缓存，后续无需重新下载

### Q2: CPU 模式下 embed 极慢
**原因**: 无 GPU 加速
**解决**: 单文件 embed 需要 30+ 秒，批量重建建议在 GPU 环境

## 每日对话归档

### 2026-04-19 对话要点

1. **qmd embed 问题解决**
   - 昨天卡在 "Gathering information" 的问题已定位
   - 根因：首次模型加载触发下载，现已缓存完成
   - CPU 模式下 embed 较慢（30+ 秒/文件），但功能正常

2. **QMD 集合重构**
   - 按工作区（main/tech/proj/media/final）分离集合
   - 核心配置、memory、experience 分开管理
   - 生成了 qmd_commands.sh 待用户执行

3. **经验教训**
   - QMD 不应该把所有文件塞到一个 memory 集合
   - 按工作区 + 文件类型分离集合是最佳实践
   - 模型缓存后无需重新下载

## 相关文件

- `/root/.openclaw/workspace-tech/qmd_commands.sh` - 集合配置脚本
- `/root/.cache/qmd/index.sqlite` - QMD 索引文件
- `/root/.cache/qmd/models/` - 模型缓存目录
- **2026-04-29** - ✅ 兼容Obsidian等笔记工具
- **2026-04-29** - ✅ 目标文件：`/home/obsidian_vault/1-Tech-Memory/daily/2026-04-29.md`
- **2026-04-29** - ✅ 格式：Obsidian兼容Markdown（含frontmatter）
- **2026-04-29** 2.才能保证把每日的会话写入每日记忆文件，总结经验教训到专项经验文件(如针对如qmd和obsidian的专项经验写入文档qmd-obsidian-system.md)，而不是累加到experience.md文件里
- **2026-04-29** **规则1：QMD相关经验**
- **2026-04-29**   ## [YYYY-MM-DD] QMD经验条目
- **2026-04-29** **规则2：Obsidian相关经验**
- **2026-04-29** **QMD-Obsidian经验写入模板**：
- **2026-04-29** 4. 更新经验索引
- **2026-05-07** - **结果**: ✅ 今日记忆已更新，准备同步到 Obsidian
- **2026-05-07** - **结果**: ✅ 今日记忆已更新，准备同步到 Obsidian
- **2026-05-18** **结果**: ✅ 确认 AGENTS.md 中 daily-index.md 路径只指向 Obsidian vault
- **2026-05-18** - ✅ 创建 archive/2026-04.md 月度索引（10423行，540K）
- **2026-05-18** - ✅ 创建 archive/2026-04.md 月度索引（10423行，540K）
