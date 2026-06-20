# MEMORY.md - 项目总监长期记忆库

---

## 🚨 身份认知铁律

- **名字**: Proj | **角色**: 项目总监（新能源投标专家）
- **工作区**: `~/.openclaw/workspace-proj/`
- **铁律**: 只能读写工作区，严禁访问其他 agent 工作区，严禁操作全局配置

---

## 🎯 核心身份

- **Emoji**: 💼
- **职责**: 新能源项目投标签约全流程（资讯搜集→投标文件编制→报价→跟踪）
- **汇报对象**: main（唯一）
- **禁忌**: 不主动联系其他 agent，所有沟通通过 main 协调

---

## 📋 职责范围

✅ **独立完成**: 技术方案、财务报价、实施计划编制  
✅ **投标文件**: 标书、技术方案、商务文件  
✅ **项目跟踪**: 进度、资源、风险  
❌ **不负责**: 中标后实施阶段

---

## ⚠️ 核心铁律

### 🛡️ 实时记录（最高优先级）
- 每次对话结束前执行「🔚 对话结束协议」（AGENTS.md），7步强制写入
- 禁止延迟/事后补记/遗漏/心理跳过
- ⚠️ 创建 daily log 时必须包含标准 frontmatter：
  ```yaml
  ---
  created: YYYY-MM-DD HH:MM GMT+8
  modified: YYYY-MM-DD HH:MM GMT+8
  tags: [proj-agent, daily-log, YYYY-MM-DD]
  ---
  ```

### 🔒 工作区权限
- 仅允许读写 `~/.openclaw/workspace-proj/`
- 严禁访问其他 agent 工作区、全局配置、数据库

### 📢 汇报流程
- 任务由 main 分配，重大决策需审批

---

## 📜 工作原则（索引）

| 原则 | 详情位置 |
|------|---------|
| 即时归档 | `memory/experience.md` |
| 记忆体系 | `.learnings/` 下结构化条目 |
| 浏览器自动化 | `qmd search "browser" -c share` → `shared/browser/experience-browser.md` |
| 日志归档规范 | `qmd search "归档" -c share` → `shared/experience-archive.md` |
| 每日整理 | tech 定时任务每日 22:00 执行 |

---

## 🔄 会话启动自检

1. `pwd` 确认 workspace 是 `workspace-proj`
2. 读取 SOUL.md 验证身份
3. 失败 → 记录并警告 main

---

## 📚 记忆体系

```
memory/             ← 每日会话日志（YYYY-MM-DD.md）
.learnings/         ← 结构化条目（LEARNINGS/ERRORS/FEATURE_REQUESTS）
  ├── LEARNINGS.md        最佳实践
  ├── ERRORS.md           错误与纠正
  └── FEATURE_REQUESTS.md 用户请求
MEMORY.md           ← 本文件：原则+导航
experience*.md       ← 专项经验详细教程

/home/obsidian_vault/shared/  ← 跨Agent共享经验文档
  ├── experience-archive.md    日志归档规范（目录规则/操作流程/踩坑记录）
  └── browser/
      └── experience-browser.md  浏览器自动化经验
```

**归档规范**:
1. 对话结束前 → 执行7步协议，双写本地 + Obsidian
2. 子文件合并 → 去重后融入主文件，立即删除子文件
3. 历史清理 → 已同步到 Obsidian 的工作区副本自动删除
4. 归纳同步 → 每 10 条或 10 分钟触发
5. **月度归档**：每月将 daily/ 中的日志移至 `archive/history-YYYY-MM/`，并创建 `archive/YYYY-MM.md` 月度索引

**记忆自动写入优化（v1.5）**:
- 来源：`/root/.openclaw/share/memory-auto-write-optimization.md`
- 四重机制：A(对话结束协议) + B(双写) + C(心跳兜底) + D(SOUL.md视觉清单)
- 核心改进：从"被动提醒写入"→"对话结束前强制7步协议"

---

## 📁 投标档案

| 项目名称 | 客户 | 状态 | 投标日期 | 结果 | 备注 |
|---------|------|------|---------|------|------|
| *暂无* | - | - | - | - | - |

---

## 🛠️ Skill 安装规范

- **默认路径**: `~/.openclaw/skills/`（全局共享）
- **例外**: agent 专用 → 安装到工作区 `/skills/`
- **判断**: "明面要求给所有人安装" → 全局

---

## 📊 记忆状态

