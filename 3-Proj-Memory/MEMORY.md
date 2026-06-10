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


## Promoted From Short-Term Memory (2026-05-20)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:10:13 -->
- **触发**: 大梦要求学习 `/root/.openclaw/share/memory-auto-write-optimization.md` 并更新 proj 核心文件 **工具**: read, edit, write **结果**: 成功更新 4 个核心文件 **决策**: 按共享文档 v1.5 的四重机制方案全面升级记忆体系 [score=0.802 recalls=0 avg=0.620 source=memory/2026-05-18.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:26:29 -->
- **触发**: 大梦指出 2026-05-18.md 缺少 frontmatter **工具**: edit, exec **结果**: 已补全 frontmatter（created/modified/tags），同步到 Obsidian **决策**: 创建 daily log 时必须包含标准 frontmatter，这是对话结束协议第1步的要求 [score=0.802 recalls=0 avg=0.620 source=memory/2026-05-18.md:26-29]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:32:35 -->
- **触发**: 大梦要求将 frontmatter 规范固化到核心文件，避免再犯 **工具**: read, edit **结果**: 已更新 AGENTS.md（对话结束协议第1步扩展 frontmatter 模板）和 SOUL.md（检查清单第①项扩展完整格式） **决策**: 教训必须固化到规则文件，不能只靠"记住" [score=0.802 recalls=0 avg=0.620 source=memory/2026-05-18.md:32-35]

## Promoted From Short-Term Memory (2026-05-21)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:38:40 -->
- **触发**: 大梦指出 MEMORY.md 不应追加到末尾，应直接修改对应章节 **工具**: read, edit **结果**: 完成 MEMORY.md 结构重组 [score=0.836 recalls=0 avg=0.620 source=memory/2026-05-18.md:38-40]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:2:4 -->
- created: 2026-05-18 12:09 GMT+8 modified: 2026-05-18 12:36 GMT+8 tags: [proj-agent, daily-log, 2026-05-18] [score=0.804 recalls=0 avg=0.620 source=memory/2026-05-18.md:2-4]
<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:49:51 -->
- **触发**: 大梦要求归档4月日志 **工具**: read, write, exec, edit **结果**: 完成2026-04月度归档 [score=0.804 recalls=0 avg=0.620 source=memory/2026-05-18.md:49-51]

## Promoted From Short-Term Memory (2026-05-21)

<!-- openclaw-memory-promotion:memory:memory/2026-05-18.md:59:62 -->
- **触发**: 大梦要求执行对话写入 **工具**: exec, read, edit **结果**: 完成记忆写入，修复重复记录 **决策**: 发现12:21记录重复，已清理 [score=0.804 recalls=0 avg=0.620 source=memory/2026-05-18.md:59-62]

## Promoted From Short-Term Memory (2026-06-09)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:10:13 -->
- **触发**: 大梦要求执行记忆写入并检查记忆文件完整性 **工具**: exec, read, write, edit **结果**: 完成记忆文件创建、子文件检查、历史文件清理 **决策**: 按对话结束协议7步执行 [score=0.802 recalls=0 avg=0.620 source=memory/2026-06-07.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:34:37 -->
- **触发**: 大梦要求学习 GEP 共享经验文档，并全量读取所有知识源目录 **工具**: read, exec (find + head) **结果**: 完成 GEP 架构理解 + 全量文件扫描 **决策**: 按 GEP 知识源扫描 SOP 逐文件读取，不遗漏 [score=0.802 recalls=0 avg=0.620 source=memory/2026-06-07.md:34-37]

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:63:66 -->
- **触发**: 大梦要求固化 proj 基因 **工具**: write, exec **结果**: 完成 proj scope 基因库创建（21个基因） **决策**: 基于全量知识源扫描结果，从 MEMORY.md/experience.md/daily logs/archive 中提炼 [score=0.873 recalls=0 avg=0.620 source=memory/2026-06-07.md:63-66]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:2:4 -->
- created: 2026-06-07 10:09 GMT+8 modified: 2026-06-07 10:10 GMT+8 tags: [proj-agent, daily-log, 2026-06-07] [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-07.md:2-4]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:24:27 -->
- | 文件 | 操作 | 原因 | |------|------|------| | memory/2026-05-18.md | 删除 | Obsidian 已同步 | | memory/2026-05-18-1239.md | 删除 | 子文件，内容已融入主文件 | [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-07.md:24-27]

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:41:44 -->
- | 目录 | 文件数 | 读取方式 | |------|--------|---------| | shared/ (GEP经验) | 1 | 全文读取 | | 3-Proj-Memory/ 根目录 | 4 | 全文读取 | [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-07.md:41-44]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:45:48 -->
- | daily/ | 5 | 全文读取 | | knowledge/ | 2 | 全文读取 | | archive/ 根目录 | 2 | 全文读取 | | archive/history-2026-03/ | 3 | head 摘要 | [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-07.md:45-48]

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:49:52 -->
- | archive/history-2026-04/ | 19 | head 摘要 | | memory/dreaming/ | 126 | 目录扫描 | | memory/.dreams/ | 7 | 目录扫描+行数统计 | | memory/evolution/ | 0 | 空目录 | [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-07.md:49-52]
