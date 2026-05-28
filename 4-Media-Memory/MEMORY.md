# MEMORY.md - 长期记忆

## 🚨 身份认知铁律
- **我是 Media（自媒体总监），执行者非主管**，只接受 main 调度
- **工作区**：`~/.openclaw/workspace-media`，禁止访问其他工作区
- **安全红线**：破坏性操作/敏感数据外发必须先确认；私密信息永不外泄

---

## 🎯 核心身份
- **名字**: Media | **角色**: 内容执行者（非主管）
- **专长**: 小红书/抖音/公众号内容创作；爆款文案；热点追踪；数据分析
- **沟通风格**: 活泼有亲和力，善用 Emoji，懂流量密码但不过度标题党

---

## 📋 职责范围
✅ 内容创作、运营、热点追踪、资讯抓取
❌ 无调度权，不能给自己或他人安排任务

---

## 🛠️ 技术栈
- 工具：web_search/web_fetch/browser/feishu_*/memory_*
- 记忆：MEMORY.md（主记忆）+ memory/YYYY-MM-DD.md（每日日志）+ .learnings/（结构化知识库）

---

## 🔄 会话启动自检
1. pwd 确认工作区：`~/.openclaw/workspace-media`
2. 检查 agentId 为 "media"
3. 异常 → 记录并上报 main

---

## ⚠️ 核心操作铁律
**即时记录原则**：每次工具调用、用户交互、文案产出后立即写入 `memory/YYYY-MM-DD.md`，禁止堆积。

---

## 📜 工作原则（索引）

| 原则 | 详情位置 |
|------|---------|
| 即时归档 | `memory/experience.md` |
| 记忆提取 | `.learnings/auto-extract.js` |
| MEMORY精简 | `EXPERIENCE-MEMORY-OPTIMIZE.md` |
| QMD使用 | `QMD_TIPS.md` |
| 会话归档 | `memory/2026-04-24.md` + .learnings/ |
| **日志归档规范** | `/home/obsidian_vault/shared/experience-archive.md` ⭐ |

---

## 🔮 QMD 使用指南
```bash
# 搜索共享文档（浏览器经验）
qmd search "CDP 9222" -c share --max-results 3

# 检查端口
netstat -tlnp | grep 9222
```

---

## 📂 记忆体系（Obsidian 迁移后）

| 路径 | 说明 |
|------|------|
| `/home/obsidian_vault/4-Media-Memory/MEMORY.md` | 长期记忆（软链接自 `~/.openclaw/workspace-media/MEMORY.md`） |
| `/home/obsidian_vault/4-Media-Memory/daily/` | 历史每日日志（YYYY-MM-DD.md） |
| `~/.openclaw/workspace-media/memory/YYYY-MM-DD.md` | 当日日志（工作区保留） |
| `/home/obsidian_vault/4-Media-Memory/knowledge/` | 专项经验文件 |
| `/home/obsidian_vault/4-Media-Memory/archive/` | 归档文件 |

**⚠️ 写入规则**：
- 长期记忆写入 `/home/obsidian_vault/4-Media-Memory/MEMORY.md`（通过软链接自动同步）
- 每日日志写入 `~/.openclaw/workspace-media/memory/YYYY-MM-DD.md`（当日），定期归档到 Obsidian daily/
- 专项经验写入 `/home/obsidian_vault/4-Media-Memory/knowledge/`

**📦 归档规则**（详见 `/home/obsidian_vault/shared/experience-archive.md`）：
- 月度归档：`archive/YYYY-MM.md`（合并当月所有 daily 日志）
- 原始文件保留：`archive/history-YYYY-MM/`（不删除）
- 归档后清理 daily/ 下已归档文件
- 标题层级：一级=月度标题、二级=日期标题、三级=时间条目
- 用 Python 脚本处理（不用 shell sed/awk），归档后必须验证完整性

---

## 📂 可用参考文档

| 文件路径 | 用途 |
|---------|------|
| `memory/experience.md` | 团队经验沉淀（身份、规范、隔离原则） |
| `.learnings/LEARNINGS.md` | 结构化学习条目（最佳实践、原则） |
| `.learnings/ERRORS.md` | 错误与修复记录 |
| `.learnings/FEATURE_REQUESTS.md` | 功能需求与改进建议 |
| `EXPERIENCE-MEMORY-OPTIMIZE.md` | **MEMORY.md 精简经验**（tech传授） |
| `QMD_TIPS.md` | **QMD 使用技巧**（软链接不穿透解法） |
| `TEACHING-MEMORY-BROWSER-QMD.md` | **浏览器经验 QMD 索引传授** |
| `/root/.openclaw/share/browser/experience-browser.md` | **浏览器自动化专项经验** |
| `/home/obsidian_vault/shared/experience-archive.md` | **日志归档规范与踩坑经验**（目录规则、操作流程、8条教训）⭐ |
| `SOUL.md` | 操作规范源头（铁律、清单、流程） |
| `IDENTITY.md` | 身份快照（职责、风格、边界） |
| `AGENTS.md` | 团队边界与协作原则 |
| `strategy/` | 内容策略与样例库（爆款文案、模板） |
| `.learnings/` | 结构化知识库（经验、错误、需求） |

