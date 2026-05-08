---
tags:
  - openclaw
---


```bash
# 查看版本
openclaw --version
openclaw status
openclaw status --all
openclaw status --deep  #带实时探测的深度诊断
openclaw status --usage # 看完整的provider用量明细
# (可以查看clawbot是否在后台运行)
openclaw health
openclaw onboard # 初始化向导
openclaw configure # 交互式配置
openclaw doctor  # 检查所有组件状态

# 重启网关
openclaw gateway restart
```

#### 配置相关
```bash
# 查看配置项
openclaw config get <key>
# 获取网关配置(如token、端口之类)
openclaw config get gateway
openclaw config get gateway.auth.token
openclaw config get gateway.controlUi.allowInsecureAuth

# 修改配置项
openclaw config set <key> <value> 
openclaw config set gateway.controlUi.allowInsecureAuth true
openclaw config set gateway.controlUi.allowedOrigins '["你的端口转发地址"]'

# 删除配置项
openclaw config unset <key> 

```



#### token配置
```bash
# 生成访问Token并查看
openclaw dashboard --no-open
openclaw config regenerate-token #命令错误的？
# 重置token
openclaw openclaw token reset
# 查看配置文件中的token字段
cat ~/.openclaw/openclaw.json | grep '"token":'
```

#### 设置openclaw建设公网
```bash
openclaw config set "gateway.bind" "lan"
openclaw config set "gateway.controlUi" '{"allowInsecureAuth" : true}'
#openclaw config set gateway.controlUi.allowedOrigins ["http://127.0.0.1:18789","http://192.168.1.200:18789"]

# 获取设备列表
openclaw devices list
# 授权指定设备
openclaw devices approve 76f81efa-c653-4c9d-8c80-e4eced5d89a4

# 局域网IP访问控制
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
openclaw config unset gateway.controlUi.dangerouslyDisableDeviceAuth

openclaw gateway restart
```

#### 配置通道channels(如QQ、飞书、钉钉)
```bash
openclaw channels list
openclaw config get channels
# 查看通道列表
openclaw plugins list | grep -i ddingtalk

# 安装钉钉
openclaw plugins install @largezhou/ddingtalk
# 钉钉配置(配置一项就自动重启？)
openclaw config set channels.ddingtalk.enabled true
openclaw config set channels.ddingtalk.clientId "dingcdkkaz567dcvympn"
openclaw config set channels.ddingtalk.clientSecret "evVZ3CKSmzBMQ4vrdtDC5ZKyUH3CDpQj7tU8PSM9yPFbvVAiwGBk1sM6axCpCV9t"

# 安装配置QQ
openclaw plugins install @sliverp/qqbot
openclaw config set channels.qqbot.enabled true
# 配置绑定当前QQ机器人(自动添加appId和clientSecret)
openclaw channels add --channel qqbot --token "1903088387:kQ1cDhyBICsKYcT9"

# 企业微信
openclaw plugins install @mocrane/wecom
openclaw plugins install @marshulll/openclaw-wecom
# 这里配置的是 app 模式，可以参考插件使用指南换成bot或者both模式
openclaw config set channels.wecom.mode "app"
openclaw config set channels.wecom.defaultAccount "app"
openclaw config set channels.wecom.accounts.app.mode "app"
openclaw config set channels.wecom.accounts.app.webhookPath "/wecom/app"
openclaw config set channels.wecom.accounts.app.corpId "你企业ID"
openclaw config set channels.wecom.accounts.app.corpSecret "应用secret"
openclaw config set channels.wecom.accounts.app.agentId "你的应用ID"
openclaw config set channels.wecom.accounts.app.callbackToken "你设置的应用的token"
openclaw config set channels.wecom.accounts.app.callbackAesKey "你设置的应用的aes-key"

# 飞书
openclaw plugins install @openclaw/feishu
```

#### 备份还原
```bash
# 一个命令归档整个本地状态
openclaw backup create
# 确认备份文件的完整性
openclaw backup verify
使用 --only-config选择性地备份您需要的部分。
# 备份 OpenClaw 配置文件：
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)
# 无脑全量备份：
cp -r ~/.openclaw ~/openclaw_bak_2026.03.24

# 解压
tar -xzvf openclaw-full-backup-20260311.tar.gz -C ~/
```

#### 设置自动更新（自动更新默认处于关闭状态）
```bash
  "update": {
    "channel": "stable",
    "auto": {
      "enabled": true,
      "stableDelayHours": 6,
      "stableJitterHours": 12,
      "betaCheckIntervalHours": 1
    }
  }
  
#更新通道说明:
stable (默认) 稳定版，推荐生产环境使用
beta	测试版，提前体验新功能
dev		开发版，最新但可能不稳定
```


