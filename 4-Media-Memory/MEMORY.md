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

**不重复造轮子**：先读经验文档再动手，不要自己写脚本分析已有方案。发布闲鱼→`run.sh`，发布小红书→`xhs` CLI。

**截图分享流程**：CDP 截图 → HTTP 服务 → `curl -I` 验证 200 → 发链接。不要 OCR 识别后再发。

**路径规范**：统一用 `~` 不要硬编码。读取 knowledge 用 Obsidian 绝对路径。

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
| `xianyu-products/` | 闲鱼商品目录（每个商品独立子目录） |

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
| `xianyu-products/README.md` | 闲鱼商品目录规范（命名、结构、发布流程） |
| `/home/bill/run.sh` | 闲鱼发布脚本（启动→注入Cookie→检查→发布） |
| `/home/bill/extract_xianyu_cookies.py` | Cookies 提取脚本（CDP 优先，SQLite 降级） |
| `strategy/` | 内容策略与样例库（爆款文案、模板） |




## Promoted From Short-Term Memory (2026-06-20)

<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:14:15 -->
- 08:58 - 记忆写入 + 旧文件清理: **触发**: 用户要求写入今天记忆并清理旧文件 **工具**: sessions_list, write, exec, md5sum [score=0.801 recalls=0 avg=0.620 source=memory/2026-06-17.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:17:20 -->
- 08:58 - 记忆写入 + 旧文件清理: **昨日记忆完整性**: 2026-06-16.md 共 10 条记录（09:44→13:36），Obsidian md5 一致; **子文件合并**: 2026-06-16-1336.md → 合并 13:36 记录后删除; **今日记忆文件**: 已创建 2026-06-17.md（frontmatter 完整）; **旧文件清理**: 2026-06-16.md → Obsidian 已同步 → 已删除 [score=0.801 recalls=0 avg=0.620 source=memory/2026-06-17.md:17-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:21:21 -->
- 08:58 - 记忆写入 + 旧文件清理: **决策**: 工作区只允许保留当天文件，昨天文件同步后立即删除 [score=0.801 recalls=0 avg=0.620 source=memory/2026-06-17.md:21-21]

## Promoted From Short-Term Memory (2026-06-22)

<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:24:25 -->
- 09:49 - 闲鱼测试商品批量发布: **触发**: 用户要求启动浏览器、扫码登录、发布xianyu-products里所有测试商品 **工具**: exec(xianyu_start.sh), edit(去掉category字段), exec(run.sh ×2), exec(xianyu_publish.py ×1), sessions_list [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:24-25]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:27:30 -->
- 09:49 - 闲鱼测试商品批量发布: 启动 Chrome → 登录态正常（panbin5218）✅; 修改两个商品 product.json，去掉 category 字段（用户要求不写手机分类）; test-item-001: 商品ID 1057980679964 ✅ 已发布; test-item-002: run.sh 检测为 UNKNOWN → 手动调 xianyu_publish.py → 商品ID 1057981571117 ✅ 已发布 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:27-30]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:31:31 -->
- 09:49 - 闲鱼测试商品批量发布: **决策**: run.sh 检测逻辑在页面跳转后可能返回 UNKNOWN，直接调 xianyu_publish.py 可绕过检测 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:31-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:34:35 -->
- 10:06 - 二维码功能 + 失效状态验证: **触发**: 用户要求验证二维码功能和失效状态处理 **工具**: exec(run.sh --check), exec(pkill+restart), python3(CDP截图+OCR), python3(extract_cookies), python3(失效等待) [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:34-35]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:37:40 -->
- 10:06 - 二维码功能 + 失效状态验证: 二维码截图获取 ✅：CDP + PIL 裁剪 passport iframe 区域放大 3x; OCR 有效性验证 ✅：能识别"手机扫码安全登录"，未检测到"二维码已失效"; 扫码登录 ✅：用户扫码后登录态恢复，panbin5218 + 订单; Cookies 提取 ✅：extract_cookies.py 从 SQLite 提取 20 个 cookies 并保存 [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:37-40]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:41:43 -->
- 10:06 - 二维码功能 + 失效状态验证: 二维码失效检测 ⏳：等待 60 秒未检测到失效（闲鱼二维码有效期 > 60s）; ⚠️ pkill 误杀：重启 Chrome 时 pkill -9 -f google-chrome 误杀了 2 次当前进程; ⚠️ cookies 注入时机：/tmp/xianyu_cookies.txt 不存在时 run.sh 跳过注入，但 Chrome 从 SQLite 自动恢复 [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:41-43]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:44:44 -->
- 10:06 - 二维码功能 + 失效状态验证: **决策**: 更新经验文档 §8 已知限制（新增 pkill 风险、二维码有效期、cookies 注入时机）；§1.3 确认不写 category；§3.2 补充 run.sh UNKNOWN 误判场景 [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:44-44]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:47:48 -->
- 10:06 - cookies 持久化修复 + 闲鱼消息读取 + 经验文档更新: **触发**: 用户指出 cookies 存在 /tmp/ 会丢失、要求验证二维码失效处理、读取闲鱼消息、更新经验文档 **工具**: edit(run.sh COOKIES_FILE), exec(重启Chrome+注入cookies), exec(消息页面截图+DOM), edit(经验文档新增§6消息读取) [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:47-48]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:50:53 -->
- 10:06 - cookies 持久化修复 + 闲鱼消息读取 + 经验文档更新: **cookies 持久化**: run.sh COOKIES_FILE 从 /tmp/xianyu_cookies.txt → /root/.openclaw/workspace-media/.config/xianyu_cookies.txt，重启后注入成功（23个cookies）; **二维码验证**: 截图+OCR+tsv方案验证通过，但60秒内未检测到失效（有效期>60s）；"快速进入"按钮只在有历史登录记录时出现; **闲鱼消息读取**: 通过 goofish.com/im 成功读取6个联系人的消息列表; **经验文档更新**: 新增§6消息读取章节（含步骤、注意事项、验证结果）；更新§1.3不写category、§3.2 cookies路径、§8已知限制 [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:50-53]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:54:54 -->
- 10:06 - cookies 持久化修复 + 闲鱼消息读取 + 经验文档更新: **决策**: cookies 路径已修复；消息读取功能已验证可用；二维码失效检测需要更长时间等待 [score=0.817 recalls=0 avg=0.620 source=memory/2026-06-17.md:54-54]

## Promoted From Short-Term Memory (2026-06-22)

<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:57:58 -->
- 12:38 - "快速进入"按钮验证 + 对话结束: **触发**: 用户要求验证经验文档中点击"快速进入"按钮的可行性 **工具**: exec(导航到登录页), exec(清除cookies), exec(悬停panbin5218→退出登录), python3(截图+OCR+DOM查询) [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:57-58]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:60:63 -->
- 12:38 - "快速进入"按钮验证 + 对话结束: ❌ "快速进入"按钮在所有测试场景中均未出现（已登录、清除cookies、退出登录后）; 原因：该按钮需要 Chrome profile 中有历史登录会话记录，当前环境（Chrome重启+SQLite恢复cookies）不满足条件; 退出登录按钮点击后跳转到个人中心，未真正退出; 经验文档中的技术方案（截图→OCR tsv→模拟点击）本身正确，但需要真实有历史登录记录的环境才能验证 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:60-63]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:64:64 -->
- 12:38 - "快速进入"按钮验证 + 对话结束: **决策**: 不更新经验文档，等"快速进入"按钮出现时再执行验证 [score=0.849 recalls=0 avg=0.620 source=memory/2026-06-17.md:64-64]

## Promoted From Short-Term Memory (2026-06-23)

<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:5:6 -->
- daily-log; media-agent [score=0.891 recalls=0 avg=0.620 source=memory/2026-06-17.md:5-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:7:8 -->
- created: 2026-06-17T08:58:00+08:00 modified: 2026-06-17T08:58:00+08:00 [score=0.891 recalls=0 avg=0.620 source=memory/2026-06-17.md:7-8]
<!-- openclaw-memory-promotion:memory:memory/2026-06-17.md:2:3 -->
- date: 2026-06-17 weekday: Tuesday [score=0.881 recalls=0 avg=0.620 source=memory/2026-06-17.md:2-3]
