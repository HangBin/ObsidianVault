---
tags:
  - openclaw
  - skill
---

配置
```
✅ 用户配置: ~/.config/obsidian/
✅ Vault配置: /home/obsidian_vault/.obsidian/
```

📁 知识库结构
```markdown
/home/obsidian_vault/
├── QMD记忆系统.md              # 核心技术文档
├── daily-notes/
│   └── 2026-04-24.md           # 今日工作日志  
├── .obsidian/                  # Obsidian核心配置目录
│   ├── plugins/                # 插件存储
│   ├── templates/              # 模板文件
│   ├── themes/                 # 主题文件
│   ├── config.json             # 核心插件设置
├── .gitkeep                  # Git占位符
└── .obsidian.json           # 基础配置
```

QMD集成
```bash
# 配置QMD监控
openclaw config set memory.qmd.workspaceDirs '["/home/obsidian_vault"]'

# 更新索引
openclaw memory update --workspace /home/obsidian_vault
```