---

---

## 📌 核心经验（2026-04-20）

### MEMORY.md 精简
- **执行时间**: 2026-04-20 15:20
- **效果**: 21.7KB → 2.9KB（-86%）
- **原则**: 核心规则保留，具体操作外移
- **执行步骤**: 备份 → 拆分 → 重写 → 验证效果

### QMD 向量搜索
- **命令**: `qmd search`（BM25）/ `qmd vsearch`（向量）/ `qmd query`（混合）
- **前提**: `vsearch` 需要先运行 `qmd embed` 生成向量数据库
- **当前状态**: 233 个文档 pending embedding

### Session 检查记录
- **检查时间**: 2026-04-20 16:38 GMT+8（全面覆盖检查）
- **检查范围**: 所有 session 文件（2026-04-14/16/20）
- **补录结果**: 2026-04-14 日记补录 12:01-14:53 共 9 条缺失记录
- **下次起始点**: 2026-04-20 16:38 之后的记录无需重新检查全部历史

---

**记住**：MEMORY.md 是启动入口，细节在外围文档。保持精简，让 QMD 承担历史检索！

## 📌 核心经验（2026-04-24）

### 上午 - 会话归档与学习沉淀
- **执行时间**: 2026-04-24 09:20
- **关键发现**: 建立结构化知识管理体系，包含错误日志、功能请求、最佳实践
- **归档策略**: 保持 session 文件格式不变，重点提取知识点到记忆体系
- **学习要点**:
  - 即时记录铁律：每次工具调用后必须立即写入 daily log
  - 路径管理规范：统一使用 `~` 而非硬编码路径
  - 文件边界原则：SOUL.md 负责规范，MEMORY.md 负责记录
  - 错误分类方法：按严重程度和类别建立错误日志体系

### 下午 - 浏览器CDP + 热点查询 + 链接验证（踩坑教训）
- **时间**: 2026-04-24 09:33-10:50
- **错误1 - 工具选择**: 查小红书热点上来就用 `tavily_search`，没走 `agent-browser --cdp 9222`
  - 教训：遇到"查平台内容"→ 优先浏览器CDP，搜索工具备选
- **错误2 - 跳过验证**: 截图分享链接没验证，连续犯三次才做对
  - 教训：分享前必须 `curl -I` 验证200后才发
- **正确流程（截图分享三步走）**:
  1. `agent-browser --cdp 9222 screenshot "/tmp/xxx.png"`
  2. `python3 -m http.server 8889 --bind 0.0.0.0 --directory /tmp/`
  3. `curl -I http://192.168.1.210:8889/xxx.png` 验证200后 → 发链接
- **明知故犯最该反省**: 文档有明确步骤但没执行到位，比不知道更严重


## Promoted From Short-Term Memory (2026-04-27)

<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:147:147 -->
- **2. 浏览器经验 QMD 索引（软链接不穿透）** [score=0.807 recalls=0 avg=0.620 source=memory/2026-04-20.md:147-147]

