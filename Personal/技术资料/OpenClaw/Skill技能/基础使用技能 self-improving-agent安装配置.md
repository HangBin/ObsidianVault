---
tags:
  - openclaw
  - skill
---
为 OpenClaw 提供三种长期记录能力：

- 错误记录
- 经验学习
- 功能需求记录

> 工作原理：什么时候会触发记录？当被错误、纠正或功能缺失等事件触发时，Skill 会将格式化的条目写入对应的日志文件。

> 学习记录的"晋升"路径: 当某条记录被反复验证、具有广泛适用性时，可以将其从 .learnings/ 目录提取出来，晋升到中央项目文件中，使其在所有会话中持久化生效。

> 学习类型 晋升到 示例 行为模式 SOUL.md "保持简洁，避免免责声明" 工作流改进 AGENTS.md "长任务时派生子 Agent" 工具注意事项 TOOLS.md

目录结构
- 需要确保在~/.openclaw/skills/目录下存在self-improving-agent的文件夹
- 包含必要的文件如SKILL.md等。

创建日志文件

```bash
# 利用self-improving-agent已有目录
cp -r ~/.openclaw/skills/self-improving-agent/.learnings ~/.openclaw/workspace
# 三个文件各司其职：
# LEARNINGS.md 用户纠正、知识缺口、最佳实践、经验沉淀
# ERRORS.md 命令失败、异常报错、API 调用失败 
# FEATURE_REQUESTS.md 收集用户提出的改进建议
```

Hook安装配置

可能需要安装和启用Hook来自动触发记录功能，例如使用 openclaw hooks enable self-improvement。

```bash
# 复制 hook 到 OpenClaw hooks 目录 
mkdir -p ~/.openclaw/hooks/self-improvement
cp -r ~/.openclaw/skills/self-improving-agent/hooks/openclaw ~/.openclaw/hooks/self-improvement
# 启用Hook（自动记录）
openclaw hooks enable self-improvement

# Hook目录结构修正
~/.openclaw/hooks/self-improvement/  # 根目录必须与Hook名称一致
├── HOOK.md        # 元数据文件（必须存在）
├── handler.ts     # TypeScript处理程序（官方推荐）
└── handler.js     # JavaScript备用（仅当无TS时使用）

mv ~/.openclaw/hooks/self-improvement/openclaw/* ~/.openclaw/hooks/self-improvement/
rmdir ~/.openclaw/hooks/self-improvement/openclaw  # 删除冗余目录
```

验证Hook激活

```bash
openclaw hooks list | grep self-improvement
# 应显示：self-improving-agent (vX.X.X) [ENABLED]
```

验证安装成功

直接让 Agent 自检：
```text
我刚安装了 self-improving-agent skill，请帮我确认： 1. .learnings 目录是否配置正确 2. 三个日志文件是否存在 3. 尝试记录一条测试学习 
```
如果一切正常，Agent 会在 LEARNINGS.md 中写入一条测试记录，你可以打开文件确认。


#### 每天自动复盘

另外，为了最后增加一个兜底的机制，我让 OpenClaw 设置了一个定时任务：每天凌晨 4 点自动进行一次自我反思。

放在凌晨 4 点考虑这个时间是资源最空闲的时候。

#### 配置 Hook 触发器（可选，进阶）
Hook 可以启用自动提醒功能。这是可选的 —— 你必须显式配置。

基础配置（用户每次提交 prompt 时触发）：
```bash
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improvement/scripts/activator.sh"
          }
        ]
      }
    ]
  }
}
```

进阶配置（额外监听 Bash 工具调用，自动检测错误）：
```bash
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improvement/scripts/activator.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./skills/self-improvement/scripts/error-detector.sh"
          }
        ]
      }
    ]
  }
}
```

说明：PostToolUse + matcher: "Bash" 的组合意味着每次 Agent 执行完 Bash 命令后，都会自动检查是否有错误需要记录。这对捕获命令行报错非常有效。




## Self-Improvement 机制详解

**工作机制**

`.learnings/` 是 **self-improving-agent skill** 的核心日志系统，分为三个文件：

| 文件                  | 用途           | 触发条件                         |
| --------------------- | -------------- | -------------------------------- |
| `LEARNINGS.md`        | 经验与最佳实践 | 用户纠正、发现更好方案、知识更新 |
| `ERRORS.md`           | 错误与失败     | 命令失败、异常、工具报错         |
| `FEATURE_REQUESTS.md` | 功能请求       | 用户提出新需求                   |

**自动捕获的6种场景**（根据 SKILL.md）:

1. 用户纠正你（"No, that's wrong..."）
2. 命令/操作失败
3. 用户请求不存在的功能
4. 外部 API/工具失败
5. 发现知识过时或不正确
6. 发现更好的方法（优化现有流程）

**何时会写入 `.learnings/`？**

| 你的行为                      | 触发文件                       | 例子                 |
| ----------------------------- | ------------------------------ | -------------------- |
| 用户说"你刚才错了，应该是..." | `LEARNINGS.md` (correction)    | 纠正 API 用法错误    |
| `exec` 命令报错退出           | `ERRORS.md`                    | `npm install` 失败   |
| 用户要求"能不能自动..."       | `FEATURE_REQUESTS.md`          | 请求自动格式检查     |
| 你发现之前文档写错了          | `LEARNINGS.md` (knowledge_gap) | 更新过时的配置方法   |
| 找到更优的流程                | `LEARNINGS.md` (best_practice) | 优化 Docker 构建参数 |



