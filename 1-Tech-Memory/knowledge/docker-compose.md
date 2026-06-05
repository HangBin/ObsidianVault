---
author: tech agent
created: 2026-04-14 09:34:12
modified: 2026-04-29 11:01:00 GMT+8
version: v1.0.0
source: tech agent memory/experience-docker-compose.md
tags: [tech-agent, experience, knowledge, docker]
---


# Docker 编排实战经验

## OpenClaw Control Center 部署问题总结（2026-04-02）

### 1. .env 文件加载失败
- **症状**: test-docker.sh 提示"无法加载 .env 文件"
- **根因**: 子 shell `(set -a && . .env && set +a)` 导致变量不可见
- **修复**: 使用 `set -a && . .env && set +a`（无括号）+ `export GATEWAY_URL LOCAL_API_TOKEN`
- **简化方案**: 删除手动加载，直接使用 `docker compose`（它自动读取 `.env`）

### 2. Dockerfile 循环依赖
- **症状**: `failed to solve: circular dependency detected on stage: builder`
- **根因**: `COPY --from=builder` 从自身复制
- **修复**: 改为 `COPY /app/package.json ... ./`（直接复制工作区文件）

### 3. HEALTHCHECK 语法
- **症状**: `unknown flag: start_period`
- **根因**: 下划线应为连字符
- **修复**: `--start-period` ✅（注意：docker-compose.yml 中字段名也需匹配 compose 版本）

### 4. Docker Compose 版本兼容
- **症状**: `Additional property start-period is not allowed`
- **根因**: 旧版 Compose 不支持 `start-period`
- **修复**: 移除 `start-period`，仅使用 `interval/timeout/retries`

### 5. docker-compose.yml 版本过时
- **症状**: `version is obsolete`
- **修复**: 删除顶部的 `version: '3.8'` 字段（compose 自动检测）

---

## ✅ 最佳实践

### Dockerfile
- 多阶段构建分离 builder/production
- 先复制依赖文件再复制源码（层缓存优化）
- 避免 `--from=builder` 循环引用
- healthcheck 使用最简字段

### docker-compose.yml
- 移除 `version` 字段
- 环境变量使用 `${VAR:-default}` 语法
- OpenClaw 数据目录 `:ro` 只读挂载
- 应用数据持久化到匿名卷

### 脚本
- 信任 `docker compose` 自动加载 `.env`
- 使用 `set -e` 快速失败
- 清晰的颜色输出和步骤提示

---

## 🔍 部署自检清单

- [ ] `.env` 无 BOM、无空格、无空值行
- [ ] Dockerfile 无循环依赖
- [ ] healthcheck 字段兼容目标 Compose 版本
- [ ] docker-compose.yml 无 `version` 字段
- [ ] 关键变量 `GATEWAY_URL`、`LOCAL_API_TOKEN` 已设置

---

## 📂 相关文件
- 完整部署套件: `openclaw-control-center-deploy/`
- 经验总结: `memory/experience-docker.md`
- 测试脚本: `test-docker.sh`（已修复变量导出和循环依赖问题）
# Docker 容器编排完整指南
## OpenClaw Control Center 部署实战

**版本**: 1.0
**最后更新**: 2026-04-02
**适用对象**: 需要部署 OpenClaw Control Center 的技术人员
**前置要求**: Docker, Docker Compose, 基础 Linux 操作

---

## 📋 目录

