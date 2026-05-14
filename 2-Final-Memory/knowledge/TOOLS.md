# TOOLS.md - 财务总监工具集

## 可用工具

| 工具 | 用途 | 备注 |
|------|------|------|
| read/write/edit | 文件操作 | 仅限工作区内 |
| exec | Shell 命令 | 仅限工作区相关、数据分析 |
| web_search | 网页搜索 | 默认 Tavily |
| web_fetch | 抓取网页 | 备用，可能受网络限制 |
| browser | 浏览器自动化 | 复杂页面交互 |
| sessions_send | 向 main 汇报 | 任务完成/问题报告 |
| feishu_* | 飞书集成 | 需 main 审批 |
| akshare-finance | 金融数据 | A股、基金、期货 |
| tavily_search | Tavily 搜索 | 财经资讯 |
| image | 图片分析 | ⚠️ 当前不可用（sharp 模块缺失），降级为 tesseract OCR |
| tesseract OCR | 图片文字识别 | `apt-get install tesseract-ocr tesseract-ocr-chi-sim`，中文识别需 chi_sim 语言包 |
| baidu-web-search | 百度千帆搜索 | 需 BAIDU_API_KEY（已在 .env 配置），中文搜索精准 |
| multi-search-engine | 17引擎聚合搜索 | 无需 API Key，7个国内 + 9个国际 + WolframAlpha |

## ⚠️ 工具降级

| 场景 | 降级方案 |
|------|---------|
| `read` 不可用 | `exec cat` |
| `write` 不可用 | `exec tee` / `exec cat >` |
| `edit` 不可用 | `exec sed -i` / python3 |
| `web_search` 不可用 | `browser` 工具 |
| `image` 不可用 | **tesseract OCR** + Python PIL 预处理 |

**原则**: 工具不可用时，第一反应是找替代方案，不是报错放弃。

---

## 📊 市场数据获取方案（最高优先级）

### ⚠️ 核心规则

1. **所有市场数据必须通过 API 获取，禁止仅依赖搜索或 Tavily**
2. **资金流向数据每次必须重新查询，禁止复制上一份报告的数据**
3. **数据获取优先级：腾讯财经 > 东方财富 > akshare > Tavily（仅作为最后手段）**

### 一、指数实时行情

**优先级 1：腾讯财经 API**（推荐，更新最快）

```bash
# 获取四大指数实时行情
web_fetch "https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688"
```

返回格式解析（以 `;` 分隔各指数，`~` 分隔字段）：
- 字段[3] = 当前价
- 字段[4] = 昨收价
- 字段[5] = 今开价
- 字段[6] = 成交量（手）
- 字段[31] = 涨跌额
- 字段[32] = 涨跌幅
- 字段[33] = 最高价
- 字段[34] = 最低价
- 字段[37] = 成交额（元）
- 字段[44] = 时间戳（YYYYMMDDHHmmss）

**优先级 2：东方财富 API**

```bash
# 获取四大指数实时行情
web_fetch "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f6,f12,f14&secids=1.000001,0.399001,0.399006,1.000688"
```

返回 JSON 格式：
- `f2` = 当前价
- `f3` = 涨跌幅
- `f4` = 涨跌额
- `f6` = 成交额
- `f12` = 代码
- `f14` = 名称

**优先级 3：akshare（备用）**

```python
import akshare as ak
df = ak.stock_zh_a_spot_em()
# 从 DataFrame 中筛选上证、深成、创业板、科创50
```

### 二、板块资金流向

**每次报告必须重新调用，禁止复用旧数据！**

```bash
# 东方财富概念板块资金净流入TOP10（行业板块）
web_fetch "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:3&fields=f2,f3,f4,f6,f12,f14,f62"

# 东方财富概念板块资金净流入TOP10（概念板块）
web_fetch "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f2,f3,f4,f6,f12,f14,f62"

# 东方财富概念板块资金净流入TOP10（地域板块）
web_fetch "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:1&fields=f2,f3,f4,f6,f12,f14,f62"
```

关键概念板块代码：
- `m:90+t:3` = 行业板块
- `m:90+t:2` = 概念板块
- `m:90+t:1` = 地域板块

重点关注的资金流向概念：
- **融资融券**（杠杆资金态度）
- **深股通**（外资对深市态度）
- **MSCI中国**（国际资金态度）
- **富时罗素**（国际资金态度）
- **标准普尔**（大盘蓝筹资金态度）

### 三、各时段报告数据获取规范

| 报告 | 生成时间 | 市场状态 | 数据获取要求 |
|------|---------|---------|-------------|
| **早盘报告** | 09:10 | 盘前 | ① API获取昨日收盘数据（腾讯/东方财富）② Tavily搜索当日最新市场资讯、政策新闻、外围市场 |
| **午盘报告** | 12:15 | 午间休市 | ① API获取上午实时行情（最新快照）② **重新调用**资金流向API ③ 搜索上午市场热点 |
| **尾盘报告** | 14:30 | 盘中（未收盘） | ① API获取实时行情（标注"盘中数据"）② **重新调用**资金流向API ③ 搜索午后市场动态 |
| **复盘报告** | 16:00 | 收盘后 | ① API获取**最终收盘数据** ② **重新调用**资金流向API ③ 对比三份报告的命中率 |

### 四、数据标注规范

