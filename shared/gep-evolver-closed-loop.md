<!--
作者: tech agent (v1.0) + final agent (v1.1 补充)
修改时间: 2026-06-06 20:33 GMT+8
版本号: v1.3.0
-->

# GEP Evolver 闭环：触发→执行→固化→基因更新

## 概述

本文档记录 GEP（Genome Evolution Protocol）Evolver 从零搭建到形成完整闭环的经验，覆盖 tech agent 和 final agent 两个 scope。包括架构设计、踩坑记录、修复方案、基因注入规范和当前状态。

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
| 基因匹配 | `selector.js` | 从基因库中匹配最佳策略 |
| 执行 | `sessions_spawn` | executor agent 按基因 strategy 修改文件 |
| 固化 | `node index.js solidify` | 将修改结果写入基因库 |
| 更新 | `genes.jsonl` + `events.jsonl` + `capsules.json` | 基因、事件、胶囊持久化 |

### 1.2 文件结构

#### Tech Scope（已部署）

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

#### Final Scope（已部署）

```
~/.openclaw/skills/capability-evolver/assets/gep/scopes/final/
├── genes.jsonl              # 56 个财务专属基因
├── events.jsonl             # 5 条进化事件
├── capsules.json            # 胶囊
├── memory_graph.jsonl       # 记忆图谱（91条）
├── evolution_state.json     # cycleCount=10
└── personality_state.json   # 人格状态

~/.openclaw/workspace-final/
└── memory/evolution/scopes/final/
    ├── genes.jsonl          # 工作区副本（与 assets 同步）
    ├── events.jsonl
    ├── memory_graph.jsonl
    ├── evolution_state.json
    └── personality_state.json
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

**⚠️ 多 scope 注意**: 不同 scope 的 workspace 和 scope 名称不同：

| Scope | OPENCLAW_WORKSPACE | EVOLVER_SESSION_SCOPE |
|-------|--------------------|-----------------------|
| tech | `/root/.openclaw/workspace-tech` | `tech` |
| final | `/root/.openclaw/workspace-final` | `final` |

创建新 scope 的 evolve.sh 时，自动 solidify 部分的环境变量必须对应修改。

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

### 3.1 Tech Scope

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

### 3.2 Final Scope（已部署）

| 指标 | 数值 |
|------|------|
| 基因数 | 56 个专属 + 58 个 main 通用 = 93 个可用 |
| 知识源 | 217 个文件（6 个目录全量扫描） |
| 基因库 | `assets/gep/scopes/final/` |
| 进化周期 | 10 轮 |
| 状态 | ✅ 已部署，运行中 |

---

## 4. 基因库概览

### 4.1 Tech Scope — 按类别分布

| 类别 | 数量 | 代表性基因 |
|------|------|-----------|
| optimize | 40 | gene_bash_script_best_practices, gene_docker_compose_deploy, gene_memory_maintenance |
| repair | 12 | gene_nextjs_systemd_deploy, gene_error_recovery, gene_service_deployment |

### 4.2 Tech Scope — TOP 5 匹配基因

1. gene_log_archive_standard（6/7 signals）
2. gene_html_email_format（6/8 signals）
3. gene_self_improvement_triggers（5/6 signals）
4. gene_docker_compose_deploy（4/5 signals）
5. gene_bash_script_best_practices（4/4 signals）

### 4.3 Scope 隔离架构（2026-06-06 改造）

Evolver 采用 **scope 隔离 + 通用基因库** 架构，每个 agent 的专属基因和通用基因分开存储，`loadGenes()` 自动合并加载。

#### 三层 scope 结构

| Scope | 基因数 | 内容 | 存放位置 |
|-------|--------|------|---------|
| **main** | 58 | 通用基因（浏览器、日志、归档、邮件排版、记忆管理...） | `assets/gep/scopes/main/` |
| **final** | 56 | 财务专属（持仓、基金、市场、报告、数据源...） | `assets/gep/scopes/final/` |
| **tech** | 16 | 技术专属（Docker、NextJS、Bash、Systemd、飞书...） | `assets/gep/scopes/tech/` |

> **selector 加载逻辑**: `loadGenes()` 加载 `当前 scope + main scope`，按 ID 去重，当前 scope 优先。
> final 运行时: 47 专属 + 58 main = 93 个可用基因。
> tech 运行时: 16 专属 + 58 main = 74 个可用基因。

#### main scope 通用基因分类

| 类别 | 数量 | 代表基因 |
|------|------|---------|
| 浏览器自动化 | 7 | gene_browser_automation, gene_browser_cdp_automation, gene_browser_path_management |
| 邮件排版 | 6 | gene_email_html_standard, gene_html_email_formatting, gene_html_email_format |
| 日志归档 | 4 | gene_log_archive_standard, gene_monthly_archive_standard, gene_backup_strategy |
| 记忆管理 | 8 | gene_memory_write_4mechanism, gene_memory_integrity_check, gene_memory_fragment_merge |
| 会话/文件 | 6 | gene_session_end_protocol, gene_subfolder_deep_scan, gene_no_append_to_end |
| GEP架构 | 3 | gene_gep_architecture_deep, gene_gep_repair_from_errors |
| 其他 | 24 | gene_cron_management, gene_error_recovery, gene_security_hardening, gene_sed_escape |

#### final scope 财务专属基因

| 类别 | 数量 | 代表基因 |
|------|------|---------|
| 持仓管理 | 8 | gene_portfolio_check_before_advice, gene_portfolio_zone_strategy, gene_ocr_portfolio_capture |
| 报告结构 | 9 | gene_report_structure_morning/midday/afternoon/review, gene_report_13section_template |
| 市场分析 | 7 | gene_market_regime_detection, gene_market_panic_sell_protocol, gene_market_regime_patterns |
| 数据源 | 6 | gene_data_source_priority, gene_data_authority_matrix, gene_fund_flow_api_strategy |
| 基金操作 | 5 | gene_new_fund_recommendation, gene_fund_forecast_7day, gene_fund_code_verification |
| 反爬/安全 | 2 | gene_anticrawl_fallback, gene_data_source_push2_only_web_fetch |
| 其他 | 19 | gene_session_end_protocol_enforce, gene_memory_daily_protocol 等 |

#### tech scope 技术专属基因

| 类别 | 数量 | 代表基因 |
|------|------|---------|
| Docker | 2 | gene_docker_compose_deploy, gene_docker_deploy_full |
| NextJS | 3 | gene_nextjs_systemd_deploy, gene_nextjs_build_optimize |
| Bash | 2 | gene_bash_script_best_practices, gene_bash_script_standard |
| 飞书 | 1 | gene_feishu_integration |
| 部署 | 4 | gene_service_deployment, gene_service_deploy_standard 等 |
| 其他 | 4 | gene_git_operation_safety, gene_delivery_standardization 等 |

---

## 5. 使用指南

### 5.1 手动触发

```bash
# Tech scope
cd ~/.openclaw/workspace-tech && bash evolve.sh

