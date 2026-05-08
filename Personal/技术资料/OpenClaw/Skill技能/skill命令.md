---
tags:
  - openclaw
  - skill
---
**安装ClawHub CLI工具**

（技能管理工具）
```
# 安装ClawHub CLI工具（技能管理工具）
npm i -g clawhub
# 初始化
clawhub init
npx clawhub init
# 登录ClawHub（使用OpenClaw访问Token）
clawhub login --token clh_K2I3byCXqZuai-XnQt8_khwZ1HkUruGZIC6ZdyY64eM

# 配置国内镜像源
openclaw config set clawhub.mirror "https://mirror.aliyun.com/clawhub/"
```

**基本skill命令**
```bash
# 查询有哪些skills
openclaw search "linux"
# 列出已安装技能
openclaw skills list
# 查看已安装的
openclaw skills list --eligible
# 查看技能配置
openclaw skills config skill-name
# 更新技能
openclaw skills update skill-name
# 强制覆盖安装
skillhub install translate-cli --force
# 安装全局skills目录下
clawhub install capability-evolver --workdir ~/.openclaw
```

**安装方式**
- 使用npx skills add ...
- 使用clawhub install ...
- 手动安装把技能目录拷贝到 ~/.openclaw/skills/