- **早盘报告**：标注"昨日收盘数据（来源：腾讯财经/东方财富API）"
- **午盘报告**：标注"午间实时数据（来源：腾讯财经/东方财富API）"
- **尾盘报告**：标注"**盘中实时数据，非最终收盘**（来源：腾讯财经/东方财富API）"
- **复盘报告**：标注"**最终收盘数据**（来源：腾讯财经/东方财富API）"

### 五、数据验证

当两个API数据不一致时：
1. 以腾讯财经为准（更新最快）
2. 记录差异并标注
3. 如差异超过0.5%，需人工核实

---

## 操盘纪律

### 8层仓位规则

| 风险等级 | 品种 | 仓位上限 |
|---------|------|---------|
| 低风险 | 债券/货币基金 | ≤ 30% |
| 中风险 | 混合/指数基金 | ≤ 20% |
| 高风险 | 股票/期货/杠杆 | ≤ 10% |

### 止损规则

- 单笔 > 5% → 立即止损
- 连续3次亏损 → 暂停+重新评估
- 重大 > 10% → 立即报告 main

---

## 使用规则

1. 所有文件操作必须在 `~/.openclaw/workspace-final/` 内
2. 严禁修改 `~/.openclaw/openclaw.json`
3. 每笔建议必须包含风险评估
4. 重大操作需 main 确认
5. 操盘记录严格保密

---

## 记忆系统

### 查询优先级

1. **Obsidian vault**: `/home/obsidian_vault/2-Final-Memory/`
2. **当日日志**: `memory/YYYY-MM-DD.md`
3. **网络搜索**: 最后手段

### QMD 检索

```bash
# BM25 全文搜索
qmd search "关键词" -c share --max-results 3
qmd search "仓位规则" -c final-daily --max-results 5

# 查看集合
qmd ls
```

### Obsidian 路径

- 每日记忆: `2-Final-Memory/daily/YYYY-MM-DD.md`
- 长期记忆: `2-Final-Memory/MEMORY.md`
- 专项经验: `2-Final-Memory/knowledge/`
- 共享文档: `/home/obsidian_vault/shared/`

---

## sessions_send 模板

**任务完成**:

```
sessions_send "✅ 任务完成：<名称>
- 关键结果：<数据>
- 风险评估：<等级>
- 下一步：<建议>"
```

**问题报告**:
```
sessions_send "⚠️ 问题：<描述>
- 紧急程度：<高/中/低>
- 需要协助：<需求>"
```

**汇报频率**: 重大决策实时 / 每日总结 / 异常立即

---

## akshare 使用

```python
# Python 脚本方式调用
import akshare as ak
# A股行情
df = ak.stock_zh_a_spot_em()
# 基金净值
df = ak.fund_etf_fund_info_em(fund="000217")
```

**频率控制**: 每5分钟最多1次查询

---

## 搜索引擎优先级

1. ✅ **baidu-web-search** — 中文搜索首选（百度千帆 API，精准）
2. ✅ **multi-search-engine** — 多引擎聚合（无需 Key，中英文自动分流）
3. ✅ **tavily_search** — 国际搜索 + 财经资讯
4. ⚠️ **web_fetch** — 直接抓取，备用
5. ❌ 避免 curl 直接抓财经网站（易被拦截）

**注意**：搜索仅用于获取市场资讯、政策新闻、外围市场行情。**指数和资金流向数据必须通过 API 获取，不可依赖搜索结果。**

---

## tesseract OCR 使用指南

安装：
```bash
apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra
pip3 install pytesseract  # 可选，命令行方式不需要
```

Python 预处理 + OCR 模板：
```python
from PIL import Image, ImageFilter, ImageEnhance
import subprocess

def ocr_image(img_path, top=0, bottom=None, scale=3, contrast=1.8):
    img = Image.open(img_path)
    w, h = img.size
    crop = img.crop((0, top, w, bottom or h))
    # 放大
    crop = crop.resize((w * scale, (bottom or h) - top * scale), Image.LANCZOS)
    # 锐化 + 对比度增强
    crop = crop.filter(ImageFilter.SHARPEN)
    crop = ImageEnhance.Contrast(crop).enhance(contrast)
    crop.save('/tmp/ocr_temp.png')
    # OCR
    result = subprocess.run(
        ['tesseract', '/tmp/ocr_temp.png', 'stdout', '-l', 'chi_sim+eng', '--psm', '6'],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout
```

### 长截图 OCR 最佳实践

1. **分段裁剪**：每段 ~1200px 高度
2. **放大 3x** + **锐化** + **对比度增强 1.8x**
3. **逐段识别**后汇总
4. 整图识别效果差，必须分段

### **适用场景**

1. 持仓截图识别
2. 图片文字提取
3. image 工具不可用时的降级方案

## baidu-web-search

- **来源**：ClawHub — `clawhub install baidu-web-search`
- **作用**：百度千帆 API 中文搜索，精准度高
- **需要 API Key**：是，需 `BAIDU_API_KEY`（已在 `/root/.openclaw/.env` 配置）
- **使用方式**：`cd /root/.openclaw/skills/baidu-web-search && node scripts/search.js "查询内容" [条数]`
- **适用场景**：中文搜索、实时新闻、政策查询、事实核查

## multi-search-engine

- **来源**：ClawHub — `clawhub install multi-search-engine`
- **作用**：17个搜索引擎聚合（7国内 + 9国际 + WolframAlpha）
- **需要 API Key**：否，完全基于 web_fetch
- **适用场景**：中英文自动分流、多引擎交叉验证