1. [环境准备](#环境准备)
2. [获取部署文件](#获取部署文件)
3. [配置环境变量](#配置环境变量)
4. [验证配置](#验证配置)
5. [构建与启动容器](#构建与启动容器)
6. [验证服务](#验证服务)
7. [容器管理命令](#容器管理命令)
8. [故障排查](#故障排查)
9. [常见错误与解决](#常见错误与解决)
10. [最佳实践](#最佳实践)

---

## 环境准备

### 1.1 系统要求

| 组件 | 版本要求 | 验证命令 |
|------|----------|----------|
| Docker | 20.10+ | `docker --version` |
| Docker Compose | 2.x+ | `docker compose version` |
| Git | 2.x+ (可选) | `git --version` |
| Node.js | 22+ (仅本地源码构建需要) | `node --version` |
| pnpm | 9.x+ (仅本地源码构建需要) | `pnpm --version` |

### 1.2 工作区结构

**推荐的部署目录**（遵循 OpenClaw 代理隔离原则）：
```
~/.openclaw/workspace-tech/
└── openclaw-control-center-deploy/  # 部署文件
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.example
    ├── .env              # 你的配置（不提交到版本控制）
    ├── run.sh
    ├── test-docker.sh
    ├── DEPLOYMENT.md
    ├── QUICKSTART.md
    └── README.md
```

**前置检查**：
```bash
# 确保在正确的工作区
cd ~/.openclaw/workspace-tech

# 检查 Docker 环境
docker --version
docker compose version

# 检查 OpenClaw Gateway 是否运行
ss -tlnp | grep 18789 || echo "Gateway 未运行"
```

---

## 获取部署文件

### 2.1 方式一：使用预打包的部署套件

部署文件已包含在 OpenClaw 仓库或独立分发包中：
```bash
# 如果还没有部署文件，克隆或复制到工作区
mkdir -p ~/.openclaw/workspace-tech
cd ~/.openclaw/workspace-tech

# 复制整个部署目录
# cp -r /path/to/openclaw-control-center-deploy ./
```

### 2.2 方式二：从源码构建部署文件

如果需要从源码创建部署套件：
```bash
cd ~/.openclaw/workspace-tech
git clone https://github.com/TianyiDataScience/openclaw-control-center.git
# 参考 DEPLOYMENT.md 创建部署文件结构
```

---

## 配置环境变量

### 3.1 复制配置模板

```bash
cd ~/.openclaw/workspace-tech/openclaw-control-center-deploy
cp .env.example .env
```

### 3.2 编辑 .env 文件（关键配置）

**必填配置**（至少设置这两项）：

```env
# OpenClaw Gateway 地址（必须）
GATEWAY_URL=http://119.45.132.214:18789
# 或本地: GATEWAY_URL=http://127.0.0.1:18789

# 本地 API Token（必须，用于保护写操作，长度至少 32 字符）
LOCAL_API_TOKEN=f9d6fb7293d4d174d8b5bdb488a5cac9768733337568e9e2
# 生成方法: openssl rand -base64 32
```

**常用可选配置**：

```env
# UI 端口（宿主机映射）
UI_PORT=4310

# UI 绑定地址
# 127.0.0.1 = 仅本地访问（默认，安全）
# 0.0.0.0 = 所有网络接口（需要外部访问时）
UI_BIND_ADDRESS=127.0.0.1

# 界面语言
NEXT_PUBLIC_LANGUAGE=en  # 或 zh

# 安全配置（首次运行保持默认）
READONLY_MODE=true
LOCAL_TOKEN_AUTH_REQUIRED=true
APPROVAL_ACTIONS_ENABLED=false
IMPORT_MUTATION_ENABLED=false
```

**配置要点**：
- ✅ **等号两边不要有空格**：`KEY=value` ✅ `KEY = value` ❌
- ✅ **值不要包含未转义的特殊字符**（如 `$`, `!`, `#` 开头等）
- ✅ **空值行用 `#` 注释**，不要留空
- ✅ **文件编码为 UTF-8 无 BOM**（VS Code 可转换）

### 3.3 配置验证

```bash
# 语法检查
bash -n .env && echo "✅ Syntax OK"

# 测试加载（应输出变量值）
bash -c 'set -a && . .env && set +a && echo "GATEWAY_URL=$GATEWAY_URL"'
# 输出: GATEWAY_URL=http://...
```

---

## 验证配置

在正式部署前，建议运行测试脚本：

```bash
cd ~/.openclaw/workspace-tech/openclaw-control-center-deploy

# 如果有 test-docker.sh（修复后的版本）
./test-docker.sh

# 或者手动逐步检查
```

**测试脚本会检查**：
1. ✅ Docker 和 Docker Compose 是否安装
2. ✅ `.env` 文件存在且可加载
3. ✅ 关键变量 `GATEWAY_URL` 和 `LOCAL_API_TOKEN` 是否设置
4. ✅ OpenClaw 数据目录是否可访问
5. ✅ 网关连通性（可选）
6. ✅ 构建并启动容器

---

## 构建与启动容器

### 5.1 基本命令

```bash
cd ~/.openclaw/workspace-tech/openclaw-control-center-deploy

# 构建镜像并后台启动容器
docker compose -f docker-compose.yml up --build -d

# 如果文件名是标准 docker-compose.yml，可以简化
docker compose up --build -d
```

### 5.2 构建参数（可选）

通过环境变量控制构建行为（在 `docker-compose.yml` 中设置或命令行传递）：

```bash
# 使用本地源码（开发/定制场景）
USE_LOCAL_SOURCE=true
LOCAL_SOURCE_PATH="/root/.openclaw/workspace-tech/openclaw-control-center"

# 或从 GitHub 克隆（默认）
USE_LOCAL_SOURCE=false
REPO_URL="https://github.com/TianyiDataScience/openclaw-control-center.git"
BRANCH="main"
```

---

## 验证服务

### 6.1 检查容器状态

```bash
# 查看容器是否运行
docker compose ps
# 或
docker ps | grep openclaw-control-center

# 查看容器日志
docker compose logs -f openclaw-control-center

# 查看最近 20 行日志
docker compose logs --tail=20 openclaw-control-center
```

### 6.2 健康检查

```bash
# 查看容器健康状态
docker inspect --format='{{.State.Health.Status}}' openclaw-control-center
# 预期: healthy (starting 表示还在启动中)

# 手动测试健康端点
curl http://localhost:4310/api/health
# 预期: {"status":"ok"}
```

### 6.3 访问控制中心

打开浏览器：

- **英文界面**: http://localhost:4310/?section=overview&lang=en
- **中文界面**: http://localhost:4310/?section=overview&lang=zh

**首次访问**：
- 系统会提示输入 API Token
- 输入 `.env` 中设置的 `LOCAL_API_TOKEN` 值

---

## 容器管理命令

### 7.1 生命周期管理

```bash
# 重启容器
docker compose restart

# 停止容器（保留数据）
docker compose down

# 停止并删除容器、网络（数据保留在卷中）
docker compose down --remove-orphans

# 重新构建并重启（应用配置更新）
docker compose up --build -d

# 强制重新构建（忽略缓存）
docker compose build --no-cache && docker compose up -d
```

### 7.2 进入容器调试

```bash
# 进入容器 shell
docker compose exec openclaw-control-center /bin/bash

# 查看容器内环境变量
docker compose exec openclaw-control-center env | grep -E 'GATEWAY|OPENCLAW'

# 查看容器内文件
docker compose exec openclaw-control-center ls -la /app
```

### 7.3 资源监控

```bash
# 查看容器资源使用
docker stats openclaw-control-center

# 查看容器详细信息
docker inspect openclaw-control-center
```

---

## 故障排查

### 8.1 日志分析

```bash
# 实时查看日志（调试模式）
docker compose logs -f --tail=100 openclaw-control-center

# 查看错误日志
docker compose logs openclaw-control-center 2>&1 | grep -i error

# 查看启动时的日志
docker compose logs openclaw-control-center 2>&1 | head -50
```

### 8.2 网络连通性测试

```bash
# 从容器内部测试网关可达性
docker compose exec openclaw-control-center bash -c 'curl -v $GATEWAY_URL/api/health' 2>&1 | head -30

# 检查端口映射
docker port openclaw-control-center
# 应显示: 4310/tcp -> 0.0.0.0:4310
```

### 8.3 配置文件问题

```bash
# 检查容器内环境变量
docker compose exec openclaw-control-center env | grep -E 'GATEWAY|LOCAL_API_TOKEN|READONLY'

# 如果配置不对，更新 .env 后重启
# 1. 编辑 .env
# 2. docker compose down
# 3. docker compose up --build -d
```

---

## 常见错误与解决

### 9.1 构建阶段错误

| 错误信息 | 原因 | 解决 |
|----------|------|------|
| `failed to solve: circular dependency detected on stage: builder` | Dockerfile 错误使用 `COPY --from=builder` 从自身复制 | 改为 `COPY /app/...` 直接复制 |
| `unknown flag: start_period` | HEALTHCHECK 使用下划线而非连字符 | 改为 `--start-period` |
| `Additional property start-period is not allowed` | 旧版 Compose 不支持 `start-period` | 从 docker-compose.yml 移除该字段 |
| `WARN ... version is obsolete` | docker-compose.yml 使用废弃的 `version` 字段 | 删除 `version: '3.8'` 行 |
| `failed to solve: executor failed running [/bin/sh -no: such file or directory` | 基础镜像路径错误 | 确认 `FROM node:22-slim` 可用 |

### 9.2 运行时错误

| 错误信息 | 原因 | 解决 |
|----------|------|------|
| `❌ GATEWAY_URL 未设置` | 测试脚本 `.env` 变量未导出 | 修复脚本：`set -a && . .env && set +a`（无括号） |
| `Connection refused` 或 `Timeout` | Gateway 地址错误或网络不可达 | 检查 `GATEWAY_URL` 是否正确，确保网关运行 |
| `健康检查失败` | 容器启动慢或端口被占用 | 等待更长时间，或修改 `UI_PORT` |
| `Authentication failed` | `LOCAL_API_TOKEN` 不匹配 | 确保浏览器输入的 token 与 `.env` 一致 |
| `Permission denied` | 数据目录挂载权限问题 | 检查 `~/.openclaw` 目录权限为当前用户 |

### 9.3 配置错误

| 错误信息 | 原因 | 解决 |
|----------|------|------|
| `无法加载 .env 文件` | 语法错误、空格、BOM 编码 | 1. `bash -n .env` 检查语法<br>2. 删除空格 `KEY=value`<br>3. 转为 UTF-8 无 BOM |
| 变量为空但 `.env` 有值 | 脚本在子 shell 中加载 | 修改脚本：去掉括号，直接 `set -a && . .env` |
| `端口已被占用` | `UI_PORT` 被其他进程占用 | `netstat -tlnp | grep 4310` 查找并停止占用进程 |

---

## 最佳实践

### 10.1 配置管理

- ✅ **配置与构建分离**：环境变量在运行时传递，不嵌入镜像
- ✅ **使用 `.env.example`**：作为模板，`.env` 不提交版本控制
- ✅ **安全默认值**：`READONLY_MODE=true`, `LOCAL_TOKEN_AUTH_REQUIRED=true`
- ✅ **敏感配置**：`LOCAL_API_TOKEN` 必须设置为强随机串，不要用默认值

### 10.2 镜像构建

- ✅ **多阶段构建**：分离 builder 和 production，减少生产镜像大小
- ✅ **层缓存优化**：先复制 `package.json` 和 `pnpm-lock.yaml` 安装依赖
- ✅ **避免依赖污染**：生产阶段用 `pnpm install --prod` 仅安装运行时依赖
- ✅ **版本固定**：Node.js 使用 `node:22-slim`，pnpm 锁定版本 `pnpm@9`

### 10.3 数据与安全

- ✅ **只读挂载**：OpenClaw 数据目录使用 `:ro`，避免容器修改宿主机
- ✅ **持久化卷**：应用数据使用匿名卷 `/app/data`
- ✅ **端口限制**：默认绑定 `127.0.0.1`，外部访问需显式配置并防火墙保护
- ✅ **认证开启**：`LOCAL_TOKEN_AUTH_REQUIRED=true` 防止未授权访问

### 10.4 运维操作

- ✅ **使用 `docker compose`**：让 Compose 自动加载 `.env`，不手动 source
- ✅ **快速失败**：脚本使用 `set -e`，任何错误立即退出
- ✅ **日志输出**：使用颜色区分状态，关键步骤有明确提示
- ✅ **健康检查**：使用最简单的 `interval/timeout/retries` 保证兼容性

### 10.5 文档与维护

- ✅ **版本化文档**：每次重大修改更新文档版本号
- ✅ **故障记录**：将新问题及时加入"常见错误"章节
- ✅ **经验沉淀**：复杂问题解决后，提炼为最佳实践

---

## 📚 相关资源

- **本指南完整源码**: `memory/experience-docker.md`
- **部署文件模板**: `openclaw-control-center-deploy/`
- **Docker 官方文档**: https://docs.docker.com/
- **Docker Compose 文件参考**: https://docs.docker.com/compose/compose-file/
- **OpenClaw 文档**: https://docs.openclaw.ai

---

## 快速命令参考

```bash
# 1. 进入部署目录
cd ~/.openclaw/workspace-tech/openclaw-control-center-deploy

# 2. 配置环境变量（首次）
cp .env.example .env
# 编辑 .env，设置 GATEWAY_URL 和 LOCAL_API_TOKEN

# 3. 启动服务
docker compose up --build -d

# 4. 查看状态
docker compose ps
docker compose logs -f

# 5. 停止服务
docker compose down

# 6. 重启服务
docker compose restart
```

---

**版本历史**:
- v1.0 (2026-04-02): 初始版本，基于 OpenClaw Control Center 部署实战总结
- **2026-06-05** - 选择器测试：选 `gene_docker_compose_deploy` ✅（之前选 `gene_gep_repair_from_errors`）