# Final scope
cd ~/.openclaw/workspace-final && bash evolve.sh
```

### 5.2 指定策略

```bash
bash evolve.sh --strategy harden   # 强化模式
bash evolve.sh --strategy balanced  # 平衡模式（默认）
bash evolve.sh --review            # 人工确认模式
```

### 5.3 查看基因

```bash
# Tech scope
cd ~/.openclaw/skills/capability-evolver
cat assets/gep/scopes/tech/genes.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    g = json.loads(line)
    if g.get('type') == 'Gene':
        print(f'{g[\"id\"]:50s} | {g[\"category\"]:10s} | signals={len(g.get(\"signals_match\",[]))}')
"

# Final scope（待 genes.jsonl 创建后）
cat assets/gep/scopes/final/genes.jsonl | python3 -c "
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

1. **Final scope 基因写入**: 将 25 个基因写入 `assets/gep/scopes/final/genes.jsonl`
2. **设置定时触发**: 每天凌晨 2 点自动跑 evolver（tech + final 各自独立）
3. **积累 capsule**: 当前 tech 1 个，目标 10+ 个触发蒸馏
4. **信号降噪优化**: 过滤 executor 自身产生的自引用信号
5. **基因质量审查**: 清理低质量基因，合并重叠基因
6. **蒸馏（Distill）**: 积累足够 capsule 后触发 skillDistiller 产出高阶基因

---

## 7. 关键教训

1. **环境变量是 solidify 的关键**: `OPENCLAW_WORKSPACE` + `EVOLVER_SESSION_SCOPE` 缺一不可（详见 2.1）
2. **executor 修改量要控制**: 当前 20 个文件太多，应该聚焦核心代码
3. **基因选择要避免局部最优**: 连续选同一基因说明信号或选择器有问题
4. **自动检测机制很重要**: 不能依赖 executor agent 自行完成 solidify
5. **知识源要持续扩充**: 79 个文件编码成了 52 个基因，还有提升空间
6. **多 scope 环境变量不同**: tech 和 final 的 workspace/scope 各自独立，创建新 scope 时注意修改（详见 2.1 表格）
7. **通用基因必须放 main scope，不要在各 scope 重复存放**: 浏览器自动化、日志归档、邮件排版、记忆管理等通用能力属于跨领域共性知识，应统一存放在 `assets/gep/scopes/main/` 基因库中。各 agent scope 只放专属基因。`loadGenes()` 已实现自动加载 `当前 scope + main scope`，无需重复存放。⚠️ 判断标准：如果基因的 strategy 不包含具体业务领域关键词（如持仓/基金/Docker/NextJS），就是通用基因，应放 main。

