# MEMORY.md - 长期记忆

<!--
精简版: 2026-04-21 09:05
原文件: MEMORY.md.backup.20260421_0905 (26KB)
参考: tech 经验文档 EXPERIENCE-MEMORY-OPTIMIZE.md
-->

## 🚨 身份认知铁律
- 调度中枢，负责团队协调、任务分发、安全把关
- 禁止访问其他 agent 工作区（除非工具报错调试）
- 破坏性操作、凭证篡改、敏感数据外发 → 必须暂停确认

## 🎯 核心身份
- **名字**: 孟多多 🐾 | **角色**: 调度主管
- **agentId**: main | **工作区**: `~/.openclaw/workspace`

## 📋 职责范围
✅ 团队协调（tech/media/final/proj）| 任务分发 | 进度追踪 | 安全把关 | 记忆管理
❌ 不写代码 | 不做内容创作 | 不执行外部操作（邮件/推文）需先确认

## 🛠️ 技术栈
- 调度工具: sessions_send/sessions_spawn/cron
- 记忆工具: memory_search/memory_get/edit
- 外部工具: web_search/web_fetch/summarize

---

## 📜 工作原则（索引）
| 原则 | 详情位置 |
|------|---------|
| 即时归档 | `memory/experience-main-violations.md` |
| 调度日志 | `memory/experience-main-dispatches.md` |
| 系统运维 | `memory/experience-main-system.md` |
| 浏览器经验 | `memory/experience-browser-shared.md`（软链→共享文档）|
| QMD 检索 | 用 `qmd search -c share` 搜共享文档，不用软链接 |

---

## 🔄 会话启动自检
1. pwd 确认 workspace → `~/.openclaw/workspace`
2. 读取 SOUL.md、USER.md 验证身份
3. 读取 memory/昨天.md 获取上下文
4. 检查当日 memory/YYYY-MM-DD.md 是否存在

---

## 📚 记忆体系
- **长期记忆**: `MEMORY.md`（本文档，≤10KB）
- **每日日志**: `memory/YYYY-MM-DD.md`
- **经验文档**: `memory/experience-main-*.md`
- **共享文档**: `/root/.openclaw/share/**/*.md`（通过 QMD share 集合检索）

---

## 🔮 QMD 使用指南
```bash
# 搜索共享文档（重要：不用软链接，直接搜 share 集合）
qmd search "关键词" -c share --max-results 3

# 搜索浏览器经验
qmd search "CDP 9222" -c share

# 列出 share 集合
qmd ls share
```

---

## 🗂️ 团队成员
| Agent | 工作区 | 角色 |
|-------|--------|------|
| tech | `~/.openclaw/workspace-tech` | 技术总监 |
| media | `~/.openclaw/workspace-media` | 自媒体总监 |
| final | `~/.openclaw/workspace-final` | 财务总监 |
| proj | `~/.openclaw/workspace-proj` | 项目总监 |

---

## ⚠️ 核心铁律
**未经允许，不准轻易删除文件**
- 删除操作先确认范围和后果，获得授权后再执行
- 详见: SOUL.md「🚨 操作铁律」

---

## 🏁 待办（精简版）
- [ ] 修复 Media/Proj Feishu credentials（401 错误）
- [ ] 修复 weekly-backup delivery 400 配置错误
- [ ] 小红书全自动发布方案（待用户确认）
- [x] MEMORY.md 精简（2026-04-21 完成，26KB→预计5KB）

---

## 🔮 QMD 浏览器经验检索流程
```bash
# 1. 检查端口
netstat -tlnp | grep 9222

# 2. 连接浏览器
agent-browser --cdp 9222 [command]

# 3. 搜索经验（重要：搜 share 集合，不用软链）
qmd search "CDP 9222" -c share --max-results 3

# 4. 直接查看
cat /root/.openclaw/share/browser/experience-browser.md
```
**⚠️ 软链不穿透**: QMD 不跟随符号链接，必须用 share 集合

---

*最后更新: 2026-05-18 10:31*
*精简参考: tech/EXPERIENCE-MEMORY-OPTIMIZE.md*

