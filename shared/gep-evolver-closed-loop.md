<!--
作者: tech agent (v1.0) + final agent (v1.1 补充)
修改时间: 2026-06-06 14:00 GMT+8
版本号: v1.1.0
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

---

## 8. Final Agent 基因注入经验（v1.1, 2026-06-06）

### 8.1 知识源扫描规范（强制）

> **⚠️ 必须进入子文件夹深度扫描，禁止只看目录结构就下结论！**

Final agent 的知识源分布在 6 大类 30+ 子目录中，总计 291 个文件。扫描时必须：

#### 8.1.1 扫描清单（逐项执行，不可跳过）

| 优先级 | 目录 | 文件数 | 扫描方式 |
|--------|------|--------|---------|
| **P0** | `knowledge/` | 4 | 全部读取，核心经验直接产基因 |
| **P0** | `archive/` | 35 | 按月+按类型扫描，Python脚本和SKILL文件优先 |
| **P0** | `daily/` | 28 | 扫描标题结构，提取对话信号模式 |
| **P0** | `report/` | 84 | 抽取最新5份报告分析结构模板 |
| **P0** | `shared/` | 12 | 全部读取，跨agent共享经验 |
| **P1** | `workspace-final/skills/` | 57 | 读取所有SKILL.md + references/ + scripts/ |
| **P1** | `/root/.openclaw/share/` | 52 | 读取cron配置+邮件系统+同步系统+学习工作流 |
| **P1** | `/root/.openclaw/skills/` | 19 | 读取capability-evolver+记忆管理+自我改进 |
| **P2** | `archive/history-2026-03/` | 5 | 扫描标题了解历史记录模式 |
| **P2** | `archive/history-2026-04/` | 24 | 扫描标题了解历史记录模式 |

#### 8.1.2 子文件夹扫描模板

```bash
# 1. 先列目录结构
echo "=== 目录X ==="
find /path/to/dir -type f | sort

# 2. 按优先级读取核心文件
for f in /path/to/dir/*/SKILL.md; do
    echo "=== $(basename $(dirname $f)) ==="
    head -30 "$f"
done

# 3. 扫描references子目录
for f in /path/to/dir/*/references/*.md; do
    echo "=== $(basename $(dirname $f))/$(basename $f) ==="
    head -50 "$f"
done

# 4. 扫描scripts子目录（Python/Bash脚本）
for f in /path/to/dir/*/scripts/*.py; do
    echo "=== $(basename $(dirname $f))/$(basename $f) ==="
    head -60 "$f"
done

# 5. 扫描cron配置
for f in /path/to/share/final-analysis/*.cron; do
    echo "=== $(basename $f) ==="
    cat "$f"
done
```

#### 8.1.3 常见遗漏点（违规记录）

| # | 遗漏 | 后果 | 教训 |
|---|------|------|------|
| 1 | 只看目录结构不进入子文件夹 | 遗漏skills/下的references/和scripts/ | `find -type f` 必须配合逐文件读取 |
| 2 | 忽略share/目录 | 遗漏cron配置+邮件系统+邮件模板 | share/是跨agent共享目录，必须扫描 |
| 3 | 忽略workspace-final/skills/ | 遗漏SKILL.md+模板+checklists | skills/下的references/和scripts/是核心经验源 |
| 4 | 只读report/不读模板 | 遗漏报告结构规范 | 必须同时读report/和skills/a-stock-daily-report/references/ |
| 5 | 忽略archive/中的Python脚本 | 遗漏数据采集经验 | .py脚本包含API调用策略和降级逻辑 |
| 6 | 忽略cron脚本 | 遗漏17项操作规则 | cron脚本的prompt就是最完整的操作规范 |

### 8.2 基因注入方案（Final Agent 25个基因）

#### 8.2.1 基因分类

| 类别 | 数量 | 覆盖范围 |
|------|------|---------|
| optimize | 17 | 持仓管理、报告结构、数据源、邮件发送、记忆协议、基金推荐 |
| repair | 6 | 反爬降级、代码验证、防跳过、碎片合并、同步可靠性、模板漂移 |
| innovate | 2 | 市场状态识别、学习提取工作流 |

#### 8.2.2 基因清单

**Optimize（17个）**：