## Promoted From Short-Term Memory (2026-04-29)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:3:3 -->
- **触发**: 用户要求学习共享文档浏览器经验，并查询小红书热点 [score=0.810 recalls=0 avg=0.620 source=memory/2026-04-24.md:3-3]
<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:17:17 -->
- **第一次尝试（错误路径）**: [score=0.810 recalls=0 avg=0.620 source=memory/2026-04-24.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:22:22 -->
- **第二次尝试（正确路径）**: [score=0.810 recalls=0 avg=0.620 source=memory/2026-04-24.md:22-22]

## Promoted From Short-Term Memory (2026-04-30)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:27:27 -->
- **热榜数据获取**: [score=0.872 recalls=0 avg=0.620 source=memory/2026-04-24.md:27-27]
<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:34:34 -->
- **小红书今日热点TOP3**: [score=0.872 recalls=0 avg=0.620 source=memory/2026-04-24.md:34-34]

## Promoted From Short-Term Memory (2026-04-30)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:69:72 -->
- | 错误类型 | 描述 | 严重程度 | |---------|------|---------| | 工具选择错误 | 查平台内容优先用浏览器而非搜索工具 | 高 | | 跳过验证步骤 | 分享链接前不验证可访问性 | 高 | [score=0.881 recalls=0 avg=0.620 source=memory/2026-04-24.md:69-72]

## Promoted From Short-Term Memory (2026-05-01)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:73:73 -->
- | 不执行已知规范 | 文档有明确步骤但没执行 | 极高 | [score=0.897 recalls=0 avg=0.620 source=memory/2026-04-24.md:73-73]

## Promoted From Short-Term Memory (2026-05-01)

<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:44:44 -->
- **错误根源**: [score=0.884 recalls=0 avg=0.620 source=memory/2026-04-24.md:44-44]

## Promoted From Short-Term Memory (2026-05-08)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:4:5 -->
- **触发**: 用户指令"学习归档经验，将3月份记忆归档" **工具**: read, exec, write (Python脚本) [score=0.884 recalls=0 avg=0.620 source=memory/2026-05-03.md:4-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:14:14 -->
- **结果**: 归档完成，目录结构规范 [score=0.884 recalls=0 avg=0.620 source=memory/2026-05-03.md:14-14]

## Promoted From Short-Term Memory (2026-05-08)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:20:21 -->
- **触发**: 用户指令"更新MEMORY.md等文件中针对共享经验文档shared相关的索引位置" **工具**: read, edit [score=0.845 recalls=0 avg=0.620 source=memory/2026-05-03.md:20-21]

## Promoted From Short-Term Memory (2026-05-09)

<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:28:28 -->
- **结果**: 所有索引更新完成 ✅ [score=0.893 recalls=0 avg=0.620 source=memory/2026-05-03.md:28-28]

## Promoted From Short-Term Memory (2026-05-14)

<!-- openclaw-memory-promotion:memory:memory/2026-05-07.md:26:27 -->
- **触发**: 用户指令 — "将今天的对话写日每日记忆文件" **工具**: read → sessions_history → write [score=0.885 recalls=0 avg=0.620 source=memory/2026-05-07.md:26-27]

## Promoted From Short-Term Memory (2026-05-14)

<!-- openclaw-memory-promotion:memory:memory/2026-05-07.md:32:32 -->
- **结果**: ✅ daily log 补全完成 [score=0.885 recalls=0 avg=0.620 source=memory/2026-05-07.md:32-32]

## Promoted From Short-Term Memory (2026-05-20)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:14:17 -->
- **触发**: 用户要求学习 `/root/.openclaw/share/memory-auto-write-optimization.md` 并更新核心文件 **工具**: read/edit/write **结果**: 成功完成所有 4 个核心文件的更新 **决策**: 按照方案 v1.5 的规范，将"被动记录"升级为"对话结束前自动写入"四重机制协议 [score=0.802 recalls=0 avg=0.620 source=memory/2026-05-18.md:14-17]

## Promoted From Short-Term Memory (2026-05-21)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:31:34 -->
- **触发**: 用户指出 2026-05-18.md 缺少 frontmatter **工具**: read/edit/write/exec **结果**: 成功 **决策**: 按方案 v1.5 规范，所有 daily-log 文件需带标准 frontmatter [score=0.887 recalls=0 avg=0.620 source=memory/2026-05-18.md:31-34]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:44:47 -->
- **触发**: 用户要求归档 4 月日志 **工具**: exec/read/write **结果**: 成功完成 **决策**: 参照 3 月归档模式（history-2026-03/ + 2026-03.md 索引） [score=0.887 recalls=0 avg=0.620 source=memory/2026-05-18.md:44-47]

## Promoted From Short-Term Memory (2026-05-24)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:7:8 -->
- created: 2026-05-18T13:19:00+08:00 modified: 2026-05-18T13:34:00+08:00 [score=0.888 recalls=0 avg=0.620 source=memory/2026-05-18.md:7-8]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:2:3 -->
- date: 2026-05-18 weekday: Monday [score=0.878 recalls=0 avg=0.620 source=memory/2026-05-18.md:2-3]

## Promoted From Short-Term Memory (2026-05-28)

<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:14:17 -->
- **触发**: 用户要求将「复述确认规则」写入核心文件 SOUL.md **工具**: read(SOUL.md), edit(SOUL.md), write(memory/2026-05-25.md) **结果**: 成功 — 在 SOUL.md 的「🔍 运行时状态检查」和「💪 你的专长与能力」之间新增「📣 复述确认规则」章节 **决策**: 规则放在靠前的位置，确保每次收到任务都能第一时间触发复述流程 [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-25.md:14-17]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:20:23 -->
- **触发**: 用户要求检查 2026-05-18 的记忆完整性，合并到主文件 **工具**: exec(ls/md5sum/rm), read(主文件+子文件+Obsidian), edit(2026-05-25.md) **结果**: 成功 — 子文件 2026-05-18-1359.md 内容已完全包含在主文件中，去重删除；Obsidian md5 一致无需重同步 **决策**: 子文件为 session 摘要，与主文件记录重复，直接删除不追加 [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-25.md:20-23]
<!-- openclaw-memory-promotion:memory:memory/2026-05-25.md:7:8 -->
- created: 2026-05-25T15:46:00+08:00 modified: 2026-05-25T15:46:00+08:00 [score=0.874 recalls=0 avg=0.620 source=memory/2026-05-25.md:7-8]
