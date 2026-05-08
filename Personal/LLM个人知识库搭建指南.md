---
tags:
  - LLM
  - 知识库
  - Karpathy
---
### **LLM Wiki 到底是啥**

说白了就一句话：**让大模型当你的知识库管理员，而不是临时搜索工具。**

传统 RAG 是你提问的时候，系统现去翻文档、切片、向量匹配、拼凑答案。每次都从头来，问完就忘。你存了 500 篇论文，它们之间有什么关系？RAG 不知道，也不关心。

Karpathy 的思路完全反过来。他让 LLM 在你存入资料的时候就开始干活——读内容、写摘要、建索引、打链接。生成的不是向量，而是一篇篇结构化的 Markdown Wiki 页面。这些页面之间有交叉引用，有反向链接，跟维基百科一个逻辑。

他在开源的 Gist 里打了个比方：**[Obsidian](https://zhida.zhihu.com/search?content_id=272603049&content_type=Article&match_order=1&q=Obsidian&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzc5NTIxNjgsInEiOiJPYnNpZGlhbiIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjI3MjYwMzA0OSwiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.aR-63fp2nV-LcHwUrXVWvuABBiLryQXoFHDCocD9p7Q&zhida_source=entity) 是前端，LLM 是后端程序员，Wiki 是代码库。** 你不直接写 Wiki，LLM 写。你负责投喂原始素材和提问，LLM 负责所有脏活——总结、归类、交叉引用、维护一致性。

### **三层结构**

  

![](https://pic3.zhimg.com/v2-cefae5b359257c504c7240d479ca5674_1440w.jpg)

  

整套方案分三层，非常清晰：

**raw/**——你的原始素材。剪藏的文章、下载的论文、会议笔记，全扔这里。LLM 只读不写。这是你的 source of truth。

**wiki/**——LLM 的领地。它读 raw 里的内容，编译成结构化的 `.md` 页面。概念页、实体页、摘要页、对比分析页，全自动生成。除了 LLM，人别动这里。

**output/**——查询产物。比如你让 LLM 写个分析报告、做个 PPT 提纲。好的结果可以"回流"到 wiki 层，变成永久资产。

三条铁律：raw 不可变、wiki LLM 独占、好的 output 要回流。

### **跟 RAG 的核心区别**

| 维度    | RAG      | LLM Wiki       |
| ----- | -------- | -------------- |
| 干活时机  | 提问时才检索拼凑 | 入库时就编译好了       |
| 有没有积累 | 没有，问完就散  | 有，Wiki 越写越精    |
| 交叉引用  | 不存在      | 自动维护 backlinks |
| 矛盾检测  | 不管       | 编译时就标记冲突       |
| 人的角色  | 搬运工      | 策展人            |

一个类比：RAG 像图书管理员，你问他问题，他现翻索引扯几页纸出来；LLM Wiki 像私人秘书，他把你所有资料读完整理成一本定制百科，你提问的时候他是在"脑内搜索"。

### **三个核心操作**

**Ingest（摄取）**——往 raw 里扔一篇新文章，让 LLM 处理。它会读内容、写摘要页、更新概念页和实体页、维护索引、追加日志。一篇源文件可能触发 10-15 个 wiki 页面的更新。

**Query（查询）**——直接提问。LLM 先扫 index.md 定位相关页面，再读具体 wiki 页面综合回答。不需要向量数据库，不需要 embedding，wiki 本身就是 RAG 的"编译缓存"。

**Lint（体检）**——定期让 LLM 给知识库做健康检查。找矛盾、找过时内容、找孤立页面、找缺失链接。这步很多人忽视，但它是保持知识库长期健康的关键。

### **怎么上手**

我自己跑通的流程：

**工具准备**：Obsidian + 一个强力 LLM（我用的 [Claude](https://zhida.zhihu.com/search?content_id=272603049&content_type=Article&match_order=1&q=Claude&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzc5NTIxNjgsInEiOiJDbGF1ZGUiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNzI2MDMwNDksImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.kaEpiuFAI003iGTNqrsg4pIff9X1Dr4z1-DfW3C8AgY&zhida_source=entity)）+ [Web Clipper](https://zhida.zhihu.com/search?content_id=272603049&content_type=Article&match_order=1&q=Web+Clipper&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzc5NTIxNjgsInEiOiJXZWIgQ2xpcHBlciIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjI3MjYwMzA0OSwiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.ZOZtGlNXrkxmPtPnMQ6ZlP8Xtq0cWj-A5Kw3XyD6GbI&zhida_source=entity) 浏览器插件。Karpathy 在 Gist 里推荐了 Obsidian Web Clipper 直接把网页转 Markdown，非常好用。

**建目录**：在 Obsidian 里建 `raw/`、`wiki/`、`output/` 三个文件夹。wiki 下面初始化 `index.md`（总索引）、`log.md`（操作日志）、`overview.md`（知识地图）。

**投喂**：看到好文章直接一键剪藏到 raw。不用管格式，不用分类，扔进去就行。

**编译**：告诉 LLM 去读 raw 里的新文件，按规范编译到 wiki。它会自动处理摘要、分类、链接。

**定期 Lint**：每周跑一次健康检查，让 LLM 扫描知识库找问题。

  

![](https://pic3.zhimg.com/v2-6c860c4f558ea97456d4c771d9828166_1440w.jpg)

### **进阶玩法**

Gist 里还藏了几个实用招：

**图片本地化**——Obsidian 设置里把附件路径指到 `raw/assets/`，绑快捷键一键下载。外链失效？不存在的。

**[Marp](https://zhida.zhihu.com/search?content_id=272603049&content_type=Article&match_order=1&q=Marp&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3Nzc5NTIxNjgsInEiOiJNYXJwIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MjcyNjAzMDQ5LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.1l4jouculwwO3W02S6SltifXtgfvz7jNqxpoLgPIdj0&zhida_source=entity) 出 PPT**——让 LLM 根据 wiki 内容直接吐 Marp 格式，几秒钟一套演示文稿。

**Dataview 做看板**——wiki 页面带 YAML frontmatter，Dataview 当数据库查，自动更新仪表盘。

**Git 管版本**——一堆 Markdown 文件，天生适合 Git。每次 ingest 完自动 commit，知识演变一目了然，写坏了 revert 就完事。

### **局限**

别神化它，几个现实问题：

**上下文窗口有极限**。虽然现在模型号称支持百万 Token，但超过 40 万字后精度打折扣。

**幻觉会固化**。LLM 编译阶段如果产生幻觉，错误会被写死到 Wiki 里。所以定期 Lint 不是可选项，是必须的。

**超大规模撑不住**。数据量到千万字级别，编译成本太高，终归要回到搜索基建。但对个人用户，这天花板足够高了。

### **这份 Gist 的真正价值**

Karpathy 开源的不是代码，是一份 instruction。他自己说得很直白：**这文档就是设计来直接复制粘贴给你的 LLM Agent 的。**

喂给 Claude Code、Codex 或者其他 coding agent，它就知道怎么帮你搭建和维护这套知识库。

不写代码，不调 API，写清楚你想要什么，让 LLM 自己去实现。这才是 2026 年该有的知识管理姿势。