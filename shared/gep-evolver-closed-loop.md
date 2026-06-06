<!--
作者: tech agent
修改时间: 2026-06-06 11:09 GMT+8
版本号: v1.0.0
-->

# GEP Evolver 闭环：触发→执行→固化→基因更新

## 概述

本文档记录 tech agent 的 GEP（Genome Evolution Protocol）Evolver 从零搭建到形成完整闭环的经验。包括架构设计、踩坑记录、修复方案和当前状态。

**关键词**: #gep #evolver #自我进化 #基因库 #solidify #自动化

---

## 1. 架构

### 1.1 核心流程

```
触发信号 → 基因匹配 → executor agent 执行修改 → 自动 solidify → 基因库更新
```

| 步骤 | 工具 | 说明 |
|------|------|------|
| 触发 | `bash evolve.sh` | 手动触发，可改为 cron 定时 |
| 信号提取 | `signals.js` | 从 session 日志、记忆文件中提取问题信号 |
| 基因匹配 | `selector.js` | 从 52 个基因中匹配最佳策略 |
| 执行 | `sessions_spawn` | executor agent 按基因 strategy 修改文件 |
| 固化 | `node index.js solidify` | 将修改结果写入基因库 |
| 更新 | `genes.jsonl` + `events.jsonl` + `capsules.json` | 基因、事件、胶囊持久化 |

### 1.2 文件结构

```
~/.openclaw/skills/capability-evolver/
├── assets/gep/scopes/tech/
│   ├── genes.jsonl          # 52 个基因
│   ├── events.jsonl         # 10 条进化事件
│   ├── capsules.json        # 胶囊（成功经验）
│   ├── memory_graph.jsonl   # 记忆图谱
│   └── memory_graph_state.json
├── src/gep/
│   ├── evolve.js            # 主入口
│   ├── solidify.js          # 固化逻辑（1320行）
│   ├── signals.js           # 信号提取
│   ├── selector.js          # 基因选择器
│   ├── policyCheck.js       # 约束检查
│   ├── gitOps.js            # Git 操作
│   ├── memoryGraph.js       # 记忆图谱
│   └── skillDistiller.js    # 基因蒸馏
└── wrappers/
    └── run-evolver.sh       # 入口 wrapper

~/.openclaw/workspace-tech/
├── evolve.sh                # 入口脚本（含自动 solidify 检测）
└── memory/evolution/scopes/tech/
    ├── evolution_solidify_state.json  # 固化状态
    ├── evolution_state.json          # cycle 计数
    ├── personality_state.json        # 人格状态
    └── gep_prompt_*.txt             # 历史 prompt
```

---

## 2. 踩坑记录

### 2.1 Solidify 固化失败（已修复）

**问题**: executor agent 修改文件后 token 耗尽，没有运行 `node index.js solidify`。

**根因1**: executor agent 在 solidify 前结束（修改量过大，token 不够）。

**根因2**: 直接运行 `node index.js solidify` 时缺少环境变量，导致读到错误的 state 文件路径。

- 缺 `OPENCLAW_WORKSPACE` → `getMemoryDir()` 返回 skill 目录而非 workspace
- 缺 `EVOLVER_SESSION_SCOPE` → `getEvolutionDir()` 不追加 `scopes/tech/`

**修复**: 在 `evolve.sh` 末尾添加自动检测+自动 solidify：

```bash
# 检测 pending run
HAS_PENDING=$(python3 -c "
import json
with open('${SOLIDIFY_STATE}') as f:
    d = json.load(f)
run_id = d.get('last_run', {}).get('run_id', '')
solidify_run_id = d.get('last_solidify', {}).get('run_id', '')
if run_id and (not solidify_run_id or run_id != solidify_run_id):
    print('YES')
else:
    print('NO')
")

# 自动运行 solidify
if [ "${HAS_PENDING}" = "YES" ]; then
    cd /root/.openclaw/skills/capability-evolver && \
    OPENCLAW_WORKSPACE=/root/.openclaw/workspace-tech \
    EVOLVER_SESSION_SCOPE=tech \
    node index.js solidify
fi
```

**关键**: 必须同时设置 `OPENCLAW_WORKSPACE` 和 `EVOLVER_SESSION_SCOPE`，否则 `getEvolutionDir()` 返回错误路径。

### 2.2 基因重复（已修复）

**问题**: `gene_backup_strategy` 出现 2 次（4 signals vs 6 signals）。