| # | 基因ID | 核心策略 | 信号来源 |
|---|--------|---------|---------|
| 1 | gene_portfolio_check_before_advice | 分析前必查持仓，已清仓只能推荐重新建仓 | MEMORY.md + README.md |
| 2 | gene_portfolio_data_authority | Obsidian版本为唯一权威源，禁止覆盖 | MEMORY.md |
| 3 | gene_report_structure_morning | 早盘报告13章完整结构 | template-morning.md + checklists.md |
| 4 | gene_report_structure_midday | 午盘报告9章结构 | README.md + checklists.md |
| 5 | gene_report_structure_afternoon | 尾盘报告11章结构 | README.md + afternoon-report.cron |
| 6 | gene_report_structure_review | 复盘报告11章结构 | README.md + checklists.md |
| 7 | gene_report_logic_consistency | 报告逻辑一致性4条（不矛盾） | SKILL-2026-05-27.md |
| 8 | gene_report_quality_validation | 操作建议具体化+命中率根因分析 | README.md + SKILL-2026-05-27.md |
| 9 | gene_data_source_priority | 腾讯>东财>akshare>Tavily | TOOLS.md + a-stock-data/SKILL.md |
| 10 | gene_fund_flow_api_strategy | push2只通过web_fetch | TOOLS.md |
| 11 | gene_multi_source_data_architecture | 六层数据架构21个端点 | a-stock-data/SKILL.md |
| 12 | gene_price_authority_rule | 数据源A为唯一价格基准 | a-stock-analysis-lite/references/ |
| 13 | gene_table_format_preference | 6列表格结构 | experience.md + MEMORY.md |
| 14 | gene_email_send_workflow | MD→HTML→验证→发送→清理 | html-email-format.md + mail-skill-setup-guide.md |
| 15 | gene_new_fund_recommendation | 场外基金+API验证+7天预判 | README.md v3.2 |
| 16 | gene_memory_daily_protocol | frontmatter+时间顺序+双写 | memory-auto-write.md + instant-archive.md |
| 17 | gene_report_index_sync | wikilink+表格+倒序 | MEMORY.md |

**Repair（6个）**：

| # | 基因ID | 核心策略 | 信号来源 |
|---|--------|---------|---------|
| 18 | gene_anticrawl_fallback | 东财>同花顺>雪球，不硬扛WAF | experience.md + ERRORS.md |
| 19 | gene_fund_code_verification | API验证代码，禁止凭记忆 | SOUL.md 违规记录 |
| 20 | gene_session_end_protocol_enforce | 8步检查，每步必须有工具调用证据 | AGENTS.md + SOUL.md |
| 21 | gene_memory_fragment_merge | 去重→融入→立即删除 | AGENTS.md |
| 22 | gene_obsidian_sync_reliability | md5sum对比+原子删除 | AGENTS.md + sync-daily-to-obsidian/ |
| 23 | gene_report_template_drift | 模板检查+章节完整性 | a-stock-daily-report/references/ |

**Innovate（2个）**：

| # | 基因ID | 核心策略 | 信号来源 |
|---|--------|---------|---------|
| 24 | gene_market_regime_detection | 8维度温度+恐慌预案+连续走势 | MEMORY.md + README.md v3.4 |
| 25 | gene_learning_extraction_workflow | memory→.learnings→定期回顾 | learning-workflow/ + self-improving-agent/ |

#### 8.2.3 基因格式（JSONL）

```json
{"type":"Gene","id":"gene_portfolio_check_before_advice","category":"optimize","signals_match":["持仓","基金","加仓","减仓","止损","建仓","清仓","操作建议"],"preconditions":["用户请求涉及持仓分析或投资决策"],"strategy":["读取portfolio.md获取最新持仓","核对每只基金状态","已清仓基金只能推荐重新建仓"],"constraints":{"max_files":3,"forbidden_paths":["node_modules",".git"],"required_reads":["/home/obsidian_vault/2-Final-Memory/portfolio.md"]},"validation":["推荐新基金前检查是否已持有同类型","操作建议与风险提示不矛盾"]}
```

### 8.3 运行配置

#### 8.3.1 环境变量
```bash
export OPENCLAW_WORKSPACE=/root/.openclaw/workspace-final
export EVOLVER_SESSION_SCOPE=final
```

