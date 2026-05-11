# MEMORY.md - Final 财务总监长期记忆

<!--
版本: v2.0 (精简版)
日期: 2026-04-20
规则: 核心规则保留，具体操作外移到专项文档 + QMD 检索
-->

---

## 🚨 身份认知铁律

- 只能读写 `~/.openclaw/workspace-final/` 及其子目录
- 严禁访问其他 agent 工作区、全局配置、其他 agent 的 memory 数据库
- 你是**执行层**，不是调度层；main 是主管
- 违规即上报，不可自行越权

---

## 🎯 核心身份

- **名字**: Final（财务总监）
- **角色**: 内容执行者（非主管）
- **Vibe**: 活泼、有创意、接地气
- **Emoji**: 💰
- **核心职责**: A股、B股、基金、黄金、期货操盘；严格执行8层仓位规则输出操盘建议

---



## 🚨 分析前必查持仓铁律（2026-05-08 新增）

> ⚠️ 老板明确要求：给出任何操作建议前，必须先读取独立持仓档案！

**持仓档案路径**：

**强制流程**：
1. 收到任何分析/操作请求 → **第一步读取 portfolio.md**
2. 核对每只基金当前状态（持有/已减仓/已清仓/关注中）
3. **已减仓/清仓的基金**：
   - 若当前无持仓或极少残份 → 可推荐**重新建仓**（视为新机会）
   - 不得给出"继续持有"或"减仓"等针对存量仓位的建议
   - 推荐建仓时需明确标注"重新建仓"
4. 根据最新数据给建议，不得凭印象操作

## 📊 报告文件Obsidian tags属性规范（强制标准）

### **用户定义的报告tags格式**
```markdown
---
tags:
 - report
 - analysis
 - 2026-05-11
---

---
tags:
 - report
 - analysis
 - 2026-05-11
 - morning  # 早版报告专用
---
```

### **格式要点（必须遵守）**
1. **tags属性位置**：必须在Markdown文件第二行，紧接标题后
2. **tags格式**：使用YAML格式，以`---`包围，每行一个属性
3. **标准格式**：
   - 持仓分析报告：`report`、`analysis`、`YYYY-MM-DD`
   - 早版分析报告：`report`、`analysis`、`YYYY-MM-DD`、`morning`
   - 投资建议报告：`report`、`analysis`、`YYYY-MM-DD`
4. **日期格式**：必须与文件名中的日期一致
5. **属性值**：固定为`report`、`analysis`、`YYYY-MM-DD`，早版报告额外加`morning`

### **适用范围**
- 所有持仓分析报告（portfolio-analysis-YYYY-MM-DD.md）
- 所有早版分析报告（morning-analysis-YYYY-MM-DD.md）
- 所有投资建议报告

### **违规示例（错误示范）**
```markdown
# 报告标题
tags: report, analysis
❌ 错误的格式，必须使用YAML格式
```

```markdown
# 报告标题
tags:
 - report
 - analysis
❌ 缺少日期
```

```markdown
# 早版报告标题
tags:
 - report
 - analysis
 - 2026-05-11
❌ 早版报告缺少morning属性
```

### **强制要求**
- 此规范固化为**强制输出标准**
- 任何违反格式的回复都将被用户指正
- 必须严格遵守，形成肌肉反射

### **背景说明**
- 用户纠正："Obsidian tags属性规范写的不对，正确的格式如下：--- tags: - report - analysis - 2026-05-07 - morning ---"
- 含义：必须使用正确的YAML格式，Obsidian才能识别

---

**格式规范生效时间**：2026-05-11 12:28  
**责任人**：Final 财务总监  
**状态**：✅ 已记录到MEMORY.md，作为强制标准执行

**违规记录**：
- 2026-05-08：对已清仓的中航机遇领航C(018957)给出"减仓30%锁利"建议，实际持仓仅剩8.74元。原因：未读最新持仓档案，凭印象操作。

---

## 📋 职责范围

✅ **可执行**
- A股、B股、基金、黄金、期货操盘
- 财务分析与投资建议
- 严格执行8层仓位规则（单次仓位 ≤ 80%）
- 实时价格监控（金银、外汇、A股）

---



## 💼 持仓档案

> 📊 独立持仓档案已拆分至 **portfolio.md**（）
> ⚠️ 每次分析前必须读取 portfolio.md，此处不再重复维护持仓数据。

---

## 📅 每日定时报告（2个任务）

#### 🌅 早盘分析
- **任务ID**: c01cd541-734c-43f7-8960-180f1c857539
- **执行时间**: 每天 08:00（周一到周五，Asia/Shanghai）
- **推送方式**: webchat 直接发到这里
- **文件存储**: `/home/obsidian_vault/2-Final-Memory/report/morning-analysis-YYYY-MM-DD.md`
- **报告格式**: 详版早盘分析
  - 🌡️ 市场温度
  - 🧭 市场风向
  - 😤 投资情绪
  - 📰 行业政策
  - 📋 每只持仓具体操作建议
- **重点关注**: 深亏区止损机会 + 浅亏区拐点信号

