---
tags:
  - openclaw
  - skill
---

**free-ride**(白嫖神器) 整理OpenRouter免费模型欠费自动切换免费模型。

任务不中断
注意:须照说明手动配置

相关文档：
- [Free Ride Skill 深度介绍](https://blog.csdn.net/weixin_45092204/article/details/158731138)

安装技能
```bash
npx clawhub@latest install freeride
cd ~/.openclaw/workspace/skills/free-ride
pip install -e .
```

第二步：配置 OpenRouter API Key

前往 openrouter.ai/keys 免费获取一个 API Key，然后：
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
# 或者持久化保存：
openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
```

第三步：一键启用免费 AI
```
freeride auto
openclaw gateway restart
```

聊天窗口可查看状态```/status```

其他
```
| `freeride auto` | Auto-configure best model + fallbacks |
| `freeride list` | See all 30+ free models ranked |
| `freeride switch <model>` | Use a specific model |
| `freeride status` | Check your current setup |
| `freeride fallbacks` | Update fallbacks only |
| `freeride refresh` | Force refresh model cache |
```

```
# Already have a model you like? Just add fallbacks:
freeride auto -f

# Want more fallbacks for maximum uptime?
freeride auto -c 10

# Coding? Switch to the best coding model:
freeride switch qwen3-coder
```

