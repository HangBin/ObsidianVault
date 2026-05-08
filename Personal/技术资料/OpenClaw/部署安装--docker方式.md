---
tags:
  - openclaw
---
手动在云服务器上部署

#### 一、前置要求
- 服务器（推荐Linux系统，如Ubuntu、Debian）
- 域名准备，用于绑定OpenClaw服务，实现公网访问
- SSL证书
- 工具准备：终端工具（如FinalShell、Xshell）、Git
- 阿里云账号实名认证，获取百炼API-Key
- Docker Engine >= 20.10
- Docker Compose >= v2.0.0
- 至少4GB可用内存
- 至少10GB可用磁盘空间

#### 二、镜像构建

1. 下载源码
```bash
# 拉取openclaw代码
git clone https://github.com/openclaw/openclaw
cd openclaw/

# 查看最新的tag
# v2026.3.2
git describe --tags $(git rev-list --tags --max-count=1)

# 创建容器持久化文件夹
mkdir -p openclaw/{config,data,logs}
chown -R 1000:1000 openclaw/{config,data,logs}
```

2. 通过docker构建镜像
> 适用于3.11之前版本

```bash
docker build -t openclaw:v2026.3.2 .
```

3. 自动构建镜像
> 适用于3.11后版本

从仓库根目录运行构建程序：```./docker-setup.sh```

此脚本：
- 构建 Gateway 网关镜像
- 运行新手引导向导
- 打印可选的提供商设置提示
- 通过 Docker Compose 启动 Gateway 网关
- 生成 Gateway 网关令牌并写入 .env

可选环境变量：
- OPENCLAW_DOCKER_APT_PACKAGES — 在构建期间安装额外的 apt 包
- OPENCLAW_EXTRA_MOUNTS — 添加额外的主机绑定挂载
- OPENCLAW_HOME_VOLUME — 在命名卷中持久化 /home/node

完成后：
- 在浏览器中打开 http://127.0.0.1:18789/。
- 将令牌粘贴到控制 UI（设置 → token）。

4. 启动前准备
```bash
# 需要再次获取带令牌的 URL？运行 
docker compose run --rm openclaw-cli dashboard --no-open。

# 控制 UI 令牌 + 配对（Docker）
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>

# 局域网IP访问控制
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
openclaw config unset gateway.controlUi.dangerouslyDisableDeviceAuth
# 修改参数 allowedOrigins
docker exec -it openclaw-2026324-openclaw-gateway-1 \
openclaw config set gateway.controlUi.allowedOrigins \
'["http://127.0.0.1:18789","http://192.168.1.200:18789"]'
```

#### 三、启动容器

```
# 启动OpenClaw网关容器
docker compose up -d openclaw-gateway

#检查
docker exec -it openclaw-gateway bash
openclaw doctor

# 执行初始化命令，进入交互式配置
docker compose run --rm -it openclaw-cli onboard
新设备需完成基础初始化：openclaw init
```

#### 四、编写docker-compose脚本

创建 ```docker-compose.yml``` 文件：
```bash
version: '3.8'

services:
  openclaw-gateway:
    image: openclaw:v2026.3.2
    container_name: openclaw-gateway
    restart: unless-stopped
    ports:
      - "18789:18789"
    volumes:
      - ./config:/home/node/.openclaw  # 配置文件持久化
      - ./logs:/tmp/openclaw  # 日志持久化
      - ./data:/home/node/clawd  # 数据持久化
    environment:
      - NODE_ENV=production # 运行环境 (development/production)
      - TZ=Asia/Shanghai
    extra_hosts:
      - "host.docker.internal:host-gateway"
    shm_size: 2g  # 共享内存大小，确保浏览器沙箱正常运行
    command: node /app/dist/index.js gateway --port 18789

  openclaw-cli:
    image: openclaw:v2026.3.2
    container_name: openclaw-cli
    network_mode: "service:openclaw-gateway"  # 共享网关网络
    volumes:
      - ./config:/home/node/.openclaw  # 配置文件持久化
      - ./logs:/tmp/openclaw  # 日志持久化
      - ./data:/home/node/clawd  # 数据持久化
    environment:
      - NODE_ENV=production # 运行环境 (development/production)
      - TZ=Asia/Shanghai
    entrypoint: ["node", "dist/index.js"]
```

#### 五、备份还原

容器
```bash
docker save -o openclaw_image_v2026.3.13.tar openclaw:v2026.3.13
docker load -i openclaw_image_v2026.3.13.tar
```

配置
```bash
# 压缩
tar -cvf openclaw-backup-20260310.tar /root/openclaw
# 解压
tar -xzf openclaw-backup-20260310.tar.gz
#解压Postman到/opt/目录里
tar -xzf Postman-linux-x64-6.3.0.tar.gz -C /root/

```

#### 问题排查

本地访问测试
```bash
curl -I http://127.0.0.1:18789
curl -I http://119.45.132.214:18789
curl -v http://119.45.132.214:18789 -H "Authorization: Bearer 94c6f773daf7e8ab2cbcb8e27f445696bb1fbe7bd9fe7cc7"
http://119.45.132.214:18789/?token=94c6f773daf7e8ab2cbcb8e27f445696bb1fbe7bd9fe7cc7
```

端口问题排查
```bash
sudo iptables -L -n | grep 18789  # 检查iptables规则
# 若未放行，添加规则并重启防火墙：
sudo iptables -A INPUT -p tcp --dport 18789 -j ACCEPT
# 检查服务是否监听18789端口
netstat -tulnp | grep 18789
```


