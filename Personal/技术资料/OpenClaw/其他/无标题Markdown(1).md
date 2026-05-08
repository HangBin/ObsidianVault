---
tags:
  - openclaw
---

善用Heartbeat做记忆维护

OpenClaw的Heartbeat机制可以定期执行记忆维护任务。比如每天凌晨跑一次：

```bash
openclaw cron add --name "记忆维护"
--cron "0 3 * * *"
--system-event "运行记忆整理：合并相似项，删除低价值项，生成摘要"
```

每日记忆整理反思提炼
```bash
AI提示词：
你帮我写一个定时任务，要求如下：
1.写成openclaw cron add...语法
2.每天23:30执行，如果这段时间关机状态，延后执行，一定要执行一次
3.每次执行成功或者失败要写日志文件，存入本地文件
4.要能给所有代理(main、tech、media、proj、final)都执行
5.实际执行内容如下：
 a.检查并整理每日记忆文件，处理合并多个相同日期的记忆文件。
 b.整理精华到 MEMORY.md
 c.进行自我反思，总结教训和经验到 experience 文件里
 d.持续从 daily logs 和 experience文件里提取新学习点到 .learnings/ 文件中
```

---

可以给 Agent 设置一个简单的自我反思机制。

每天晚上运行一次任务，读取当天的对话，总结经验，然后更新 SOUL 和 USER 文件。这样它会不断修正自己的行为逻辑。

过一段时间，比如一周或者半个月，你还可以让它做一次完整整理。让它读取所有历史聊天记录，然后重新生成 SOUL 和 USER。这样它会形成一套更稳定的行为模式。

---

你把你的MEMORY.md和SOUL.md文件，不需要的、觉得冲突混淆的，告诉我一下，我会让你删除
确认删除 MEMORY.md 中的 6 项内容，同时把SOUL.md按重要优先级重新排版下

---

