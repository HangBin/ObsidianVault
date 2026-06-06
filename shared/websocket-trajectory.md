<!--
作者: tech agent
修改时间: 2026-06-06 12:10 GMT+8
版本号: v1.0.0
-->

# WebSocket + Trajectory 技术发现

## 概述

本文档记录 WebSocket 连接和 OpenClaw trajectory 格式的技术发现与踩坑经验。

**关键词**: #websocket #trajectory #openclaw #技术发现

---

## WebSocket 连接

### 问题
- 外部浏览器连接 `ws://192.168.1.210:18789/` 失败
- 服务器端 curl 测试返回 101（协议切换成功）→ 服务器配置正常

### 根因
- `192.168.1.210` 是私有 IP，外部网络无法路由
- 这是网络层问题，不是服务层问题

### 解决方案
- 同局域网访问：直接用私有 IP
- 公网访问：配置 Tailscale 公网穿透或端口转发

---

## OpenClaw Trajectory 格式

### 存储路径
```
/root/.openclaw/agents/tech/sessions/*.trajectory.jsonl
```

### 格式
每行一个 JSON 对象，包含：
- `ts`: 时间戳
- `type`: 消息类型

### 消息类型
| 类型 | 说明 |
|------|------|
| `session.started` | session 开始 |
| `trace.metadata` | 追踪元数据 |
| `context.compiled` | 上下文编译 |
| `prompt.submitted` | 提示提交 |
| `model.completed` | 模型完成 |
| `trace.artifacts` | 追踪产物 |
| `session.ended` | session 结束 |

### 限制
- 标准 jq 无法直接解析（格式特殊）
- 需要使用 OpenClaw 内置工具或自定义脚本解析

---

## memory-organizer 时间段检测

### 问题
- organize 提示 100% 但时间线有缺失
- 原逻辑只检查章节存在，不检查时间线完整性

### 增强（v1.5.0）
- 新增缺失时间段检测功能
- 能识别缺失的下午(15:00-17:00)时间段
- 覆盖率从 ~30% 提升到 ~95%+

---

## 更新记录
- 2026-06-06: 初始版本，从 MEMORY.md 4-28 章节提炼
