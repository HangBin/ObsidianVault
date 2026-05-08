---
tags:
  - openclaw
  - agent
---


#### 路由bindings规则
accountId对应channels里配置的Id
```bash
  "bindings": [
    {
        "agentId": "media",
        "match": {
            "channel": "feishu",
            "accountId": "media"
        }
    },
    {
        "agentId": "tech",
        "match": {
            "channel": "feishu",
            "accountId": "tech"
        }
    },
    {
        "agentId": "main",
        "match": {
            "channel": "feishu",
            "accountId": "main"
        }
    }
  ],
```

#### 通道channels配置(飞书、QQ)
通过通道配置指定agent
```bash
  "channels": {
    "qqbot": {
      "enabled": true,
      "appId": "1903336769",
      "clientSecret": "fGfrpZ6PULzQhlcF",
      "markdownSupport": true,
      "allowFrom": [
        "*"
      ]
    },
    "feishu": {
      "enabled": true,
      "accounts": {
        "main": {
          "agent": "main",
          "appId": "cli_a9279c8b9bf89ccb",
          "appSecret": "tcvms89TXXEBBzsXZrGUXeeM4n4IwigM",
          "enabled": true
        },
        "media": {
          "agent": "media",
          "appId": "cli_a930eb7d21fa5cd3",
          "appSecret": "AbPS1gFyUIcupEWI20mPOtSBeCOFWeVp",
          "enabled": true
        }
      }
    }
  }
```
通过会话路由规则,配置复杂的路由规则


#### 其他设置
```bash
2. 流式回复
openclaw config set channels.feishu.streaming true
作用：开启后,AI回复会像打字一样逐字显示,而不是等全部生成完才一次性输出。
3. 开启耗时显示
openclaw config set channels.feishu.footer.elapsed true
作用：每次回复末尾显示耗时(如"已完成·耗时 1m 54s"),让你清楚知道AI干了多久,心里有数。看着时间,你就知道Token大概烧了多少。钱花在哪,一目了然。
4. 开启状态展示
openclaw config set channels.feishu.footer.status true
作用：显示"已读""正在思考""正在执行"等状态提示,交互更透明,不再对着空气干等。这个挺重要。不然有时候你不知道AI是在思考还是卡死了。
6. 话题独立上下文
openclaw config set channels.feishu.threadSession true
作用：在飞书群聊的话题模式下,每个话题拥有独立上下文,互不干扰,支持多任务并行。这个特别适合团队使用。不同话题讨论不同事情,不会串。
```

