---
tags:
  - ai
  - Claude
  - mcp
  - Skill
  - 安装配置
---
### 一、安装

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

### 二、配置国产模型
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

### 三、MCP(Model Context Protocol)
Claude Code去连接外部工具的一个接口

MCP market资源网站：`https://mcpmarket.com/zh`

1. `Playwright` 控制浏览器
	通过命令安装: `claude mcp add playwright npx @playwright/mcp@latest`

### 四、Skill
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

### 五、内置命令
#### 1.会话控制
- `/clear` 清空上下文
- `/resume` 可以找到之前所有的历史对话
- `/rewind` 回到对话中的之前某个点
- `/export` 一导出对话数据
- `/context` 查看当前上下文占用情况
- `/goal` 设定一个目标，让 AI 自己一轮接一轮地干，直到干完为止，不用你每轮都点确认。
	使用方式：`/goal` 修复登录页的接口对接，要求测试通过、构建成功，🎯 设置目标，立即开始
	适合场景：修复 bug（有明确报错）、跑测试直到全部通过、迁移 API（有构建验证）

#### 2.模型和使用情况
- `/model` 显示或切换当前Claude模型
- `/cost` 查看当前会话的费用估算
- `/usage` 查看模型和费用使用概览
- `/extra-usage` 查看详细的使用数据明细
#### 3.项目设置
- `/init` 在目录中初始化Claude code
- `/memory` 配置或查看项目记忆
- `/add-dir` 索引额外的项目自录
- `/config` 查看或更新配置设置
#### 4.代码操作
- `/diff` 显示相对于代码库的当前更改
- `/security-review` 对代码进行安全分析
- `/plan` 先规划，生成项目或任务计划
- `/permissions` 管理文件读/写权限
- `/compact` 压缩项目数据以提供上下文
#### 5.智能体层
- `/agents` 列出可用的专用智能体
- `/skills` 查看所有安装的Skills
- `/plugin` 管理系统插件
- `/mcp` 可以查看所有我们安装的MCP
- `/reload-plugin` 重新加载已安装插件
#### 6.其他命令
- `@` 可以选择一个工作目录下的文件，比如之前生成的Markdown文件
- 双击esc 后悔药，直接回到上一个检查点
- Ctrl+R 翻旧旧账。昨天的提示词忘了?按Ctrl+R秒速搜索历史对话，比翻记事本快
- !直接运行命令 输入 !git status 或 Inpm test结果直接进上下文，不用来回切终端
- Ctrl+G 打开你的默认编辑器，像vim、vscode都行，保存退出内容自动提交给claude。一般用来粘贴大段报错信息
- `/btw` 长对话里，有时候你想问个一次性的问题。
- `/copy` 输入/copy会复制最后一条回复

Memory Updates 智能记忆
告诉Claude:"记住我用bun不用npm"它会自动记在CLAUDE.md里下次自动用对命令，不打断心流

Remote 随时随地接力。网页版开始写代码，回家接着写
用 claude --teleport 把云端会话"拉"到本地，无缝切换设备

Ctrl+s 暂存想法
打字打到一半想看别的?按Ctrl+S暂存当前提示词准备好了自动恢复，不用复制到记事本

会话随时恢复
电脑没电了?终端意外关闭?输 claude --continue 瞬间恢复上下文完美保留，工作流永不丢失

### 提示词
- 用playwright mcp 打开百度，搜索“什么是mcp”，并且选两篇优质搜索结果，打开并阅读，把结果保存到本地的一个 markdown 文件
- 根据 @什么是MCP_搜索结果汇总.md ，使用 hyperframes skills，制作 10s 的科普视频，dark mode，网格背景，有动画演示其原理



### 
#### 核心功能实战指南

拖拽文件直接分析，支持 PDF、Excel、Markdown、纯文本、代码文件等本地文件 —— 拖进对话框就能开始互动。

> 请总结这份 PDF 的第三章，并提取所有专业术语作为术语表

Claude 会结构化输出重点内容 + 专业提取，适合做读书笔记、学术资料整理等。如图所示：

![59f74c1b708eb59ab735bb4a231f35ca.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6db9e70ef8fc49bfa21dc07d6d8467e9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Yqq5Yqb55qE5bCP6Zuo:q75.awebp?rk3s=f64ab15b&x-expires=1776068774&x-signature=G8d4LrSw0IVuiJDOENp7WHG0q8M%3D)

> 写一个 Python 爬虫，抓取豆瓣电影 Top250 的标题和评分，保存成 CSV 文件

Claude 会返回完整代码 + 所需依赖库，连安装命令都一并生成。如图所示：

![f0452f070133aa15a23fe221f8d601a9.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/263d938d5a8943aca9800413058a1945~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Yqq5Yqb55qE5bCP6Zuo:q75.awebp?rk3s=f64ab15b&x-expires=1776068774&x-signature=tPfinfAnJ%2FaFFzM875F9HQN5xYc%3D)


## 总结

Claude Desktop 本质上是把 Claude 从网页端“请回”到你的桌面，让它离你的文件、任务、习惯更近了一步。不论是代码生成、文档提炼、对话总结，还是通过 MCP 动手操作本地文件，它都能成为你真正的「全能助手」。

一句话总结：

> 下载、配置、熟练用三招，Claude Desktop 就能从聊天工具变成你的高效工作台。

下一步建议：

- 把常用文件拖进去试试 Claude 的理解能力
- 创建一个 Prompt 收藏夹，从模板到自动化场景一步步走起来
- 定期整理 MCP 指令，形成你自己的“AI 工具流”



### CLAUDE.md
是Agent每次开工前,都会读一遍的规则文件
![[Pasted image 20260512213634.png]]




### 配置

1. 地区限制
	运行命令`notepad.exe .\.claude.json`，打开Claude Code的配置文件
	添加`"hasCompletedOnboarding": true`，保存并且关闭，绕过软件对地区的检测
2. 修改Claude code默认的权限模式
	AI每运行一条命令，都需要我批准它才能继续执行，这是Claude code默认的权限模式

