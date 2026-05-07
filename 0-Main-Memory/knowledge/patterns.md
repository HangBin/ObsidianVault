---
author: main agent
created: 2026-05-01 13:12:00 GMT+8
modified: 2026-05-01 13:12:00 GMT+8
version: v1.0.0
tags:
main-agent
knowledge
experience
patterns
---


author: main agent
created: 2026-05-01 13:10:00 GMT+8
modified: 2026-05-01 13:10:00 GMT+8
version: v1.0.0
tags:
 - main-agent
 - knowledge
 - experience
 - patterns

# 工程模式库 - 最佳实践与工作流

## 🎯 核心工程模式

### 1️⃣ 系统自愈模式
**触发条件**：HEARTBEAT 检测到 cron 任务超时 >1h  
**自动修复流程**：
1. 检测 cron 目录缺失 (`~/.openclaw/cron/`)
2. 创建目录结构 (`mkdir -p`)
3. 添加缺失任务 (`openclaw cron add`)
4. 重启 Gateway (`openclaw gateway restart`)
5. 验证任务列表 (`openclaw cron list`)

**成功案例**：2026-03-29 恢复瘫痪 24h+ 的每日简报任务  
**关键点**：无需管理员干预，系统自主强制触发完成修复

### 2️⃣ 双通道通信模式
**场景**：Agent 群聊通道异常 (timeout/401)  
**Fallback 策略**：
- 优先使用 `feishu:direct` 私聊会话
- 验证 agent 在线状态和响应速度
- 临时切换模型（如遇到 API 限制）

**应用**：Final agent 正常，Tech 间歇性，Media/Proj 需修复 credentials

### 3️⃣ 状态汇报模板化
**要求**：所有 agent 回复使用标准化格式  
**模板**：`✅ 连通性正常 | 使用模型：{model}`

**收益**：
- 减少"废话"，提高信息密度
- 便于自动化解析（正则匹配）
- 统一团队沟通规范

**执行记录**：Tech agent 14:18 首次遵循，后续全员推广

### 4️⃣ 即时归档自动化
**铁律**：任何操作单元后必须立即 `edit` 追加到 `memory/YYYY-MM-DD.md`  
**覆盖范围**：
- ✅ 工具调用（read/exec/write/edit/sessions_send 等）
- ✅ 用户回复
- ✅ 重要决策（即使无工具调用）

**双保险**：回复展示 + 文件持久化  
**效果**：记忆覆盖率 100%，零遗漏

### 5️⃣ 路径安全化
**问题**：绝对路径暴露敏感信息 (`/home/node/.openclaw`)  
**解决方案**：统一使用 `~/.openclaw` 引用  
**执行范围**：MEMORY.md + 所有 daily logs

**工具**：`grep` 定位 + `edit` 批量替换

### 6️⃣ 配置管理轻量化
**原则**：Agent 专用技能 → 工作区 `/skills/`；全局技能 → `~/.openclaw/skills/`  
**判断逻辑**："明面要求给所有人安装" → 全局；否则按 agent 专用  
**例外处理**：Agent 需要隔离时，安装到各自工作区

### 7️⃣ 记忆归纳触发机制
**规则**：每 10 分钟或每 10 条调度记录触发归纳  
**输出**：提炼调度策略、Agent 性能评估、用户偏好 → 同步到 MEMORY.md  
**现状**：依赖人工检查，需改进自动化


## 🔄 标准工作流

### 记忆文件维护工作流
**触发条件**：memory/ 目录出现碎片（重复日期、session 文件混入）
**维护流程**：
1. 识别异常文件：`ls memory/*.md` 检查重复日期和非 daily log 文件
2. 分类处理：
   - Session 存储文件 → 移至 `.recycle/bin/`（恢复 agents/ 存储结构）
   - 重复日期文件（如 `*-brief.md`）→ 合并内容后删除冗余
3. 验证结构：确保每个日期仅一个主文件，保留 `experience.md`
4. 更新索引：同步 `MEMORY.md` 中的文件管理规范

**成功案例**：2026-04-04 整理（删除4个文件，结构清洁）
**关键点**：定期执行（建议每周），避免碎片堆积

### 学习点持续提取模式
**触发周期**：每次记忆维护任务（03:00 AM）或用户指令

**提取来源**：
- ✅ `memory/YYYY-MM-DD.md`（daily logs）
- ✅ `memory/experience.md`（经验沉淀）
- ✅ 系统运行状态（cron 执行情况、错误日志）

**输出结构**：
- **LEARNINGS.md**：学习收获、优化点、模式识别（medium 优先级）
- **ERRORS.md**：失败案例、异常处理、根因分析（high/critical 优先级）
- **FEATURE_REQUESTS.md**：用户需求、自动化改进、功能增强（medium/high 优先级）

**条目格式**：
- ID 编码：LRN-YYYYMMDD-NNN / ERR-YYYYMMDD-NNN / REQ-YYYYMMDD-NNN
- 必填字段：Logged, Priority, Status, Area, Summary, Details, Suggested Action, Metadata
- 状态流转：pending → in_progress → resolved

**自动化建议**：
- 在记忆维护脚本中调用学习点提取器（分析 delta）
- 区分 auto_extract 和 manual 条目来源
- 定期将验证过的学习点升级到 MEMORY.md「核心原则」

**执行记录**：2026-04-04 首次完整执行，生成 4 新条目


## 📊 调度主管数据统计

- **总调度次数**：30+（自 3-27 起）
- **工具调用**：~18 次
- **agent 消息**：10+ 次
- **cron 操作**：5+ 次
- **归纳次数**：4 次
- **自主修复**：1 次（3-29）
- **管理员响应**：0 次（关键问题持续 5+ 小时）


## 🎯 调度主管最佳实践

1. **每次会话启动** → 读取 MEMORY.md + memory/昨天.md
2. **调度决策** → 写入 MEMORY.md（长期记忆）
3. **团队协作** → 记录到 memory/今天.md（每日原始日志）
4. **工具调用后** → 立即 `edit` 追加记录（触发、工具、参数、结果、决策）
5. **回复用户后** → 立即 `edit` 追加记录（回复内容、关键决策）
6. **每 10 分钟/10 条记录** → 触发归纳并同步到 MEMORY.md
7. **会话结束前** → 自检清单（所有操作是否已记录？）
8. **心跳检查发现异常** → 立即记录并升级告警级别
9. **任务监控项缺失** → 视为最高优先级，立即修复
10. **系统自愈能力** → 参考 3-29 案例，保持修复脚手架


## 🎯 核心原则（main 专用）

1. **自主性**：系统能自动修复 minor failures
2. **冗余设计**：双通道、双模型（主+备）
3. **模板化**：所有对外格式必须固化到配置文件
4. **轻量化**：避免过度设计，优先简单方案
5. **即时性**：记录必须在事件发生后 1 秒内完成
6. **零容忍**：任务监控项缺失必须立即修复（参考 3-31 教训）


## ⚠️ 待改进项

| 优先级 | 问题 | 状态 |
|--------|------|------|
| 🔴 紧急 | 修复 Media/Proj Feishu credentials（401 错误）| 未修复 |
| 🟠 高 | 修复 weekly-backup delivery 400 配置错误 | 未修复 |
| 🟡 中 | 小红书全自动发布方案 | 等待用户确认 |
| 🟡 中 | 实现归纳自动化检查点 | 待处理 |
| 🟢 低 | 审计工作区异常增长 | 需归档 |
| 🟢 低 | maintenance_agent.sh 缺失 | 跳过 |


**最后更新：2026-05-01 12:52**
