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

## 📌 核心经验（2026-06-13）

### 闲鱼一键自动发布 — 完全自动闭环
- **执行时间**: 2026-06-13 14:30-15:35
- **成果**: 完全自动闭环发布 3 个商品（¥0.09 / ¥8888 / ¥99999），用户全程无操作
- **核心突破**: `xvfb-run --auto-servernum` 自动创建虚拟 X Server + 设置 DISPLAY → CDP 9222 端口自动监听
- **Session cookies 恢复**: Chrome 重启后 cookie2/XSRF-TOKEN 丢失，通过 CDP `Network.setCookie` 从 `/tmp/xianyu_cookies.txt` 注入恢复
- **图片上传修复**: fetch 返回结构嵌套 `{"object":{"fileId":"xxx"}}`，需取 `data.object.fileId`
- **一键命令**: `bash run.sh --image img.png --desc '描述' --price 99999` 或 `bash run.sh`（读 config.json）
- **脚本位置**: `/home/bill/run.sh`（入口）、`/home/bill/xianyu_start.sh`（Chrome启动）、`/home/bill/xianyu_publish.py`（CDP发布核心）
- **经验文档**: `/home/obsidian_vault/4-Media-Memory/knowledge/xianyu-automation-guide.md`（708行）

### 💡 关键教训
- `sudo bash` 和 `sudo -u bill` 环境下 DISPLAY 变量为空 → Chrome 找不到 X Server → CDP 不通
- `xvfb-run` 是唯一可靠方案：自动设置 DISPLAY + 虚拟桌面
- Session cookies (expires=-1) 在 Chrome 重启后自动清理 → 必须从文件注入恢复
- 闲鱼没有公开的发布 API（测试均返回 404）→ CDP 浏览器自动化是唯一可行方案



## 📌 核心经验（2026-06-12）

### 闲鱼商品发布 — CDP 自动化
- **执行时间**: 2026-06-12 11:20-18:30
- **成果**: 成功发布第1个商品"DeepSeek V4 API 包月畅用"（¥4，已上架）
- **核心突破**: CDP DOM.setFileInputFiles + base64 图片注入绕过 React 事件限制
- **签名算法**: md5(token + "&" + t + "&" + appKey + "&" + dataStr)，已验证
- **第2商品卡点**: React 组件 fileList 状态无法通过 setState 更新，发布 API 调用失败（参数非法）
- **关键标识符**: 上传接口 `stream-upload.goofish.com`，发布 API `mtop.idle.pc.idleitem.publish`

### 无效知识文件根因分析
- **问题**: 4 个无效文件被反复写入 knowledge/ 目录
- **根因**: `sync-daily-to-obsidian.sh` 的 `promote_to_knowledge()` 函数 + cron 每 30 分钟触发
- **教训**: 脚本自动写入 ≠ agent 主动记录；cron 驱动脚本需审查副作用
- **状态**: 4 个文件已删除，脚本修复待确认

### 💡 关键教训
- DOM.setFileInputFiles 无法让 React 识别文件上传（beforeUpload 拦截机制）
- React 组件状态更新需要找到正确的 fiber setState 调用方式
- 签名算法验证通过但 API 参数格式仍需调试

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

