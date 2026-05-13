---
tags:
  - ai
  - DeepSeek
---
开发平台 `https://platform.deepseek.com/usage`

聊天 `https://chat.deepseek.com/a/chat/s/184a5015-b899-46eb-a021-a7f5f7220082`

账号信息

```
base_url = "https://api.deepseek.com"
api_key = "sk-eb8b3474e89746a59f972de859ad15ba"
```

Temperature 设置 temperature 参数默认为 1.0。

我们建议您根据如下表格，按使用场景设置 temperature。

如未指定 max_tokens，默认最大输出长度为 4K。请调整 max_tokens 以支持更长的输出。

|场景|温度|
|---|---|
|代码生成/数学解题|0.0|
|数据抽取/分析|1.0|
|通用对话|1.3|
|翻译|1.3|
|创意类写作/诗歌创作|1.5|

#### [](#api)api

对话补全 `https://api.deepseek.com/chat/completions` 根据输入的上下文，来让模型补全对话内容。