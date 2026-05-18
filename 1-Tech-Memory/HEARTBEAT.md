# HEARTBEAT.md

## 记忆完整性检查（每次心跳执行一次）

1. 获取当天日期 YYYY-MM-DD
2. 检查 `memory/YYYY-MM-DD.md` 是否存在
   - 不存在 → 从当前会话历史中提取关键信息，自动创建并写入（含标准 frontmatter：created/modified/tags: daily-log + tech-agent）
   - 存在但最后更新 > 2小时 → 追加心跳检查标记 `## HH:MM - 💓 心跳检查（无新操作）`
3. 合并当天子记忆文件
   - 扫描 `memory/YYYY-MM-DD*.md`（排除主文件）
   - 将子文件内容按时间顺序融入主文件对应记录中（不加任何分隔标记）
   - 同步到 Obsidian `daily/YYYY-MM-DD.md`
   - 合并完成后立即删除子文件
4. **漏写检测（关键兜底）**
   - 调用 `sessions_list` 获取当天所有活跃 session（`activeMinutes=720`）
   - 对每个 session 调用 `sessions_history`，提取所有用户消息的时间戳
   - 对比 `memory/YYYY-MM-DD.md` 中已记录的时间点
   - 如果发现某个 session 有用户消息但记忆文件中无对应时间段的记录 → 自动补写
   - 补写格式：`## HH:MM - [从session内容推断的主题]`
   - 如果无法推断主题，简写：`## HH:MM - 对话记录（来源：session补录）`
