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
- **GEP Evolver**：capability-evolver 技能，52+ 基因，自动进化闭环（2026-06-06 学习）

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

### ⚠️ 软链接（Symlink）须知
以下工作区 `memory/` 下的目录是软链接，指向 Obsidian vault。**写入时两个位置自动同步，读取时用绝对路径。**

| 工作区路径 | → Obsidian 路径 |
|------------|------------------|
| `memory/daily` | `/home/obsidian_vault/4-Media-Memory/daily/` |
| `memory/knowledge` | `/home/obsidian_vault/4-Media-Memory/knowledge/` |
| `memory/archive` | `/home/obsidian_vault/4-Media-Memory/archive/` |
| `MEMORY.md` | `/home/obsidian_vault/4-Media-Memory/MEMORY.md` |

**关键规则**：
- 读取经验文档用 Obsidian 绝对路径：`/home/obsidian_vault/4-Media-Memory/knowledge/xxx.md`
- **不要只用工作区相对路径读 knowledge/，软链接部分工具解析会异常**
- 写入 `memory/YYYY-MM-DD.md` 后必须双写 Obsidian `daily/YYYY-MM-DD.md`

| 路径 | 说明 |
|------|------|
| `/home/obsidian_vault/4-Media-Memory/MEMORY.md` | 长期记忆 |
| `/home/obsidian_vault/4-Media-Memory/daily/` | 历史每日日志 |
| `/home/obsidian_vault/4-Media-Memory/knowledge/` | 专项经验文件 |
| `/home/obsidian_vault/4-Media-Memory/archive/` | 归档文件 |
| `~/.openclaw/workspace-media/memory/YYYY-MM-DD.md` | 当日日志（工作区保留） |

---

## 📂 可用参考文档

| 文件路径 | 用途 |
|---------|------|
| `SOUL.md` | 操作规范源头（铁律、清单、流程） |
| `IDENTITY.md` | 身份快照（职责、风格、边界） |
| `AGENTS.md` | 团队边界与协作原则 + 对话结束协议 |
| `.learnings/LEARNINGS.md` | 结构化学习条目（最佳实践、原则） |
| `.learnings/ERRORS.md` | 错误与修复记录 |
| `.learnings/FEATURE_REQUESTS.md` | 功能需求与改进建议 |
| `/home/obsidian_vault/4-Media-Memory/knowledge/xianyu-automation-guide.md` | **闲鱼自动化经验指南** ⭐ |
| `/home/obsidian_vault/4-Media-Memory/knowledge/xhs-publish-guide.md` | **小红书发布经验指南** |
| `/home/obsidian_vault/4-Media-Memory/knowledge/experience.md` | **经验沉淀**（团队成立、规范、踩坑） |
| `/home/obsidian_vault/shared/experience-archive.md` | **日志归档规范**（目录规则、操作流程、8条教训） |
| `strategy/` | 内容策略与样例库（爆款文案、模板） |

---

---

## 📌 核心经验

### 闲鱼自动化发布（2026-06-12 → 06-13 → 06-15）
- **当前方案**: `bash /home/bill/run.sh --image ... --desc ... --price ...` 一键发布
- **核心突破**: `xvfb-run --auto-servernum` 自动创建虚拟 X Server → CDP 9222 端口监听
- **登录态管理**: run.sh 自动从 `/tmp/xianyu_cookies.txt` 注入 session cookies；过期时截图二维码让用户扫码
- **图片上传**: fetch 上传 + React fiber onChange 注入（三步法）
- **已验证商品**: DeepSeek V4 API (¥4)、Claude Opus 4.8 (¥0.09)、MacBook Pro M4 (¥8888)、周杰伦签名专辑 (¥888,888)
- **经验文档**: `/home/obsidian_vault/4-Media-Memory/knowledge/xianyu-automation-guide.md`
- **踩坑**: sudo 环境 DISPLAY 为空 → xvfb-run 是唯一方案；session cookies 重启后丢失需注入；fiber 树深度 71 层不要自己写遍历

### 小红书发布（2026-06-10）
- **方案**: `xhs` CLI / Python API（Cookie: a1 + web_session）
- **经验文档**: `/home/obsidian_vault/4-Media-Memory/knowledge/xhs-publish-guide.md`
- **踩坑**: read 必须加 `--xsec-token`；Cookie 路径是 `~/.xiaohongshu-cli/cookies.json` 不是 `.config/`

### 记忆体系与规范（2026-04-20 → 04-24）
- **MEMORY.md 精简**: 21.7KB → 2.9KB（-86%），核心规则保留，操作外移到知识库
- **软链接**: `memory/daily`、`memory/knowledge`、`memory/archive`、`MEMORY.md` → Obsidian vault
- **即时记录铁律**: 每次工具调用后立即写入 daily log，禁止堆积
- **截图分享流程**: CDP 截图 → HTTP 服务 → curl 验证 200 → 发链接
- **QMD 搜索**: `qmd search "关键词" -c share/knowledge/daily --max-results 5`

### 💡 通用踩坑
- 文档有明确步骤但没执行到位，比不知道更严重（明知故犯）
- 分享前必须验证链接 200
- 路径统一用 `~` 不要硬编码
- **先读经验文档再动手，不重复造轮子**

