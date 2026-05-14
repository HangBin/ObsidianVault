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


## Promoted From Short-Term Memory (2026-04-23)

<!-- openclaw-memory-promotion:memory:memory/2026-04-16.md:5:6 -->
- **记录时间**: 2026-04-16 12:39:27 **状态**: 占位文件（由每日记忆管理系统自动创建） [score=0.903 recalls=0 avg=0.620 source=memory/2026-04-16.md:5-6]
<!-- openclaw-memory-promotion:memory:memory/2026-04-18.md:323:323 -->
- - Candidate: Reflections: No strong patterns surfaced. [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-18.md:3-3]

## Promoted From Short-Term Memory (2026-04-24)

<!-- openclaw-memory-promotion:memory:memory/2026-04-19.md:338:338 -->
- - Candidate: Reflections: No strong patterns surfaced. [score=0.829 recalls=0 avg=0.620 source=memory/2026-04-19.md:98-98]

## Promoted From Short-Term Memory (2026-04-25)

<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:116:118 -->
- - Candidate: Possible Lasting Truths: 00:00 - 初始化: **记录时间**: 2026-04-11 08:56:44 **状态**: 占位文件（由每日记忆管理系统自动创建） [confidence=0.58 evidence=memory/2026-04-11.md:5-6]; 00:00 - 初始化: **记录时间**: 2026-04-12 13:13:50 **状态**: 占位文件（由每日记忆管理系统自动创建） [confidence=0.58 evidence=memory/2026-04-12.md:5-6]; 00:00 - - confidence: 0.62 - evidence: memory/2026-04-19.md:341-343 [score=0.854 recalls=0 avg=0.620 source=memory/2026-04-20.md:8-10]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:122:122 -->
- **触发**: 用户要求合并归档文件 [score=0.854 recalls=0 avg=0.620 source=memory/2026-04-20.md:122-122]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:135:137 -->
- **触发**: 用户指令"把今天tech传授的三个核心内容学习一下" **文件**: EXPERIENCE-MEMORY-OPTIMIZE.md、QMD_TIPS.md、TEACHING-MEMORY-BROWSER-QMD.md **结果**: ✅ 全部读取 [score=0.854 recalls=0 avg=0.620 source=memory/2026-04-20.md:135-137]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:113:113 -->
- - Candidate: Reflections: No strong patterns surfaced. [score=0.834 recalls=0 avg=0.620 source=memory/2026-04-20.md:98-98]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:132:132 -->
- **结果**: ✅ 已确认 [score=0.834 recalls=0 avg=0.620 source=memory/2026-04-20.md:132-132]

## Promoted From Short-Term Memory (2026-04-26)

<!-- openclaw-memory-promotion:memory:memory/2026-04-21.md:1:1 -->
- [Tue 2026-04-21 09:49 GMT+8] \n\n向量语义搜索需embed,你先不管，我来操作qmd embed生成向量，你只管在需要的时候使用就行了\n\n确认! 我会等您完成 qmd embed 生成向量后，随时协助您使用向量搜索。不需要我主动触发 embed 过程 \u2013 您掌握这个步骤，我只需要在需要时帮您进行语义查询即可。\n\n比如您之后完成 embed 后，可以这样联系我:\n1. 示例查询:\u201c如何优化无头浏览器性能\u201d\n2. 示例领域:\u201c浏览器自动化经验\u201d\n3. 或直接使用您实际需要的搜索关键词\n\n我会处理语义搜索过程。有什么具体搜索需求时再发通知即可。 [score=0.861 recalls=0 avg=0.620 source=memory/2026-04-21.md:1-1]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:141:141 -->
- **1. MEMORY.md 精简经验** [score=0.861 recalls=0 avg=0.620 source=memory/2026-04-20.md:141-141]
<!-- openclaw-memory-promotion:memory:memory/2026-04-20.md:129:129 -->
- **结果**: ✅ 完成 [score=0.840 recalls=0 avg=0.620 source=memory/2026-04-20.md:129-129]

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
