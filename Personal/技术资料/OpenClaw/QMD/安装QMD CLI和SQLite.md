---
tags:
  - qmd
  - sqlite
  - OpenClaw配置
  - memory
  - 搜索
---
## 安装
```bash
# 安装 QMD CLI
所有平台统一使用以下命令：
npm i -g bun
npm install -g @tobilu/qmd
# 安装失败，CMake版本太低(3.16.3)，且node-llama-cpp编译依赖缺失。尝试跳过postinstall：
npm install -g @tobilu/qmd --node-llama-cpp-postinstall=skip 2>&1
# 验证安装
qmd --version

# 安装支持向量扩展的 SQLite
# 访问 SQLite 官网下载页面：https://www.sqlite.org/download.html
# 下载 “Precompiled Binaries for Windows” 中的 sqlite-tools-win-x64-*.zip（包含 sqlite3.exe）
# 重启终端，验证安装
apt install sqlite3
sqlite3 --version
```

## 编辑 OpenClaw 配置文件
```bash
  "memory": {
    "backend": "qmd",
    "qmd": {
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",
        "debounceMs": 15000
      },
      "limits": {
        "maxResults": 6,
        "timeoutMs": 8000
      },
      "scope": {
        "default": "allow",
        "rules": [
          {
            "action": "allow",
            "match": {
              "chatType": "direct"
            }
          }
        ]
      }
    }
  }
```
针对 `memory` 部分的完整配置示例
```bash
{  
  memory: {  
    backend: "qmd", // 启用QMD后端  
    qmd: {  
      // QMD 可执行文件路径（默认使用PATH中的qmd，无需修改）  
      command: "qmd",  
      // 搜索模式：query(完整语义)/search(仅BM25)/vsearch(仅向量)  
      // 设备优化：低配设备（<8GB内存）切换为searchMode: "search"  
      searchMode: "query",  
      // 是否包含默认记忆文件（推荐开启）  
      includeDefaultMemory: true,  
      // 额外索引路径（可添加个人笔记、团队知识库等）  
      paths: [  
        { path: "~/notes", pattern: "**/*.md", name: "my-notes" }  
      ],  
      // 索引更新配置  
      update: {  
        interval: "5m",          // 索引自动更新间隔  
        debounceMs: 15000,       // 文件变更防抖时间，避免频繁更新  
        onBoot: true,            // 网关启动时自动更新索引  
        waitForBootSync: false,  // 不阻塞启动直到索引更新完成  
        embedInterval: "60m",    // 向量嵌入更新间隔  
        commandTimeoutMs: 30000, // collection操作超时  
        updateTimeoutMs: 120000, // 索引更新超时  
        embedTimeoutMs: 120000   // 向量嵌入更新超时  
      },  
      // 查询限制配置  
      limits: {  
        maxResults: 6,           // 最大返回结果数  
        maxSnippetChars: 700,    // 单个结果片段最大字符数  
        maxInjectedChars: 4000,  // 注入LLM上下文的最大总字符数  
        timeoutMs: 30000         // 查询超时时间（低配设备30000ms）  
      },  
      // 搜索作用域精细控制  
      scope: {  
        default: "allow",        // 全局默认允许所有场景搜索  
        rules: [  
          // 可自定义规则，如禁止电报群聊搜索  
          // { action: "deny", match: { channel: "telegram", chatType: "group" } }  
        ]  
      },  
      // 会话索引（实验性功能，暂不推荐开启）  
      sessions: {  
        enabled: false,          // 是否索引历史会话记录  
        retentionDays: 30        // 会话记录保留天数  
      }  
    }  
  }  
}
```
## 需要下载的模型

| 模型                              | 大小      | 用途   |
| ------------------------------- | ------- | ---- |
| `embeddinggemma-300M-GGUF`      | ~600MB  | 向量嵌入 |
| `Qwen3-Reranker-0.6B-Q8_0-GGUF` | ~600MB  | 结果重排 |
| `qmd-query-expansion-1.7B`      | 1.28 GB | 查询扩展 |

