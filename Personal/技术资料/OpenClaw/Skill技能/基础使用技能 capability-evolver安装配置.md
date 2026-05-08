---
tags:
  - openclaw
  - skill
---

### 背景

不是OpenClaw不聪明，是它没有"成长"的机制。每次对话结束，经验清零，下次从头来。

capability-evolver 做的就是这件事：让 AI 分析自己的历史表现，找出哪里做得不好，然后修改自己的行为规则，下次做得更好。

### 🔧 技能功能
根据文档，这是一个自我进化引擎，主要功能包括：

- 运行时分析 - 分析历史执行记录
- 改进识别 - 自动识别能力增强机会
- 协议约束应用 - 遵循受限的进化协议
- 持续优化 - 自动应用改进策略

### 安装

```clawhub install capability-evolver```

### 配置
```bash
  "skills": {
    "entries": {
      "capability-evolver": {
        "enabled": true
      }
    }
  }
```
