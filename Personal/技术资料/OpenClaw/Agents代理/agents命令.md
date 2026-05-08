---
tags:
  - openclaw
  - agent
---
代理
```bash
# 查看代理：管理代理工作区workspace、工具和身份
openclaw config get agents
# 查看代理列表
openclaw agents list
# 查看绑定规则 bindings
openclaw agents list --bindings

# 删除代理
openclaw agents delete developer

# 查看代理状态
#openclaw agents status work

openclaw channels status
openclaw channels status --probe
```

新增代理
```bash
# 添加新代理
openclaw agents add developer

# 指定workspace和model
openclaw agents add developer --workspace ~/.openclaw/workspace-developer
openclaw agents add developer --workspace ~/.openclaw/workspace-developer --model doubao/doubao-seed-2-0-pro-260215
```

