---
author: tech agent
created: 2026-04-28 18:17:38
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
tags:
  - tech-agent
  - knowledge
  - experience
  - bash
---


# 脚本开发指南 - Bash 最佳实践与技术沉淀

**Agent**: tech
**更新日期**: 2026-04-04
**适用范围**: 所有 Bash 脚本开发

---

## 🎯 指南概述

本文档总结 Bash 脚本开发的核心最佳实践，基于记忆归档与学习提取工作流的实践经验，适用于所有 OpenClaw Agents 的自动化脚本编写。

### 覆盖主题
- 工作区路径动态检测
- 算术运算与数据类型（八进制陷阱）
- 文本处理（段落分割、清理）
- 函数设计（生成条目、分类逻辑）
- 用户体验（dry-run、verbose）
- 共享分发与部署

### 示例场景
```bash
# 记忆归档工作流
extract_learnings_auto.sh  # 自动提取
organize_memories.sh       # 完整整理
start.sh                   # 交互入口
```

（完整示例见 `/root/.openclaw/share/learning-workflow/`）

---

## 🔧 核心主题

### 1. 工作区路径动态检测

**问题**：硬编码路径导致脚本无法跨 Agent 复用
**解决**：基于脚本位置向上查找父目录
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="$WORKSPACE/memory"
LEARNINGS_DIR="$WORKSPACE/.learnings"
```
**价值**：脚本可放在 `scripts/` 子目录或根目录，自动适配

---

### 2. Bash 算术与数据类型

**八进制陷阱**：
```bash
next_id="008"
next_id=$((next_id + 1))  # ❌ 报错: value too great for base
```

**强制十进制**：
```bash
next_id=$((10#$next_id + 1))  # ✅ 正确
```

**适用场景**：ID 处理、数字格式化、等差数列

---

### 3. 文本行清理与格式化

**问题**：`grep | sed | tail` 可能输出含换行符的多行内容
**解决**：
```bash
ids=$(command ... | tr -d '\n\r')
# 或
ids=$(command ... | awk '{printf "%d\n", $1}')
```

**固定宽度格式化**：
```bash
printf '%03d' "$ids"  # 001, 002, ... 999
```

---

### 4. 段落分割与内容提取

**场景**：从 Markdown 文件中提取 `## 标题` 开头的段落
**实现**：
```bash
awk '
BEGIN { paragraph="" }
/^## [A-Z]/ {
    if (paragraph != "") print paragraph
    paragraph=$0 "\n"
    next
}
{ paragraph = paragraph $0 "\n" }
END { if (paragraph != "") print paragraph }
' file.md | while read -r para; do
    process_paragraph "$para"
done
```

**要点**：awk 负责分段，Bash `while read` 逐段处理

---

### 5. 生成函数设计

**避免 heredoc 引号嵌套问题**，使用纯 `echo`：
```bash
generate_error_entry() {
    local title="$1" snippet="$2" file="$3"
    echo "## [ERR-$(date +%Y%m%d)-$(pad_id "$next_id")] $title"
    echo ""
    echo "### Summary"
    echo "$title"
    echo ""
    echo "```"
    echo "$snippet"
    echo "```"
    # ...
}
```

**优势**：结构清晰，易于调试，无 quoting 问题

---

### 6. 交互式脚本 (start.sh)

**要求**：支持从 `scripts/` 子目录运行，自动定位工作区
**模式**：
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

if [ -d "$WORKSPACE_DIR/memory" ] && [ -d "$WORKSPACE_DIR/.learnings" ]; then
    cd "$WORKSPACE_DIR" || exit 1
fi
```

**用户流程**：
```bash
cp scripts/ ~/.openclaw/workspace-<agent>/scripts/
cd ~/.openclaw/workspace-<agent>
./scripts/start.sh  # ✅ 自动定位并运行
```

---

### 7. 命令行参数设计

**标准参数**：
```bash
--dry-run    # 预览，不修改文件
--verbose    # 详细日志
--help       # 帮助信息
```

**实现模式**：
```bash
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=1 ;;
        --verbose) VERBOSE=1 ;;
        --help) usage; exit 0 ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
    shift
done
```

---

### 8. 共享分发模式

**集中管理**：
```
/root/.openclaw/share/learning-workflow/
├── *.sh
├── 说明.md
└── start.sh
```

**Agent 使用**：
```bash
mkdir -p ~/.openclaw/workspace-<agent>/scripts
cp /root/.openclaw/share/learning-workflow/*.sh ~/.openclaw/workspace-<agent>/scripts/
cd ~/.openclaw/workspace-<agent>
./scripts/start.sh
```

**优势**：统一版本，集中维护，易于更新

---

### 9. 错误处理与用户体验

**原则**：
- ✅ `set -e`：任何命令失败即退出
- ✅ 明确的错误信息：包含当前路径、脚本位置、期望结构
- ✅ 状态反馈：使用 emoji（✅ ❌ ⚠️ 🧠）
- ✅ 统计汇总：显示处理文件数、新增条目数

**示例**：
```bash
if [ ! -d "$MEMORY_DIR" ]; then
    error "memory/ 不存在"
    exit 1
fi
```

---

### 10. 调试技巧

| 技巧 | 命令 |
|------|------|
| 跟踪执行 | `bash -x script.sh` |
| 打印变量 | `echo "var='$var' (len=${#var})"` |
| 验证算术 | `echo $((10#008 + 1))` |
| 管道调试 | `cmd | tee /tmp/debug.log` |
| 段落分割 | `awk '...' file \| head -20` |

---

## 📋 检查清单（新脚本开发）

- [ ] 路径动态检测（SCRIPT_DIR + dirname）
- [ ] 八进制数字使用 `10#` 前缀
- [ ] 所有输出 `tr -d '\n\r'` 清理
- [ ] 生成函数用 `echo` 而非 heredoc
- [ ] 支持 `--dry-run` 和 `--verbose`
- [ ] start.sh 支持 `scripts/` 子目录运行
- [ ] 错误信息包含路径信息
- [ ] 文档化函数用途和参数
- [ ] 测试边界情况（空文件、无匹配）
- [ ] 共享时提供 `说明.md`

---

## 🔄 与其他经验关联

- **experience-docker.md** - Docker 容器编排
- **experience-mission-control.md** - Next.js 应用部署
- **experience.md** - 综合工作流模式
- **backup_workspaces/README.md** - 工作区备份系统实现（2026-04-05）

---

## 💡 近期实践案例

### 工作区备份系统 (backup_workspaces_weekly.sh)

**实现要点**:
- ✅ 多工作区并行备份（main/tech/media/proj/final）
- ✅ 按工作区独立保留最新3份备份（删除最老）
- ✅ 纯文本日志 + 分隔线，清晰易读
- ✅ 自动清理旧备份，防止磁盘占用
- ✅ 错误处理：`set -e` + 目录检查

**关键代码**:
```bash
# 保留最新3份
mapfile -t backups < <(find "$BACKUP_DIR" -name "${NAME}_backup_*.tar.gz" | sort -r)
if [[ ${#backups[@]} -gt 3 ]]; then
  rm -f "${backups[@]:3}"
fi
```

**经验沉淀**:
- 避免 `--from=builder` 循环依赖（Docker 教训）
- 日志格式优先考虑可读性（避免 ANSI 颜色）
- 每个工作区独立管理备份数量，避免单点占用

---

## 📚 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-04 | 1.0 | 初始版本（基于学习提取工作流） |
| 2026-04-05 | 1.1 | 补充工作区备份系统实践案例 |

---

**Happy Scripting! 🚀**

- **2026-04-29** **规则4：脚本开发相关经验**

---

## 📝 Shell 脚本注释规范与命令语法（2026-04-30 新增）

### 核心规则

**所有可执行 shell 脚本必须包含以下注释块：**

```bash
#!/bin/bash
#===============================================
# script-name.sh
# 脚本功能简短描述
#===============================================
#
# 用途：
#   详细说明脚本的用途和使用场景
#
# 使用方式：
#   ./script-name.sh [参数]
#
# 命令语法：
#   ./script-name.sh --param1 value1 --param2 value2
#
# 示例：
#   ./script-name.sh --write --today
#   ./script-name.sh "直接写入内容"
#
# 注意事项：
#   重要的限制条件和副作用
#
#===============================================
```

### 必须包含的元素

| 元素 | 位置 | 说明 |
|------|------|------|
| Shebang | 第1行 | `#!/bin/bash` |
| 标题块 | 第2-5行 | 脚本名 + 功能描述 |
| 用途 | 注释中 | 详细说明使用场景 |
| 使用方式 | 注释中 | 基本语法 |
| 命令语法 | 注释中 | 具体参数说明 |
| 示例 | 注释中 | 常用命令示例 |
| 注意事项 | 注释中 | 重要限制条件 |

## 📅 更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-04-04 | 1.0 | 初始版本 |
| 2026-04-05 | 1.1 | 补充工作区备份系统实践案例 |
| 2026-04-30 | 1.2 | 新增脚本注释规范 |