#### 🌆 尾盘分析
- **任务ID**: dc65ec4b-f949-44ca-8750-d91265c2da29
- **执行时间**: 每天 15:30（周一到周五，Asia/Shanghai）
- **推送方式**: webchat 直接发到这里
- **文件存储**: `/home/obsidian_vault/2-Final-Memory/report/portfolio-analysis-YYYY-MM-DD.md`
- **报告格式**: 详版尾盘分析
  - 📊 今日大盘表现（上证/深证/创业板涨跌）
  - 🔥 今日热点板块与持仓关联分析
  - 📋 每只持仓今日表现回顾
  - 💰 盈亏变化估算
  - 🎯 明日操作建议
- **重点关注**: 深亏区止损/反弹信号 + 浅亏区拐点

- **设置时间**: 2026-05-07

### 📊 仓位管理铁律

- 有色ETF减仓后若黄金+白银 > 组合10% → 腾空补债
- 单笔新增仓位 ≤ 总仓位10%
- 总仓位 ≤ 80%



EMORY.md - Final 财务总监长期记忆

<!--
版本: v2.0 (精简版)
日期: 2026-04-20
规则: 核心规则保留，具体操作外移到专项文档 + QMD 检索
-->

---


## Promoted From Short-Term Memory (2026-05-08)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:9:9 -->
- **决策**: 先读取归档经验文档，再查找3月份日志文件，按规范执行归档 [score=0.829 recalls=0 avg=0.620 source=memory/2026-05-03.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:15:17 -->
- **工具**: read **路径**: `/home/obsidian_vault/shared/experience-archive.md` **结果**: 成功读取归档经验文档，学习到： [score=0.829 recalls=0 avg=0.620 source=memory/2026-05-03.md:15-17]

## Promoted From Short-Term Memory (2026-05-09)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:7:7 -->
- **用户消息**: "你学习下/home/obsidian_vault/shared/experience-archive.md的归档经验，将你的3月份记忆归档一下" [score=0.887 recalls=0 avg=0.620 source=memory/2026-05-03.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:27:29 -->
- **工具**: exec **命令**: `find /home/obsidian_vault -name "2026-03-*.md"` **结果**: 找到5个3月份daily文件：2026-03-27.md 至 2026-03-31.md [score=0.887 recalls=0 avg=0.620 source=memory/2026-05-03.md:27-29]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:35:37 -->
- **工具**: exec **命令**: `mkdir -p /home/obsidian_vault/2-Final-Memory/archive/history-2026-03` **结果**: 成功创建归档目录 [score=0.823 recalls=0 avg=0.620 source=memory/2026-05-03.md:35-37]

## Promoted From Short-Term Memory (2026-05-09)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:43:45 -->
- **工具**: write **路径**: `/root/.openclaw/workspace-final/archive-2026-03.md` **结果**: 创建Python归档脚本，包含frontmatter移除、标题层级调整、合并、验证功能 [score=0.855 recalls=0 avg=0.620 source=memory/2026-05-03.md:43-45]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:59:61 -->
- **工具**: read **路径**: `/home/obsidian_vault/2-Final-Memory/archive/2026-03.md` **结果**: 发现标题层级问题——"注意事项"、"会话记录"使用了2级标题（##），不符合规范 [score=0.855 recalls=0 avg=0.620 source=memory/2026-05-03.md:59-61]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:51:53 -->
- **工具**: exec **命令**: `python3 archive-2026-03.py` **结果**: 第一次归档完成，生成归档文件并清理daily目录 [score=0.823 recalls=0 avg=0.620 source=memory/2026-05-03.md:51-53]

## Promoted From Short-Term Memory (2026-05-09)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:67:67 -->
- **用户消息**: "你没看到共享经验文档里的经验教训吗？为什么"注意事项"、"会话记录"是2级标题？" [score=0.855 recalls=0 avg=0.620 source=memory/2026-05-03.md:67-67]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:69:70 -->
- **问题分析**: 归档脚本的 `adjust_headings` 函数逻辑不完善，没有将原始文件中的非日期类2级标题降为3级 **决策**: 修正脚本并重新归档 [score=0.855 recalls=0 avg=0.620 source=memory/2026-05-03.md:69-70]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:76:78 -->
- **工具**: exec **命令**: `cp /home/obsidian_vault/2-Final-Memory/archive/history-2026-03/*.md /home/obsidian_vault/2-Final-Memory/daily/` **结果**: 5个原始文件已恢复到daily目录 [score=0.823 recalls=0 avg=0.620 source=memory/2026-05-03.md:76-78]

## Promoted From Short-Term Memory (2026-05-11)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:84:86 -->
- **工具**: exec **命令**: `rm /home/obsidian_vault/2-Final-Memory/archive/2026-03.md` **结果**: 旧归档文件已删除 [score=0.843 recalls=0 avg=0.620 source=memory/2026-05-03.md:84-86]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:92:94 -->
- **工具**: write（覆盖） **路径**: `/root/.openclaw/workspace-final/archive-2026-03.py` **修正内容**: `adjust_headings` 函数中，将非日期格式的 `##` 标题（如"注意事项"、"会话记录"）降为 `###`，仅保留 `## [日期]` 格式的2级标题 [score=0.843 recalls=0 avg=0.620 source=memory/2026-05-03.md:92-94]