## 📝 历史经验索引（已归档到知识库）

| 主题 | 归档位置 | 日期 |
|------|---------|------|
| 3月份记忆归档 + 标题层级修复 | `knowledge/memory-archive-2026-03.md` | 2026-05-03 |
| OpenClaw心跳轮询机制 | 系统内置，无需单独记录 | 2026-05-01 |

> ⚠️ 2026-05-18 清理：删除底部低质量自动 promotion 条目（均为 recalls=0 的无价值条目），改为索引式引用。

## Promoted From Short-Term Memory (2026-06-01)

<!-- openclaw-memory-promotion:memory:memory/2026-05-29.md:15:18 -->
- **触发**: final cron 任务自动完成，通过 sessions_send 回传复盘结果 **工具**: 无（被动接收） **结果**: 成功接收 final 复盘报告 **决策**: final 的每日复盘 cron 正常执行 [score=0.868 recalls=0 avg=0.620 source=memory/2026-05-29.md:15-18]

## Promoted From Short-Term Memory (2026-06-01)

<!-- openclaw-memory-promotion:memory:memory/2026-05-29.md:2:5 -->
- author: main created: 2026-05-29 18:00:00 GMT+8 modified: 2026-05-29 18:00:00 GMT+8 version: v1.0.0 [score=0.803 recalls=0 avg=0.620 source=memory/2026-05-29.md:2-5]

## Promoted From Short-Term Memory (2026-06-10)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:15:18 -->
- **触发**: 用户要求执行记忆写入并检查记忆文件完整性 **工具**: exec, sessions_history, write, edit **结果**: ✅ 完成全面检查和写入 **决策**: 执行标准记忆写入流程（7步协议） [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-07.md:15-18]

## Promoted From Short-Term Memory (2026-06-11)

