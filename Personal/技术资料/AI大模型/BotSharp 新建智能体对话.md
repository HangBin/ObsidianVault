---
tags:
  - ai
  - agent
  - BotSharp
---
# AI智能体第一谈，关于BotSharp浅浅入门

.NET9 作为与时俱进全新的跨平台版本，更深层次的支持了各类生成式 AI。[为.NET](http://xn--siq.NET) 生态又增添了活力。

下面是笔者关于入门 BotSharp 的小经验，希望能帮到大家。

## [](#第一部分-botsharp-入门教程)第一部分 BotSharp 入门教程：

### [](#11-botsharp-介绍)1.1 BotSharp 介绍

BotSharp [是一个基于.NET](http://xn--4gqvdonr53ar0r.NET) 框架开源的智能对话平台，专为开发人员提供灵活、可定制且易于扩展的聊天机器人开发框架。它支持多种自然语言处理模型，并结合机器学习和深度学习技术，帮助开发者轻松构建与用户进行交互的智能对话系统[1]。

### [](#12-配置项目)1.2 配置项目

#### [](#1后端部分)1).后端部分

笔者使用的是星火 API 中的 Spark Max 大模型

首先配置 WebStarter项目中的 appsettings.json 文件

```
"LlmProviders": [
    {
      //讯飞模型
      "Provider": "sparkdesk",
      "Models": [
        {
          "Name": "Max",
          "Type": "chat",
          "PromptCost": 0.0015,
          "CompletionCost": 0.002
        }
      ]
    }
  ],
  //讯飞模型
  "SparkDesk": {
    "AppId": "d087ba3a",
    "ApiKey": "92ae8a9d247b5e165466ad467dd64333",
    "ApiSecret": "ZDI0MzI3MTRjYzFmNDkwOWEwZTM5MzIw",
    "ModelVersion": {
      "DisplayName": "Max",
      "Domain": "generalv3.5",
      "AddressPart": "v3.5"
    }
  },
```

配置好后使用 VS 运行 WebStarter 项目运行，至此后端配置配置完毕。

#### [](#2前端部分)2).前端部分

配置：BotSharp-UI/.env 配置文件

将https://botsharp.azurewebsites.net 改为本地的后端地址如下：

```
# PUBLIC_SERVICE_URL=https://botsharp.azurewebsites.net
# PUBLIC_LIVECHAT_HOST=https://victorious-moss-007e11310.4.azurestaticapps.net/
PUBLIC_SERVICE_URL=http://localhost:5500
PUBLIC_LIVECHAT_HOST=http://localhost:5015/
```

至此前端准备完毕 从命令行中按Ctrl+C中止前端运行，再执行

```
npm run dev
```

进行重启前端项目

至此最基本的前后端联调配置全部完毕，下面通过UI来配置智能体让其能说话。

### [](#13-前端配置组件)1.3 前端配置组件

1).安装组件

![img](https://q5.itc.cn/q_70/images03/20250106/90c3602515324b0cafcf476b48257528.png?ynotemdtimestamp=1778553916926)

图1 组件选项卡。第一步点击该选项卡进入组件配置界面

![img](https://q3.itc.cn/q_70/images03/20250106/f1c7e55ebc72480da68b9ff511cc1bbb.png?ynotemdtimestamp=1778553916926)

图2 组件配置界面。第二步翻到第3页安装sparkdesk智能体，点击Install安装按钮

安装好后

![img](https://q2.itc.cn/q_70/images03/20250106/b38a12b68ddb44d89b919b65216bd6df.png?ynotemdtimestamp=1778553916926)

图3 智能体选项卡。第三步点击 Agent中的 Agents选项卡

图4 智能体配置界面。第四步点击Chatbot智能体标题，会进入该智能体配置界面。

图5 智能体详细配置界面。第五步选择Provider和模型。

![img](https://q1.itc.cn/q_70/images03/20250106/1c318a09f6a04322892f182885d28e3e.png?ynotemdtimestamp=1778553916926)

图6 智能体详细配置界面。第六步保存智能体。

图7 智能体列表界面。第七步点击test按钮即可进行对话

![img](https://q4.itc.cn/q_70/images03/20250106/55a991bb0d1c43f4a22e36cd681e8cc9.png?ynotemdtimestamp=1778553916926)

图8 对话界面。

恭喜你，完成了入门Botsharp的第一步