---
tags:
  - openclaw
---

#### sessions 会话
```bash
# 查看活跃会话
openclaw sessions
# 查看所有代理会话
openclaw sessions --all-agents
# 查看指定代理会话
openclaw sessions --agent tech
# Only last 2 hours.
openclaw sessions --active 120
openclaw sessions --json
```

#### cron 定时任务
```bash
# 查看所有定时任务
openclaw cron list
openclaw cron list --json --all

# 编辑定时任务（修改执行时间）
openclaw cron edit --name daily-email-summary --cron "30 9 * * *"

# 删除定时任务
openclaw cron remove --name daily-email-summary

# 创建定时任务：每天9点读取未读邮件并生成汇总
openclaw cron add \
  --name daily-email-summary \
  --cron "0 9 * * *" \
  --message "帮我读取所有未读邮件，汇总发件人、主题和关键信息，生成markdown格式的汇总报告"
```

#### Hook

```bash
# 查看列表和激活状态
openclaw hooks list
```

#### memory 记忆系统
```
# 记忆索引状态
openclaw memory status
# 建索引
openclaw memory index
# 搜索记忆
openclaw memory search
```

#### 聊天
```
# 以tech代理身份开启新聊天
openclaw agent --agent tech --message "醒来"

# 临时指定模型，不修改配置
openclaw agent --model "doubao/doubao-seed-2-0-pro-260215" --message "解释量子计算的原理"

# 使用 Gemini Image
openclaw agent --model "local-google/gemini-3-pro-image" --message "分析这张图片" --image ./photo.jpg
```