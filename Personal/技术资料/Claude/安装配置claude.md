---
tags:
  - ai
  - Claude
  - mcp
  - Skill
---
### 安装

#### 1. PowerShell 原生安装(官方推荐)

```powershell 
irm https://claude.ai/install.ps1 | iex
```

#### 2. CMD 原生安装
```cmd
curl -fsSL https://claude.ai/install.cnd -o install.cmd && install.cmd && del install.cmd
```

#### 3. npm全局究装
```bash
npm install g anthropic-ai/claude-code
```

#### 4.WSL 里安装
```bash
curl -fsSl https://claude.ai/install.sh l bash
```

#### 5. WinGet安装
```powershell 
winget install Anthropic.ClaudeCode
```
下载完成后，运行'claude'可看到启动界面

不同的源下载和安装，大部分在国肉网络，环境运行是会失败的
可以在国内环境下载安装claude code的命令，WinGet安装方式

### 配置国产模型
运行命令`notepad.exe .\.claude.json`，打开Claude Code的配置文件
添加`"hasCompletedOnboarding": true`，保存并且关闭，绕过软件对地区的检测
按两次`ctrl+C`可以关闭claude，回到正常的命令界面

#### 1. 配置kimi
添加一段配置，用来指定它使用的模型
```bash
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.moonshot.cn/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-GhquKR7fGn9ETwsD8lOlswnJPdn1oVUZKlScBJVCfcG9w6vG",
    "ANTHROPIC_MODEL": "kimi-k2.6"
  },
```
#### 2. 配置OpenRouter

设置环境变量 $env:OPENROUTER_API_KEY="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"

使用 Claude（通过 OpenRouter）
claude --api-url https://openrouter.ai/api/v1 "你是什么模型？"

### MCP
Claude Code去连接外部工具的一个接口

MCP market资源网站：`https://mcpmarket.com/zh`

1. `Playwright` 控制浏览器
	通过命令安装: `claude mcp add playwright npx @playwright/mcp@latest`

### Skill
给Claude Code装的一个现成的能力包。让AI能够连接外部服务，同时预设了大量的提示词，用来知道AI如何完成某一特定工作
skill资源网站：`https://skillhub.cn/`

- `Hyperframes` 通过编程来剪辑视频的Skills
	通过命令安装：`npx skills add heygen-com/hyperframes`


`安装这个skill，skill项目地址为: https://github.com/anthropics/skills/tree/main/skills/skill-creator`

可以直接让Claude Code读取下面这两个链接里所有的Skills，然后告诉它你的需求，让它帮你看看社区里有没有已经造好的轮子。
```
读取下面网页里面所有的 Skills，当我给你提出我的需求之后，匹配最合适的，并且返回它的链接。  
https://github.com/anthropics/skills

https://github.com/ComposioHQ/awesome-claude-skills
```

### 内置命令
- `@` 可以选择一个工作目录下的文件，比如之前生成的Markdown文件
- `/resume` 可以找到之前所有的历史对话
- `/context` 查看当前上下文占用情况
- `/compact` 总结前面所有的对话，释放掉大部分上下文
- `/clear` 清空上下文
- `/mcp` 可以查看所有我们安装的MCP
- `/skills` 查看所有安装的Skills

### 提示词
- 用playwright mcp 打开百度，搜索“什么是mcp”，并且选两篇优质搜索结果，打开并阅读，把结果保存到本地的一个 markdown 文件
- 根据 @什么是MCP_搜索结果汇总.md ，使用 hyperframes skills，制作 10s 的科普视频，dark mode，网格背景，有动画演示其原理

### CLAUDE.md
是Agent每次开工前,都会读一遍的规则文件
![[Pasted image 20260512213634.png]]




### 配置

1. 地区限制
	运行命令`notepad.exe .\.claude.json`，打开Claude Code的配置文件
	添加`"hasCompletedOnboarding": true`，保存并且关闭，绕过软件对地区的检测
2. 修改Claude code默认的权限模式
	AI每运行一条命令，都需要我批准它才能继续执行，这是Claude code默认的权限模式


权限模式
- default 默认模式;基本是只读操作直接执行，其他操作会询问
- acceptEdits 自动接受文件编辑和常见文件系统命令
 - plan 只分析、读文件、写计划，不改代码
- auto 自动执行大多数操作，但带后台安全检查
- dontAsk 不会弹确认框;只有预先批准的工具才能用
- bypassPermissions 跳过几乎所有权限检查，最激进

`claude -permission-mode bypassPermissions`
或: `claude --dangerously-skip-permissions`
或设: `"defaultMode":"bypassPermissions"`