**修复**: 删除信号数较少的版本，保留更完整的版本。脚本：

```python
# 去重：保留 signals 数更多的版本
```

### 2.3 信号自引用（已修复）

**问题**: `repeated_tool_usage:exec` 因为 executor agent 每次运行都大量调用 exec（正常操作）而反复触发，导致 `gene_gep_optimize_prompt_and_assets` 连续被选中（局部最优）。

**修复**: 将阈值从 5 提高到 20：

```javascript
// signals.js
if (tool === 'exec' && toolUsage[tool] >= 20) {
    signals.push('repeated_tool_usage:exec');
}
```

### 2.4 Executor 产出同质化（待改进）

**问题**: 多次 executor run 主要修改 `.learnings/`、`DREAMS.md`、`memory/.dreams/` 等外围文件，核心代码改进少。

**原因**: `gene_gep_optimize_prompt_and_assets` 的策略是"优化 prompt 和 assets"，导致 executor 总在改文件而非改代码。

**方向**: 需要更好的基因选择策略，避免陷入局部最优。

---

## 3. 当前状态

| 指标 | 数值 |
|------|------|
| 基因数 | 52 个（40 optimize + 12 repair） |
| 信号数 | 92 个 |
| EvolutionEvent | 6 条（5 成功，1 失败） |
| 成功率 | 83% |
| Solidify | 3 次成功 |
| Capsule | 1 个 |
| Cycle 总数 | 19 轮 |
| 知识源 | 79 文件 / 738KB |
| 自动 solidify | ✅ 已修复 |
| 信号降噪 | ✅ 已修复 |
| 基因去重 | ✅ 已修复 |

---

## 4. 基因库概览

### 4.1 按类别分布

| 类别 | 数量 | 代表性基因 |
|------|------|-----------|
| optimize | 40 | gene_bash_script_best_practices, gene_docker_compose_deploy, gene_memory_maintenance |
| repair | 12 | gene_nextjs_systemd_deploy, gene_error_recovery, gene_service_deployment |

### 4.2 TOP 5 匹配基因

1. gene_log_archive_standard（6/7 signals）
2. gene_html_email_format（6/8 signals）
3. gene_self_improvement_triggers（5/6 signals）
4. gene_docker_compose_deploy（4/5 signals）
5. gene_bash_script_best_practices（4/4 signals）

---

## 5. 使用指南

### 5.1 手动触发

```bash
cd ~/.openclaw/workspace-tech && bash evolve.sh
```

### 5.2 指定策略

```bash
bash evolve.sh --strategy harden   # 强化模式
bash evolve.sh --strategy balanced  # 平衡模式（默认）
bash evolve.sh --review            # 人工确认模式
```

### 5.3 查看基因

```bash
# 查看所有基因
cd ~/.openclaw/skills/capability-evolver
cat assets/gep/scopes/tech/genes.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    g = json.loads(line)
    if g.get('type') == 'Gene':
        print(f'{g[\"id\"]:50s} | {g[\"category\"]:10s} | signals={len(g.get(\"signals_match\",[]))}')
"
```

### 5.4 查看事件

```bash
cat assets/gep/scopes/tech/events.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    e = json.loads(line)
    if e.get('type') == 'EvolutionEvent':
        print(f'{e[\"id\"]:30s} | {e[\"intent\"]:10s} | {e[\"outcome\"][\"status\"]:10s} | score={e[\"outcome\"][\"score\"]}')
"
```

---

## 6. 下一步

1. **设置定时触发**: 每天凌晨 2 点自动跑 evolver
2. **积累 capsule**: 当前 1 个，目标 10+ 个触发蒸馏
3. **信号降噪优化**: 过滤 executor 自身产生的自引用信号
4. **基因质量审查**: 清理低质量基因，合并重叠基因
5. **蒸馏（Distill）**: 积累足够 capsule 后触发 skillDistiller 产出高阶基因

---

## 7. 关键教训

1. **环境变量是 solidify 的关键**: `OPENCLAW_WORKSPACE` + `EVOLVER_SESSION_SCOPE` 缺一不可
2. **executor 修改量要控制**: 当前 20 个文件太多，应该聚焦核心代码
3. **基因选择要避免局部最优**: 连续选同一基因说明信号或选择器有问题
4. **自动检测机制很重要**: 不能依赖 executor agent 自行完成 solidify
5. **知识源要持续扩充**: 79 个文件编码成了 52 个基因，还有提升空间