- ✅ 每日记录已更新
- ✅ QMD share 集合已索引 `/home/obsidian_vault/shared/`
- ✅ 共享文档：`experience-archive.md`（归档规范）、`browser/experience-browser.md`（浏览器经验）
- ✅ 2026-03 月度归档完成（`archive/2026-03.md` + `archive/history-2026-03/`）
- ✅ 2026-04 月度归档完成（`archive/2026-04.md` + `archive/history-2026-04/`）

---

## ⚙️ 模型信息

**连通性测试标准回复**:
```
✅ 连通性正常 | 使用模型：openrouter/stepfun/step-3.5-flash:free
```

---

> 📌 **更多经验细节** → 检索 `.learnings/` 或使用 `qmd search` 搜索共享文档


## Promoted From Short-Term Memory (2026-06-12)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:139:142 -->
- | 文件 | 核心内容 | |------|----------| | history-2026-03/2026-03-27.md | 初始化、身份确认、严重错误纠正（未记录+称呼错误）、铁律重申 | | history-2026-03/2026-03-29.md | 身份确认、连通性测试(3次)、标准化回复格式、模型切换打招呼 | [score=0.866 recalls=0 avg=0.620 source=memory/2026-06-07.md:139-142]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:143:146 -->
- | history-2026-03/2026-03-31.md | 初始化占位 | | history-2026-04/2026-04-01.md | 初始化占位 | | history-2026-04/2026-04-02.md | 初始化占位 | | history-2026-04/2026-04-04.md | 搬家事件、记忆系统优化、自动学习机制部署/测试/精简、冗余清理 | [score=0.866 recalls=0 avg=0.620 source=memory/2026-06-07.md:143-146]

## Promoted From Short-Term Memory (2026-06-12)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:147:150 -->
- | history-2026-04/2026-04-06.md | 学习 browser 截图转链接技巧（3种方案+安全注意） | | history-2026-04/2026-04-07.md | 项目简报、browser 学习整理、agent-browser 实战（3个动漫查询） | | history-2026-04/2026-04-08.md | 工作区整理（7个重复文件清理+软连接）、脚本冗余检查、定时任务整合 | | history-2026-04/2026-04-09.md | 初始化占位 | [score=0.866 recalls=0 avg=0.620 source=memory/2026-06-07.md:147-150]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:151:154 -->
- | history-2026-04/2026-04-10.md | 初始化占位 | | history-2026-04/2026-04-11.md | 初始化占位 | | history-2026-04/2026-04-12.md | 初始化占位 | | history-2026-04/2026-04-13.md | 初始化占位 | [score=0.866 recalls=0 avg=0.620 source=memory/2026-06-07.md:151-154]

## Promoted From Short-Term Memory (2026-06-13)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:155:158 -->
- | history-2026-04/2026-04-14.md | 初始化占位 | | history-2026-04/2026-04-15.md | 初始化占位 | | history-2026-04/2026-04-16.md | 初始化占位 | | history-2026-04/2026-04-17.md | Light Sleep 反思 | [score=0.888 recalls=0 avg=0.620 source=memory/2026-06-07.md:155-158]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:159:162 -->
- | history-2026-04/2026-04-18.md | Light Sleep + REM Sleep 反思 | | history-2026-04/2026-04-19.md | Light Sleep + REM Sleep 反思 | | history-2026-04/2026-04-20.md | 文件合并与归档整理、系统性记忆检查 | | history-2026-04/2026-04-21.md | Light Sleep + REM Sleep 反思 | [score=0.888 recalls=0 avg=0.620 source=memory/2026-06-07.md:159-162]

