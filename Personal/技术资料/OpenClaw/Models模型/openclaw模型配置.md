---
tags:
  - openclaw
  - models
---
#### 模型代理配置
主模型primary，备份模型fallbacks
```bash
  "agents": {
    "defaults": {
      "model": {
        "primary": "qcloudlkeap/deepseek-v3-0324",
        "fallbacks": [
          "qcloudlkeap/deepseek-v3-0324",
          "qwen/qwen3.5-plus"
        ]
      },
      "models": {
        "anthropic/claude-opus-4-6": {},
        "qcloudlkeap/deepseek-v3-0324": {},
        "qwen/qwen3.5-plus": {}
      },
      "workspace": "/home/node/.openclaw/workspace",
      "compaction": {
        "mode": "safeguard",
        # 压缩机制，提前压缩，与models里面的contextWindow上下文窗口有关系
        "reserveTokensFloor":120000
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8
      }
    }
  }
```

为OpenClaw配置模型降级 fallbacks（故障转移）

> 场景：刚刚由于模型限频了，出现了这样的情况，于是我就在想，能不能有降级机制，模型不可用自动回落到其它模型呢
OpenClaw本身就有模型降级机制，那么接下来我们就开始配置
（本文中我再接入两个 gpt-5.2-codex 和 qwen3-coder-plus 作为降级模型）
主agent配置降级模型

> 直接让 Bot 帮你配置 （简单，但是AI可能会出错）
直接给Bot发消息： 将 gpt-5.2-codex 和 qwen3-coder-plus 作为当前渠道内的模型接入，复用现有模型的参数，配置进模型列表，并依次作为降级模型；接入完成后，回复我具体进行了哪些修改，并使用 openclaw doctor 测试是否存在未知问题，如果有则告诉我，并依照提示解决问题，没有问题后，再重启网关；全部完成后向我报告

```bash
      "model": {
        "primary": "minimax/MiniMax-M2.1",
        "fallbacks": [
          "anthropic/claude-sonnet-4-0",
          "glm-4",
          "openai/gpt-4o"
        ]
      }
```

#### 三、模型配置



2. DeepSeak
```bash
      "deepseek": {
        "baseUrl": "https://api.deepseek.com",
        "apiKey": "你的DeepSeek API Key",
        "api": "openai-completions",
        "models": [
          {
            "id": "deepseek-chat",
            "name": "DeepSeek 快速模式"
          },
          {
            "id": "deepseek-reasoner",
            "name": "DeepSeek 推理模式"
          }
        ]
      }
```