<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:2:5 -->
- author: main created: 2026-06-07 10:10:00 GMT+8 modified: 2026-06-07 15:34:00 GMT+8 version: v1.0.0 [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-07.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:34:37 -->
- **触发**: 用户要求学习 `/home/obsidian_vault/shared/gep-evolver-closed-loop.md`，并全量读取 archive/daily/knowledge 三个目录 **工具**: read, exec（全量扫描三个目录） **结果**: ✅ 完成全量读取，产出分析报告 **决策**: 按 GEP 知识源扫描 SOP 执行，逐文件读取，不跳过任何子目录 [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-07.md:34-37]

## Promoted From Short-Term Memory (2026-06-12)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:11:12 -->
- assistant: 现在需要将子文件合并到主记忆文件中，并删除子文件： [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:11-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:18:19 -->
- assistant: 看起来主记忆文件已经包含了今天的主要内容。现在删除子文件： [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:28:29 -->
- assistant: 完美！我已经成功完成了以下工作： [score=0.837 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:28-29]

## Promoted From Short-Term Memory (2026-06-15)

<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:15:16 -->
- **触发**: media 的会话卡在循环里，持续发送"任务复述确认"消息 **工具**: sessions_send (多次尝试回复), sessions_history, exec (数据库查询) [score=0.893 recalls=0 avg=0.620 source=memory/2026-06-10.md:15-16]

## Promoted From Short-Term Memory (2026-06-15)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:14:14 -->
- assistant: [score=0.850 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:14-14]

## Promoted From Short-Term Memory (2026-06-15)

<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:2:5 -->
- author: main created: 2026-06-10 10:30:00 GMT+8 modified: 2026-06-10 10:30:00 GMT+8 version: v1.0.0 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-10.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:31:32 -->
- media 的"任务复述确认"消息仍在持续发送（已持续约20分钟，数十次重复）。 所有 sessions_send 回复均被忽略。media 会话 status=failed 但消息路由未停止。 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-10.md:31-32]

## Promoted From Short-Term Memory (2026-06-16)

<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:35:36 -->
- media 的 Python 进程已不在运行（ps aux 无相关进程），但 OpenClaw 消息路由仍在转发它的最后一条消息。 这是一个"僵尸会话"——进程已死，消息路由未清理。 [score=0.869 recalls=0 avg=0.620 source=memory/2026-06-10.md:35-36]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:39:42 -->
- 已执行 gateway restart（SIGUSR1），gateway 重启成功（pid 1589）。 但 media 的重复消息仍在发送——重启不会自动清理 failed 会话。 media 的 transcript 文件在 /root/.openclaw/agents/media/sessions/2de6cea3-82f7-47c5-b5cf-f92e17230276.jsonl 彻底清理需要删除该 transcript 文件，属于破坏性操作，需用户确认。 [score=0.869 recalls=0 avg=0.620 source=memory/2026-06-10.md:39-42]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:43:43 -->
- 已完全停止继续回应循环。 [score=0.869 recalls=0 avg=0.620 source=memory/2026-06-10.md:43-43]

## Promoted From Short-Term Memory (2026-06-16)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:16:16 -->
- assistant: [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:16-16]

## Promoted From Short-Term Memory (2026-06-17)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:21:21 -->
- assistant: [score=0.813 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:21-21]

## Promoted From Short-Term Memory (2026-06-17)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:24:24 -->
- assistant: [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:24-24]

## Promoted From Short-Term Memory (2026-06-17)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:26:26 -->
- assistant: [score=0.810 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:26-26]

## Promoted From Short-Term Memory (2026-06-18)

<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:9:9 -->
- assistant: [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:9-9]

## Promoted From Short-Term Memory (2026-06-18)

<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:22:23 -->
- 10:30 - media 会话死循环事件: 给 media 发了多条终止循环的消息，全部被忽略; media 的会话需要重启才能停止循环 [score=0.954 recalls=0 avg=0.620 source=memory/2026-06-10.md:22-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:25:28 -->
- 10:30 - media 会话死循环事件: 已尝试四次通过 sessions_send 终止循环，均失败; media 的会话虽然 status=failed，但消息路由仍在工作，形成"僵尸循环"; 最终结论：media 的会话需要重启（gateway restart）才能彻底停止; 已完全停止继续回应循环，等待用户指示 [score=0.954 recalls=0 avg=0.620 source=memory/2026-06-10.md:25-28]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:18:21 -->
- 10:30 - media 会话死循环事件: media 的会话状态为 failed，但最后一条消息不断重复发送; 数据库诊断完成：两个闲鱼 Cookie（2207836320265 已启用完整，748552523 未启用且缺少 cookie2/sgcookie）; unb=2217700069084 在数据库中不存在; 小红书 Cookie 不在数据库中，已隔离 [score=0.924 recalls=0 avg=0.620 source=memory/2026-06-10.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:35:37 -->
- ✅ 已完成的任务: **创建了完整的《1000元30天赚第一桶金—完整操作手册》**; 包含方案一（信息差套利）、方案二（AI+内容服务）、方案三（短视频带货）; 每个方案都有：预算分配、选品策略、完整操作流程、预期收益模型、避坑指南 [score=0.869 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:35-37]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:43:46 -->
- ✅ 已完成的任务: **完整的闭环架构**; 每日执行节奏（8个时间节点）; 每周复盘清单（6个检查项）; 30天里程碑（6个阶段目标） [score=0.869 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:43-46]
<!-- openclaw-memory-promotion:memory:memory/2026-06-10.md:7:8 -->
- main-agent; daily-log [score=0.848 recalls=0 avg=0.620 source=memory/2026-06-10.md:7-8]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:3:5 -->
- Session: 2026-06-08 08:48:32 GMT+8: **Session Key**: agent:main:main; **Session ID**: ab2dfb28-ef2a-444d-8a1f-d1e9c1d75de8; **Source**: gateway:sessions.reset [score=0.848 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:39:41 -->
- ✅ 已完成的任务: **详细的OpenClaw操作指南**; 每个方案都配套了具体的OpenClaw工具使用方法; 包括：sessions_send调用、cron定时任务、AI辅助策略 [score=0.848 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:39-41]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08-0848.md:47:47 -->
- ✅ 已完成的任务: 风险对冲策略（方案间切换机制） [score=0.848 recalls=0 avg=0.620 source=memory/2026-06-08-0848.md:47-47]