---

## 8. 基因注入规范：知识源扫描 SOP

> **⚠️ 适用范围**: 所有 agent 新建/扩充基因库时，必须遵循本 SOP，确保不遗漏经验。

### 8.1 扫描原则

1. **必须进入子文件夹深度扫描**，禁止只看目录结构就下结论
2. **先列目录 → 再按优先级读取 → 最后提炼基因**
3. **每个 SKILL.md 的 `references/` 和 `scripts/` 子目录是核心经验源**，不可跳过
4. **cron 脚本的 prompt 往往是最完整的操作规范**，不可忽略
5. **跨 agent 共享目录**（如 `share/`、`/root/.openclaw/share/`）包含共同经验，必须扫描
6. **违规记录是最好的 repair 基因来源**，重点扫描

### 8.2 扫描清单模板

```bash
# 1. 先列目录结构（不遗漏子文件夹）
echo "=== 目录X ==="
find /path/to/dir -type f | sort

# 2. 按优先级读取核心文件
for f in /path/to/dir/*/SKILL.md; do
    echo "=== $(basename $(dirname $f)) ==="
    head -30 "$f"
done

# 3. 扫描references子目录（核心方法论）
for f in /path/to/dir/*/references/*.md; do
    echo "=== $(basename $(dirname $f))/$(basename $f) ==="
    head -50 "$f"
done

# 4. 扫描scripts子目录（Python/Bash脚本）
for f in /path/to/dir/*/scripts/*.py; do
    echo "=== $(basename $(dirname $f))/$(basename $f) ==="
    head -60 "$f"
done

# 5. 扫描cron配置（最完整的操作规范）
for f in /path/to/share/*/*.cron; do
    echo "=== $(basename $f) ==="
    cat "$f"
done
```

### 8.3 Final Agent 知识源扫描实例

以下以 final agent 的实际扫描为例，展示完整扫描过程：

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

**总计**: 291 个文件 → 产出 25 个基因

### 8.4 常见遗漏点（违规记录）

| # | 遗漏 | 后果 | 教训 |
|---|------|------|------|
| 1 | 只看目录结构不进入子文件夹 | 遗漏skills/下的references/和scripts/ | `find -type f` 必须配合逐文件读取 |
| 2 | 忽略share/目录 | 遗漏cron配置+邮件系统+邮件模板 | share/是跨agent共享目录，必须扫描 |
| 3 | 忽略workspace-final/skills/ | 遗漏SKILL.md+模板+checklists | skills/下的references/和scripts/是核心经验源 |
| 4 | 只读report/不读模板 | 遗漏报告结构规范 | 必须同时读report/和skills/*/references/ |
| 5 | 忽略archive/中的Python脚本 | 遗漏数据采集经验 | .py脚本包含API调用策略和降级逻辑 |
| 6 | 忽略cron脚本 | 遗漏17项操作规则 | cron脚本的prompt就是最完整的操作规范 |

### 8.5 基因格式（JSONL）

```json
{"type":"Gene","id":"gene_portfolio_check_before_advice","category":"optimize","signals_match":["持仓","基金","加仓","减仓","止损","建仓","清仓","操作建议"],"preconditions":["用户请求涉及持仓分析或投资决策"],"strategy":["读取portfolio.md获取最新持仓","核对每只基金状态","已清仓基金只能推荐重新建仓"],"constraints":{"max_files":3,"forbidden_paths":["node_modules",".git"],"required_reads":["/home/obsidian_vault/2-Final-Memory/portfolio.md"]},"validation":["推荐新基金前检查是否已持有同类型","操作建议与风险提示不矛盾"]}
```

### 8.6 Final Agent 运行配置

```bash
# 环境变量
export OPENCLAW_WORKSPACE=/root/.openclaw/workspace-final
export EVOLVER_SESSION_SCOPE=final

# 路径映射
# 基因库: ~/.openclaw/skills/capability-evolver/assets/gep/scopes/final/
# 固化状态: ~/.openclaw/workspace-final/memory/evolution/scopes/final/
# 信号源: ~/.openclaw/workspace-final/memory/
# 经验源: /home/obsidian_vault/2-Final-Memory/

# 运行命令
cd ~/.openclaw/workspace-final && bash evolve.sh --review    # 首次
cd ~/.openclaw/workspace-final && bash evolve.sh --strategy balanced  # 日常

# 建议定时: 每天凌晨 02:00
# 不影响现有 4 个 cron 报告流程（09:10/12:00/14:30/16:00）
```

### 8.7 知识源→基因映射表（Final Agent）

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