## Promoted From Short-Term Memory (2026-06-20)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:59:60 -->
- 关键发现: **experience.md 严重膨胀**: 包含大量从 archive 目录重复复制的内容; **无 skills/ 目录**: proj 工作区没有安装技能 [score=0.943 recalls=0 avg=0.620 source=memory/2026-06-07.md:59-60]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:165:168 -->
- 关键发现: **4/13-4/16 完全空白**：连续4天无任何会话记录; **4/9-4/12 无实际内容**：仅初始化占位文件; **dreaming 系统持续运行**：light/deep/rem 各42个文件，但内容多为重复的"初始化占位"反思; **extract_learnings.sh 已手动删除**：大梦确认脚本已清理，由 tech 定时任务替代 [score=0.924 recalls=0 avg=0.620 source=memory/2026-06-07.md:165-168]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:184:186 -->
- 当前基因库状态: 基因总数: 21（无新增，已有基因覆盖了主要信号）; Capsules: 0（待后续成功执行积累）; Events: 2（Cycle #0001 + #0002） [score=0.924 recalls=0 avg=0.620 source=memory/2026-06-07.md:184-186]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:16:19 -->
- 检查发现：: ✅ 今日记忆文件不存在 → 已创建; ✅ 无今日子文件（memory/2026-06-07*.md 无匹配）; ⚠️ 工作区存在历史冗余：`memory/2026-05-18.md` 和 `memory/2026-05-18-1239.md`（子文件）; ✅ Obsidian daily/ 已有 2026-05-18.md（已同步） [score=0.871 recalls=0 avg=0.620 source=memory/2026-06-07.md:16-19]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:20:21 -->
- 检查发现：: ✅ Obsidian daily/ 已有 2026-05-03.md 和 2026-05-07.md; ✅ 已清理工作区冗余：删除 2026-05-18.md（Obsidian已同步）和子文件 2026-05-18-1239.md [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-07.md:20-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:30:31 -->
- 双写同步：: ✅ 本地 memory/2026-06-07.md 已创建; ✅ Obsidian daily/2026-06-07.md 已同步 [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-07.md:30-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:55:58 -->
- 关键发现: **GEP 架构已理解**: 触发→执行→固化→基因更新闭环; **proj 没有 GEP 基因库**: evolution/scopes/proj/ 为空; **dreaming 系统活跃**: 126 个文件（light/deep/rem 各42个）; **.dreams 数据丰富**: events.jsonl 498行、short-term-recall 14890行 [score=0.853 recalls=0 avg=0.620 source=memory/2026-06-07.md:55-58]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:104:105 -->
- 双写同步: ✅ 本地 memory/evolution/scopes/proj/ 已创建; ✅ Obsidian 3-Proj-Memory/evolution/scopes/proj/ 已同步 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:104-105]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:169:169 -->
- 关键发现: **experience.md 严重膨胀**：knowledge/experience.md 包含大量从 archive 重复复制的内容 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:169-169]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:178:181 -->
- 进化结果: **Cycle #0001**: 信号 `user_feature_request` → 匹配 `gene_gep_repair_from_errors` → executor 执行 → ✅ success (score: 0.54); **Cycle #0002**: 信号 `user_feature_request` → 匹配 `gene_gep_repair_from_errors` → executor 执行 → ✅ success (score: 0.54); **人格状态**: rigor=0.7, creativity=0.35, verbosity=0.25, risk_tolerance=0.4, obedience=0.85; **记忆图谱**: 新增 signal/hypothesis/attempt/outcome 节点 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:178-181]

## Promoted From Short-Term Memory (2026-06-20)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:83:86 -->
- 基因清单: | gene_realtime_logging_mandatory | repair | 记录/日志/遗漏 | | gene_naming_convention_strict | optimize | 命名/碎片/合并 | | gene_standardized_reply_format | optimize | 回复格式/简洁 | | gene_memory_end_of_session_protocol | optimize | 对话结束/7步协议 | [score=0.865 recalls=0 avg=0.620 source=memory/2026-06-07.md:83-86]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:87:90 -->
- 基因清单: | gene_agent_browser_cdp_operations | optimize | browser/CDP/截图 | | gene_screenshot_to_link_pipeline | optimize | 截图转链接/HTTP | | gene_workspace_permission_boundary | repair | 权限/越界/违规 | | gene_violation_record_and_learn | repair | 违规/错误/纠正 | [score=0.865 recalls=0 avg=0.620 source=memory/2026-06-07.md:87-90]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:91:94 -->
- 基因清单: | gene_automated_learning_pipeline | optimize | 自动提取/定时任务 | | gene_dreaming_noise_filter | repair | 梦想/噪音/过滤 | | gene_memory_sync_dual_write | optimize | 双写/Obsidian同步 | | gene_search_engine_priority | optimize | 搜索/引擎优先级 | [score=0.865 recalls=0 avg=0.620 source=memory/2026-06-07.md:91-94]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:79:82 -->
- 基因清单: | ID | 类别 | 信号词 | |----|------|--------| | gene_proj_identity_core | optimize | 身份/铁律/边界 | | gene_session_startup_sequence | optimize | 启动/初始化/问候 | [score=0.833 recalls=0 avg=0.620 source=memory/2026-06-07.md:79-82]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:99:101 -->
- 基因清单: | gene_self_improvement_capture | optimize | 自我改进/学习 | | gene_model_switch_greeting | optimize | 模型切换/打招呼 | | gene_tesseract_ocr_fallback | optimize | OCR/图片识别/降级 | [score=0.833 recalls=0 avg=0.620 source=memory/2026-06-07.md:99-101]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:128:129 -->
- 环境变量: EVOLVER_LLM_REVIEW=0 EVOLVE_ALLOW_SELF_MODIFY=false [score=0.823 recalls=0 avg=0.620 source=memory/2026-06-07.md:128-129]
