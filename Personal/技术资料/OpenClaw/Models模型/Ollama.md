
接入本地Ollama配置的openclaw.json示例

```bash
      "ollama": {
        "baseUrl": "http://192.168.1.3:11434",
        "apiKey": "ollama-local",  // 任意非空值
        "api": "openai-completions",  // 兼容OpenAI格式
        "models": [
          {
            "id": "qwen3:8b",  // 本地模型名称
            "name": "qwen3:8b",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 131072,  // 上下文窗口大小
            "maxTokens": 8192
          }
        ]
      }
```

验证命令：curl http://localhost:11434/api/tags（应返回模型列表）


```bash
# 测试模型调用
curl -X POST http://192.168.1.210:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "ollama/gemma4:e2b", "messages": [{"role": "user", "content": "你好"}]}'
```



```
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3:8b"  // 默认模型
      }
    }
  },
  "tools": {
    "web": {
      "search": {
        "enabled": false  // 禁用网络搜索
      },
      "fetch": {
        "enabled": true  // 启用本地资源获取
      }
    }
  }
```