你本地下载模型（推荐）

```bash
# 1. 创建模型目录
mkdir -p ~/.cache/qmd/models/

# 2. 下载模型文件（需要 HuggingFace 账号和代理）
#  Embedding:   https://huggingface.co/ggml-org/embeddinggemma-300M-GGUF
#  Reranking:   https://huggingface.co/ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF
#  Generation:  https://huggingface.co/tobil/qmd-query-expansion-1.7B-gguf

# 3. 上传到 VPS 的 ~/.cache/qmd/models/ 目录
scp -r ./models/* user@vps:~/.cache/qmd/models/
```


## QMD效率最大化的解决方案

**核心思路：MEMORY.md = 索引目录，详细内容在 memory/ 目录**

**现状分析**

```
MEMORY.md (21KB) ──── 自动加载 ──── 每次会话必读
memory/*.md (224文件) ── QMD索引 ──── 按需查询
```

**问题**：MEMORY.md 仍然太大（21KB），而且被删掉的那些"历史关键事件"并没有消失，只是被移到了memory/ 目录（QMD索引范围）。

------

**✅ QMD效率最大化的最佳实践**

方案：分层记忆架构

```
┌─────────────────────────────────────────┐
│  MEMORY.md (目标: ≤10KB)                │
│  - 身份铁律、职责范围、核心规则             │
│  - 索引引用（指向 memory/experience-*） │
│  - 高频操作摘要（不超5行/项）           │
└─────────────────────────────────────────┘
              ↓ 引用
┌─────────────────────────────────────────┐
│  memory/experience-*.md (详细经验)      │
│  - 完整的技术方案、流程、错误记录        │
│  - QMD索引范围，按需检索                │
└─────────────────────────────────────────┘
              ↓ 检索
┌─────────────────────────────────────────┐
│  QMD (224文件, 1765向量)                │
│  - 会话中主动 query 获取相关片段        │
│  - 只加载需要的部分，不污染上下文       │
└─────────────────────────────────────────┘
```

------

**🔧 具体操作**

1.精简 MEMORY.md（保持 ≤10KB）

- 删除重复的章节描述
- 历史事件只保留"索引指针"，不保留详情
- 工作流模式精简为一句话引用
- 只保留**核心规则**和**高频操作**
- 把长篇经验、详细流程移到 `memory/YYYY-MM-DD.md`（QMD 索引范围）

2.会话中使用 QMD

```bash
# 当用户问"上次Docker部署的问题怎么解决的"
qmd query "docker 部署问题" --collection tech-daily -n 3

# 当用户问"4月9日的经验"
qmd get memory/2026-04-09.md -l 50
```

3. 效果

| 场景       | 无QMD优化 | QMD优化后           |
| ---------- | --------- | ------------------- |
| 会话启动   | 21KB      | ~10KB ✅             |
| 问历史细节 | ❌ 不知道  | ✅ qmd query 获取    |
| 上下文总量 | 固定36KB  | 启动10KB + 按需补充 |



## QMD 搜索方式

| 方式          | 命令                            | 速度            | 用途         |
| ------------- | ------------------------------- | --------------- | ------------ |
| **BM25 搜索** | `qmd search "关键词" -c share`  | ⚡ 快            | 直接全文检索 |
| **语义搜索**  | `qmd query "自然语言" -c share` | 🐢 慢（需embed） | 语义理解     |

正确的向量搜索流程

```bash
# 1. 先生成 embeddings（一次性）
qmd embed -f

# 2. 然后才能用向量搜索（需先embed）
qmd vsearch "浏览器 CDP 端口配置" -c share --max-results 5

# 3. 或者用混合搜索（自动判断）
qmd query "浏览器 CDP 端口配置" -c share

# 搜索浏览器经验（share 集合）
qmd search "CDP 9222" -c share                # 全文搜索（BM25）
```

