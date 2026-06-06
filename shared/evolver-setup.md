<!--
作者: tech agent
修改时间: 2026-06-06 12:10 GMT+8
版本号: v1.0.0
-->

# Evolver 安装配置经验

## 概述

本文档记录 capability-evolver（GEP）的安装、配置和初始化经验。

**关键词**: #evolver #gep #安装 #配置 #自我进化

---

## 安装

### 来源
- ClawHub: `clawhub install capability-evolver`
- 安装位置: `~/.openclaw/skills/capability-evolver/`

### 目录结构
```
~/.openclaw/skills/capability-evolver/
├── assets/gep/scopes/     # 基因库（按 scope 隔离）
│   ├── tech/genes.jsonl   # tech agent 的基因
│   ├── tech/events.jsonl  # 进化事件
│   └── tech/capsules.json # 经验胶囊
├── src/gep/               # 核心源码
│   ├── evolve.js          # 主入口
│   ├── solidify.js        # 固化逻辑
│   ├── signals.js         # 信号提取
│   ├── selector.js        # 基因选择器
│   └── policyCheck.js     # 约束检查
└── wrappers/
    └── run-evolver.sh     # 入口 wrapper
```

---

## 配置

### 环境变量
| 变量 | 说明 | 示例 |
|------|------|------|
| OPENCLAW_WORKSPACE | 工作区路径 | /root/.openclaw/workspace-tech |
| EVOLVER_SESSION_SCOPE | agent 作用域 | tech |
| EVOLVE_STRATEGY | 进化策略 | balanced/harden/review |

### 入口脚本
```bash
# 手动触发
cd ~/.openclaw/workspace-tech && bash evolve.sh

# 指定策略
bash evolve.sh --strategy harden

# 指定 scope
EVOLVER_SESSION_SCOPE=tech bash evolve.sh
```

---

## 基因库初始化

### 2026-06-04 深度扫描
- 从 Obsidian 知识库扫描 79 个文件（738KB）
- 编码 45 个新基因（从 8 扩充到 53，去重后 52）
- 覆盖领域：Docker、Bash、Next.js、systemd、Obsidian、Git、浏览器、安全等

### 基因分类
| 类别 | 数量 | 作用 |
|------|------|------|
| optimize | 40 | 改进现有系统、修复工作流 |
| repair | 12 | 修复部署、构建、配置错误 |

---

## 关键踩坑

### 1. Solidify 环境变量缺失
- **现象**：`node index.js solidify` 读取到错误的 state 文件
- **原因**：缺少 OPENCLAW_WORKSPACE 和 EVOLVER_SESSION_SCOPE
- **修复**：必须同时设置两个环境变量

### 2. Executor 不执行 solidify
- **现象**：executor agent 修改文件后结束，不运行 solidify
- **原因**：修改量过大，token 在 solidify 前耗尽
- **修复**：在 evolve.sh 中添加自动检测+自动 solidify 逻辑

### 3. 信号自引用
- **现象**：repeated_tool_usage:exec 反复触发同一基因
- **原因**：executor 正常调用 exec 10+ 次，超过阈值 5
- **修复**：将阈值从 5 提高到 20

---

## 进化历程

| 日期 | 里程碑 | 基因数 |
|------|--------|--------|
| 2026-04-04 | 首次安装 | 8 |
| 2026-04-24 | 配置完成 | 8 |
| 2026-06-04 | 深度扫描+基因扩充 | 53 |
| 2026-06-06 | 去重清理 | 52 |
| 2026-06-06 | 闭环修复+solidify 自动化 | 52 |

---

## 更新记录
- 2026-06-06: 初始版本，从 MEMORY.md Evolver 相关章节提炼
