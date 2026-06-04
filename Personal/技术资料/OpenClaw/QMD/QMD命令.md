---
tags:
  - qmd
  - 命令
---
## 集合与索引建立

```bash
# 创建集合与添加文档
# 为主代理、tech代理创建集合并添加工作区文档
qmd collection add ~/.openclaw/workspace --name main
qmd collection add ~/.openclaw/workspace-tech --name tech

# 添加上下文语义描述（增强搜索效果）
# 为主集合、tech集合添加语义描述
qmd context add qmd://main "main主工作区的核心配置集合"
qmd context add qmd://main-daily "main主工作区的每日对话和经验文档集合"

# 列出所有集合确认创建成功
qmd collection list
# 测试main集合搜索功能
qmd search "project timeline" -c main
# 测试tech集合搜索功能
qmd search "deployment process" -c tech

# memory目录以及子目录所有md文件
qmd collection add --path ~/.openclaw/workspace/memory/ --name main-memory

# 添加根目录md文件（仅当前层级）
# (把所有的md文件全加进来了)
qmd collection add --path ~/.openclaw/workspace/ --name main
# 递归添加memory目录所有md文件（含archive子目录）
qmd collection append --path ~/.openclaw/workspace/memory/**/*.md --name main


# 1. 核心配置集合（根目录配置文件）
qmd collection add config ~/.openclaw/workspace-tech/ \
  --pattern "*.md" \
  --description "核心配置: MEMORY/SOUL/IDENTITY/AGENTS/TOOLS/USER"

# 2. 每日对话集合（memory 日志）
qmd collection add daily ~/.openclaw/workspace-tech/memory/ \
  --pattern "*.md" \
  --description "每日对话日志"

# 3. 经验文档集合（experience 文件）
qmd collection add experiences ~/.openclaw/workspace-tech/memory/ \
  --pattern "experience-*.md" \
  --description "经验文档汇总"

如果需要排除特定文件（如临时文件），可添加--exclude参数：
qmd collection add ~/.openclaw/workspace/*.md --exclude "temp*.md" --name main


--pattern "*.md"
--pattern "experience*.md"

# 删除索引文件（重置所有数据）
rm -f /home/memory-collection/index.sqlite

# main-root: 核心配置
qmd collection add /root/.openclaw/workspace --mask "*.md" --name main-root --description "main主工作区的核心配置集合"
# memory目录以及子目录所有md文件(38个文件，对的)
qmd collection add --path ~/.openclaw/workspace/memory/ --name main-daily --description "main主工作区的每日对话和经验文档集合"
# main-daily: memory 目录（包含 experience*.md）
# 30错误的，缺少子文件夹
qmd collection add /root/.openclaw/workspace/memory --mask "*.md" --name main-daily
# 30错误的，缺少子文件夹
qmd collection add /root/.openclaw/workspace/memory/ --mask "*.md" --name main-daily

# workspace-tech
qmd collection add /root/.openclaw/workspace-tech --mask "*.md" --name tech-root
qmd collection add --path ~/.openclaw/workspace-tech/memory/ --name tech-daily
```

##  索引与集合操作命令

```bash
qmd --version
# 查看索引状态
qmd status
# 列出文件
qmd ls main-root
# 查看具体文件信息
qmd get qmd://tech-daily/2026-04-18.md

# 初始化索引
qmd index init
# 更新索引（指定目录）
qmd index update /path/to/memory/files

# 查看集合列表
qmd collection list
# 创建集合
qmd collection create <集合名>
# 创建集合：
qmd collection add . --name workspace
# 命令说明
# - . ：表示当前目录（你的 workspace 目录）
# - --name workspace：给这个集合起个名字叫 “workspace”
# 更新单个集合
qmd collection update <集合名> /path/to/files
# 查看 workspace 集合路径
qmd collection show workspace

# 删除集合
qmd collection remove tech-daily

# 生成向量索引（支持语义搜索）
qmd embed
# 初始化索引
qmd update
qmd update --dir "~\.openclaw\workspace"

# 全文搜索（不依赖向量）
qmd search "<关键词>"
qmd search "query" -c main-root

# 语义检索
qmd query "关键词" --collection memory --max-results 5


💡 高级用法
混合搜索（结合关键词与语义）：
qmd query "error handling strategies" --hybrid -c main
导出结构化结果（供AI使用）：
qmd search "authentication" --json -n 10
守护模式（保持模型加载状态）：
qmd daemon start
qmd query "quarterly planning" --daemon


手动重建索引：openclaw memory index --force
```