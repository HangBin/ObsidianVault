---
tags:
  - openclaw
  - agent
---

新增绑定规则 bindings
```bash
# 先查看导出当前配置
openclaw config get bindings > /tmp/bindings-backup.json
# 追加一条飞书群组绑定
openclaw config set --json bindings '[ 原有绑定..., 新的飞书绑定 ]'
```

为多个群组配置不同 Agent
```bash
# 在 bindings 中添加多个群组绑定；
openclaw config set --json bindings '[
  {
    "agentId": "feishu-writer",
    "match": {
      "channel": "feishu",
      "peer": {
        "kind": "group",
        "id": "oc_e4dfb35658c81ce5100add124c3592a8"
      }
    }
  }
]'
#  groupAllowFrom 中添加多个会话 ID。
openclaw config set --json channels.feishu.groupAllowFrom '[
  "oc_e4dfb35658c81ce5100add124c3592a8"
]'
```


实现单Bot与Agent的绑定
```bash
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu", 
        "accountId": "cli_a9279c8b9bf89ccb"
      }
    }
  ]
```
或者通过“群聊/私聊匹配”实现同一Bot路由到不同Agent
```bash
    {
      "agentId": "media",
      "match": {
        "channel": "feishu",
        "peer": {
          "kind": "group",
          "id": "oc_02bb0bb304c8dec979632ac0f122e7af"
          }
        }
    }
```
