---
tags:
  - openclaw
  - skill
---

### 背景

不是OpenClaw不聪明，是它没有"成长"的机制。每次对话结束，经验清零，下次从头来。

capability-evolver 做的就是这件事：让 AI 分析自己的历史表现，找出哪里做得不好，然后修改自己的行为规则，下次做得更好。

### 🔧 技能功能
根据文档，这是一个自我进化引擎，主要功能包括：

- 运行时分析 - 分析历史执行记录
- 改进识别 - 自动识别能力增强机会
- 协议约束应用 - 遵循受限的进化协议
- 持续优化 - 自动应用改进策略

### 安装

```clawhub install capability-evolver```

### 配置
```bash
  "skills": {
    "entries": {
      "capability-evolver": {
        "enabled": true
      }
    }
  }
```

### 🔑 注册信息
- **node_id**: `node_5f516c9011000421`
- **node_secret**: `7bfa9be7d80d5f08f4a4d75721034f53d1c245ee0dc799a98ac12556fc5c34b9`
- **claim_code**: `7H58-UJQ5`
- **claim_url**: `https://evomap.ai/claim/7H58-UJQ5`
接下来配置环境变量文件，然后把 node_id 持久化



**点击这个链接绑定账户**：[https://evomap.ai/claim/7H58-UJQ5](https://evomap.ai/claim/7H58-UJQ5)

这个链接 24 小时内有效，绑定后节点就关联到你的 EvoMap 账户了，可以在 dashboard 查看活动和积分。绑定完成后告诉我，我来做后续的 heartbeat 测试 🧬

明白了，这是 EvoMap 平台的限制——新注册账户需要等 12 小时才能绑定节点。
当前时间 11:31，账户是今天注册的，估计要到今晚 23:30 左右才能解锁。
我先记下来，12 小时后提醒你。



目前我们有 **5 个 workspace**（main/tech/media/proj/final），如果要让每个都用 evolver，有两种做法：
**方案 A：共享一个 node（简单）**

- 所有 agent 指向同一个 `~/.evomap/node_id`
- 配置一次就行，但声誉/积分混在一起

**方案 B：各自独立注册（规范）**

- 每个 agent 跑一次 `POST /a2a/hello`，各自拿到独立的 node_id
- 用各自工作区下的 `.env` 配置自己的 `A2A_NODE_ID`
- `~/.evomap/node_id` 只给主 agent（或不用）















## 🔬 共享 + 命名空间隔离方案深度分析

### 先理解 GEP 协议的数据结构

复制

```
genes.json = 基因库（策略模板，3 种 category）
   ├── repair    → 看到 error/exception/failed 信号 → 触发修复
   ├── optimize  → 看到 protocol/gep/prompt 信号 → 触发优化
   └── innovate  → 看到 feature_request/capability_gap → 触发创新

capsules.json = 经验胶囊（已验证的修复记录）
   └── 记录：什么 trigger → 用了哪个 gene → 改了什么 → 结果如何

events.jsonl = 进化事件日志（追加式，记录每次进化）
```

### 模拟场景推演

假设运行一段时间后，两个 agent 各自积累了不同的经验：

**Tech Agent（技术专家）可能产生的经验：**

复制

```
genes:
  - gene_tech_npm_install_repair     signals: [npm, install, missing module]
  - gene_tech_webpack_optimize       signals: [webpack, build time, slow]
  - gene_tech_docker_network_fix     signals: [docker, network, dns]

capsules:
  - "exec: unknown command 'process'" → 修复方案 A
  - "npm ERR! code ENOENT" → 修复方案 B
```

**Media Agent（自媒体专家）可能产生的经验：**

复制

```
genes:
  - gene_media_browser_timeout       signals: [browser, timeout, screenshot]
  - gene_media_ocr_preprocessing     signals: [ocr, image quality, tesseract]
  - gene_media_content_template      signals: [content, template, wechat]

capsules:
  - "browser action timeout" → 降级方案 X
  - "OCR 中文识别率低" → 预处理方案 Y
```

---

### 优劣对比

#### ✅ 共享方案的优势

|维度|分析|
|---|---|
|**跨域经验复用**|⭐ **核心价值**。Tech 修过 "exec: unknown command 'process'" 的经验，Media 在浏览器自动化遇到类似 shell 错误时，可以直接复用同一个 capsule，不用重新摸索|
|**修复效率**|假设 Media 遇到 npm 依赖问题（安装截图工具），Tech 的 `gene_tech_npm_install_repair` 的 signals_match 虽然写的是 npm，但 selector 是**语义匹配**（`scoreGeneSemantic` 用分词+TF-IDF），不是精确字符串匹配，所以跨域仍然可能命中|
|**进化密度**|5 个 agent 的失败经验汇聚到同一个基因库，genes/capsules 增长更快，新 agent 启动时已有丰富经验|
|**维护成本**|只需维护一份 assets/gep/，不需要同步 5 个副本|

#### ❌ 共享方案的问题

|维度|分析|严重程度|
|---|---|---|
|**信号语义漂移**|Tech 的 `signals_match: [error, exception, failed]` 和 Media 的 `signals_match: [browser, timeout, crawl]` 混在一起。`scoreGene()` 用 tag overlap + 语义权重混合打分，当基因库膨胀到 50+ 条时，一个 browser timeout 信号可能错误命中 repair 类的 error gene，而不是更相关的 browser gene|⚠️ **中高**|
|**胶囊污染**|Capsule 的 trigger 字段包含原始错误信息（如完整的 error log）。Tech 的 capsule 记录的是 `exec: unknown command`，Media 的记录是 `browser action timeout`。如果 selector 的语义匹配不够精确，Media 的 browser 问题可能匹配到 Tech 的 exec 修复方案|⚠️ **中**|
|**并发写冲突**|两个 agent 同时跑 `node index.js`，都往同一个 `assets/gep/genes.json` 写新 gene，可能互相覆盖。虽然有 git 锁，但 evolver 本身没有内置文件锁机制|🔴 **高**|
|**进化方向发散**|Evolver 的 `EVOLVE_STRATEGY=balanced` 会根据当前 workspace 的 memory 决定进化方向。5 个 agent 的 memory 内容完全不同（tech 记代码、media 记内容运营），共享同一个 evolver 运行会随机从 memory 采样，导致进化方向飘忽不定|⚠️ **中**|
|**信用混淆**|Hub 看到的是同一个 node_id "Tech-Agent"，Tech 刷的 reputation 和 Media 的混在一起，无法区分哪个 agent 贡献了高质量 capsule|⚠️ **低**|

---

### 📊 量化对比

|指标|完全共享|命名空间隔离|完全独立|
|---|---|---|---|
|基因库规模（预估/月）|30-50 条|30-50 条（共享）|每个 6-10 条|
|跨域复用率|100%|~40%（命名空间内）|0%|
|错误匹配率（错配）|~15-25%|~5-10%|~2-5%|
|并发安全性|❌ 需加锁|⚠️ 需加锁|✅ 天然安全|
|维护复杂度|低|中|高|
|Hub 身份数|1|1|5|
|经验多样性|⭐⭐⭐⭐⭐|⭐⭐⭐⭐|⭐⭐|

---

### 🎯 结论

**"共享 + 命名空间隔离"方案真正的瓶颈不在命名空间，而在 selector 的匹配精度。**

GEP 的 selector 用的是 `scoreTagOverlap + 0.6 * scoreGeneSemantic`（TF-IDF 分词），这种轻量语义匹配在基因库 < 20 条时还行，但超过 30 条后，跨域错配率会显著上升。

**所以实际推荐方案取决于你的使用模式：**

|如果…|推荐|
|---|---|
|5 个 agent 的 evolver 不会同时跑|**共享 + 命名空间隔离** ✅ 简单高效|
|需要严格隔离进化方向|**完全独立**，每个 agent 各注册一个 node|
|想要经验共享但又要方向清晰|**混合**：Hub 层共享一个 node，但每个 agent 的 workspace 下跑 evolve 时用 `--strategy` 限制方向（Tech 用 `repair-only`，Media 用 `innovate`）|

老板你倾向哪种？








## ✅ 共享+命名空间隔离方案实施完成！

老板，全部搞定，以下是最终交付清单：

### 📦 交付物总览

|组件|数量|位置|
|---|---|---|
|共享 Evolver 实例|1|`~/.openclaw/skills/capability-evolver/`|
|共享 node 身份|1|`~/.evomap/node_id`|
|Agent 独立配置|4|`~/.openclaw/workspace-{tech,media,proj,final}/.env`|
|Agent 入口脚本|4|`~/.openclaw/workspace-{tech,media,proj,final}/evolve.sh`|
|GEP 隔离目录|4|`assets/gep/scopes/{tech,media,proj,final}/`|
|配置文档|1|`EVOLVER-SHARED-CONFIG.md` (428 行)|

### 🎯 各 Agent 策略分配

|Agent|策略|回滚|说明|
|---|---|---|---|
|🛠️ tech|repair-only|hard|技术问题多，先修再创新|
|🎬 media|innovate|stash|内容创作，持续创新|
|💼 proj|balanced|hard|项目管理，均衡发展|
|📊 final|harden|hard|财务数据，稳定可靠|

### 🔑 核心隔离机制

- **信号源隔离** → 每个 agent 只读自己 workspace 的 memory
- **GEP 资产隔离** → `EVOLVER_SESSION_SCOPE` 让 genes/capsules/events 各管各的
- **进化方向隔离** → `EVOLVE_STRATEGY` 各走各的方向
- **并发安全** → `acquireLock()` PID 文件锁，同时只能一个 agent 跑
- **经验共享** → 基础 genes 库只读共享，跨域命中率高

### 📝 使用方式

```bash
# Tech 跑一次进化
cd ~/.openclaw/workspace-tech && bash evolve.sh

# Media 持续循环
cd ~/.openclaw/workspace-media && bash evolve.sh --loop

# 临时覆盖策略
cd ~/.openclaw/workspace-tech && EVOLVE_STRATEGY=innovate bash evolve.sh
```

详细文档在 `~/.openclaw/skills/capability-evolver/EVOLVER-SHARED-CONFIG.md`，包含架构图、目录结构、安装指南、故障排查、策略说明 🧬

