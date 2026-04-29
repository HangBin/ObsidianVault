# 系统运维经验 - 问题与解决方案

<!--
来源: MEMORY.md 系统恢复案例、Feishu 配置问题分析
拆分时间: 2026-04-21
用途: main 系统运维经验沉淀
-->

## 🔧 系统恢复案例

### cron 环境未初始化（3-29）
**问题**：cron 目录不存在，每日简报任务瘫痪 24+ 小时

**自主修复过程**：
1. 检测到 cron 目录不存在，任务超时 24h+
2. 根据 HEARTBEAT.md 指令"如果超时，通过 CLI 强制触发"
3. 执行 `mkdir -p ~/.openclaw/cron`
4. 执行 `openclaw cron add ...` 添加每日简报任务
5. 执行 `openclaw gateway restart`（失败但服务仍运行）
6. 验证 `openclaw cron list` - 任务正常，下次运行 in 10m

**结果**：系统调度功能完全恢复，每日简报成功触发

**关键洞察**：
- HEARTBEAT 定时检查 + 自主修复指令 = 系统自愈能力
- 管理员零响应不影响关键功能恢复
- 修复后需验证任务执行状态（不仅检查列表）

---

### 每日简报任务失踪（3-31）
**问题**：cron 任务再次消失，delivery 配置错误

**时间线**：
- 06:21：首次发现并记录
- 08:21：错过 8:00 AM 执行窗口
- 12:02：持续 5 小时 41 分钟仍未修复

**根因**：
- 缺少 cron 任务创建自动化机制
- delivery 配置 `mode: "announce", channel: "last"` 无效

---

## 🧪 Feishu 配置问题分析

**现象**：media/final/proj 在群聊通道持续 timeout，tech 间歇性 timeout

**历史错误记录**：
- 11:46 AM：401 The API key format is incorrect（3 个 agent）
- 14:10-14:22：全员 timeout（包括 tech）

**根因推测**：
1. **Provider 配置绑定错误**：Feishu provider 可能未正确绑定到群聊频道
2. **App 权限不足**：缺少 `chat:read`/`chat:write` 权限
3. **Token 过期或格式错误**：app_id/app_secret 未正确注入

**验证步骤**：
1. 检查 `~/.openclaw/agents/{media,final,proj}/provider/feishu/` 配置
2. 验证环境变量：`env | grep FEISHU_`
3. 确认 Feishu 应用权限勾选了"群聊消息"
4. 尝试通过 direct 会话验证 provider 是否工作

**临时方案**：
- 通过 direct 会话调度（sessionKey: agent:xxx:feishu:direct:ou_xxx）
- 仅限私聊场景，群聊仍需修复

---

## ⚙️ 技术债务（待处理）

| 问题 | 状态 | 备注 |
|------|------|------|
| Media/Proj Feishu credentials 401 | ❌ 未修复 | 持续多日 |
| weekly-backup delivery 400 | ❌ 未修复 | 脚本成功，仅 reporting 失败 |
| maintenance_agent.sh 缺失 | ❌ 未修复 | 备份前置任务跳过 |
| 归纳自动化检查点 | ❌ 未实现 | 依赖人工 |

---

**最后更新：2026-04-21 09:05**