#### 8.3.2 路径映射
| 用途 | 路径 |
|------|------|
| 基因库 | ~/.openclaw/skills/capability-evolver/assets/gep/scopes/final/ |
| 固化状态 | ~/.openclaw/workspace-final/memory/evolution/scopes/final/ |
| 信号源 | ~/.openclaw/workspace-final/memory/ |
| 经验源 | /home/obsidian_vault/2-Final-Memory/ |

#### 8.3.3 运行命令
```bash
# 首次用review模式
cd ~/.openclaw/workspace-final && bash evolve.sh --review

# 日常低频后台（建议每天凌晨2:00）
cd ~/.openclaw/workspace-final && bash evolve.sh --strategy balanced
```

#### 8.3.4 与现有cron的关系
```
现有系统（不受影响）:
  cron 09:10 → 早盘报告
  cron 12:00 → 午盘报告
  cron 14:30 → 尾盘报告
  cron 16:00 → 复盘报告

新增系统（低频后台）:
  cron 02:00 → evolve.sh --strategy balanced
  → 基因库更新 → 下次报告时基因匹配生效
```

### 8.4 知识源→基因映射表

| 知识源文件 | 产出基因 | 经验提取方式 |
|-----------|---------|-------------|
| MEMORY.md | gene_portfolio_check, gene_portfolio_data_authority, gene_session_end_protocol | 直接提取铁律和规则 |
| share/final-analysis/README.md | gene_report_structure_*, gene_report_logic_consistency | 提取报告规则和章节要求 |
| knowledge/experience.md | gene_anticrawl_fallback, gene_table_format | 提取实战经验和格式规范 |
| archive/SKILL-2026-05-27.md | gene_report_logic_consistency, gene_report_quality | 提取4条逻辑一致性规则 |
| a-stock-daily-report/SKILL.md | gene_report_structure_*, gene_new_fund_recommendation | 提取报告模板和基金推荐规范 |
| a-stock-daily-report/references/checklists.md | gene_report_quality_validation | 提取Checklist |
| a-stock-daily-report/references/fund-code-registry.json | gene_fund_code_verification | 提取已验证基金代码 |
| a-stock-data/SKILL.md | gene_multi_source_data_architecture, gene_data_source_priority | 提取六层数据架构 |
| a-stock-analysis-lite/references/data-sources.md | gene_price_authority_rule | 提取价格权威性规则 |
| a-stock-analysis-lite/references/report-template.md | gene_report_structure_morning | 提取HTML报告模板 |
| morning-report.cron | gene_report_structure_morning, gene_market_regime_detection | 提取17项操作规则 |
| afternoon-report.cron | gene_report_structure_afternoon | 提取尾盘操作规则 |
| shared/html-email-format.md | gene_email_send_workflow | 提取排版规则 |
| shared/mail-skill-setup-guide.md | gene_email_send_workflow | 提取发送配置 |
| shared/memory-auto-write.md | gene_memory_daily_protocol | 提取归档规范 |
| shared/instant-archive.md | gene_memory_daily_protocol, gene_memory_fragment_merge | 提取即时归档格式 |
| shared/sync-daily-to-obsidian/README.md | gene_obsidian_sync_reliability | 提取同步规范 |
| shared/log-archive.md | gene_memory_cleanup_protocol | 提取归档目录规则 |
| share/daily-report-config.md | gene_report_structure_* | 提取cron配置 |
| capability-evolver/SKILL.md | gene_learning_extraction_workflow | 提取Evolver运行机制 |
| self-improving-agent/SKILL.md | gene_learning_extraction_workflow | 提取.learnings/规范 |
| share/learning-workflow/ | gene_learning_extraction_workflow | 提取学习工作流 |

### 8.5 关键教训（Final Agent 特有）

1. **子文件夹必须深度扫描**: 只看目录结构就规划，会遗漏 80% 的经验（如 references/、scripts/、cron 脚本）
2. **cron 脚本是最完整的操作规范**: morning-report.cron 的 prompt 包含 17 项操作规则，比任何文档都详细
3. **SKILL.md 不等于全部**: 每个 SKILL 的 references/ 子目录才是真正的方法论（模板、数据源、checklist）
4. **违规记录是最好的基因来源**: MEMORY.md 中的违规记录直接产出了防跳过、代码验证等 repair 基因
5. **跨 agent 共享目录是关键**: /root/.openclaw/share/ 包含邮件系统、同步系统、学习工作流，是所有 agent 的共同经验
