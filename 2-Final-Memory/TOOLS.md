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

#### 📦 a-stock-data skill（GitHub: simonlin1212/a-stock-data v2.1）

六层数据架构，21个端点，覆盖行情/研报/信号/新闻/基础数据/公告。

**数据源优先级**:
1. **mootdx** (TCP 7709) → K线+五档盘口+逐笔成交+财务快照+F10（不封IP）
2. **腾讯财经** (HTTP) → PE/PB/市值/换手率/涨跌停（GBK编码，字段43=振幅，46=PB）
3. **akshare** (Python) → 研报+一致预期+新闻+公告+龙虎榜+解禁+行业
4. **同花顺热点** (HTTP) → 当日强势股+题材归因reason tags（零鉴权73ms）
5. **同花顺hsgtApi** (HTTP) → 北向资金分钟级+自缓存历史
6. **百度股市通** (HTTP) → 概念板块归属+个股资金流向
7. **东财reportapi** (HTTP) → 研报列表+PDF下载

**快速调用示例**:
```python
# 腾讯实时行情
import urllib.request
url = "https://qt.gtimg.cn/q=sh600519,sz000001"
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read().decode("gbk")
# 字段[3]=当前价, [39]=PE, [44]=总市值, [46]=PB, [47]=涨停价

# 同花顺热点（当日强势股+题材归因）
import requests
url = "http://zx.10jqka.com.cn/event/api/getharden/date/2026-05-14/..."
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
df = pd.DataFrame(r.json()["data"])
# reason字段=题材归因tags

# 百度概念板块
url = "https://finance.pae.baidu.com/api/getrelatedblock?code=600519&market=ab&typeCode=all"
```

✅ mootdx v0.11.7 已安装 — TCP行情(K线/五档盘口/逐笔成交) + 财务快照 + F10（不封IP）
✅ akshare v1.18.41 已安装 — 个股资金流向/指数历史/涨停板/行业板块（部分接口网络偶尔超时）
✅ stockstats — ⚠️ Python 3.8 兼容性问题，暂不可用（不影响核心功能）

**mootdx 使用示例**:
```python
from mootdx.quotes import Quotes
client = Quotes.factory(market='std')

# 实时报价（返回DataFrame）
quotes = client.quotes(symbol=['600519', '000001'])
print(quotes[['code','price','last_close','open','high','low','vol','amount']])

# K线（返回DataFrame）
klines = client.bars(symbol='600519', category=4, offset=10)  # 4=日线
print(klines[['datetime','open','close','high','low','vol','amount']])

# 财务快照（返回DataFrame，37字段）
fin = client.finance(symbol='600519')
print(fin[['code','liutongguben','zongguben','eps','roe','profit','income']])

# F10公司资料
text = client.F10(symbol='600519', name='最新提示')
```

**腾讯财经字段索引（实测校准）**:
- 字段[3]=当前价, [39]=PE(TTM), [43]=振幅%, [44]=总市值(亿), [46]=PB, [47]=涨停价
- ⚠️ 网上很多教程把索引43写成PB，实测是振幅%，PB在索引46

#### ⚠️ 核心问题：东方财富 push2 接口行为异常（2026-05-15 实测）

| 调用方式 | push2 板块资金流向 | push2 指数行情 |
|---------|-------------------|---------------|
| curl | ❌ 无响应 | ❌ 无响应 |
| Python urllib | ❌ 连接被关闭 | ❌ 连接被关闭 |
| **web_fetch** | ✅ **可用**（需加大 maxChars） | ✅ **可用** |

**结论：东方财富 push2 接口只能通过 web_fetch 调用，不可用 curl/urllib。**
**使用时注意：maxChars 默认值可能不够，建议设为 5000+ 以获取完整数据。**

**其他接口实测状态（2026-05-15）：**
- ✅ **腾讯财经 API** — curl/web_fetch 都通，实时行情首选
- ✅ **akshare 个股资金流向** — 可用（返回近几日数据）
- ✅ **akshare 指数历史** — 可用
- ❌ **akshare 行业/概念板块** — 连接被关闭（依赖东方财富 HTTP 下游被封）
- ✅ **mootdx** — 可用（TCP 7709 协议，不受 HTTP 限制）

#### 降级策略（按优先级排序）

**优先级 1：web_fetch 调用东方财富 push2（唯一可用方式）**

```
web_fetch url="https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:3&fields=f2,f3,f4,f6,f12,f14,f62" maxChars=5000
```

**优先级 2：akshare 个股资金流向（可用）**

```python
import akshare as ak
df = ak.stock_individual_fund_flow(stock="600519", market="sh")
```

**优先级 3：akshare 指数历史（可用）**

```python
import akshare as ak
df = ak.stock_zh_index_daily(symbol="sh000001")
```

**优先级 4：搜索 + 网页抓取（最后手段）**

**绝对不能**：不写资金流向、不标注失败原因、复制上一份报告的数据。

#### 关键概念板块代码

- `m:90+t:3` = 行业板块
- `m:90+t:2` = 概念板块
- `m:90+t:1` = 地域板块

#### 重点关注的资金流向概念

- **融资融券**（杠杆资金态度）
- **深股通**（外资对深市态度）
- **MSCI中国**（国际资金态度）
- **富时罗素**（国际资金态度）
- **标准普尔**（大盘蓝筹资金态度）

### 三、各时段报告数据获取规范

| 报告 | 生成时间 | 市场状态 | 数据获取要求 |
|------|---------|---------|-------------|
| **早盘报告** | 09:10 | 盘前 | ① API获取昨日收盘数据（腾讯/东方财富）② Tavily搜索当日最新市场资讯、政策新闻 ③ **外围市场实时数据**（美股期货/港股早盘/A50期货/大宗）④ **昨日走势模式检查**（读取前日复盘，识别倒N字形等特殊模式）⑤ **资金流向前置检查**（腾讯财经板块资金）⑥ **前日资金流向连续性分析**（来自前日复盘）⑦ **期货市场监控**（碳酸锂/铜/原油/黄金）⑧ **科技股宽区间+止盈线双档制** |
| **午盘报告** | 12:15 | 午间休市 | ① API获取上午实时行情（最新快照）② **重新调用**资金流向API ③ 搜索上午市场热点 |
| **尾盘报告** | 14:30 | 盘中（未收盘） | ① API获取实时行情（标注"盘中数据"）② **重新调用**资金流向API ③ 搜索午后市场动态 ④ **尾盘加速预判量化**（方向判断+偏差区间+各基金预判+支撑压力位）⑤ **止盈条件动态调整量化**（触发条件+调整幅度+分级体系）⑥ **收盘前30分钟关键操作清单分级**（🔴必须/🟡建议/🟢可等）⑦ **新基金建仓推荐更新（场外基金）**：基于全天资金流向+尾盘实时数据，验证早盘/午盘推荐或新增推荐，**必须给场外基金代码，禁止给场内ETF代码** |
| **复盘报告** | 16:00 | 收盘后 | ① API获取**最终收盘数据** ② **重新调用**资金流向API ③ 对比三份报告的命中率 ④ **改进方案执行效果追踪量化**（逐条评估+应用率/有效率+闭环总结） |

### 四、数据标注规范

- **早盘报告**：标注"昨日收盘数据（来源：腾讯财经/东方财富API）"
- **午盘报告**：标注"午间实时数据（来源：腾讯财经/东方财富API）"
- **尾盘报告**：标注"**盘中实时数据，非最终收盘**（来源：腾讯财经/东方财富API）"
- **复盘报告**：标注"**最终收盘数据**（来源：腾讯财经/东方财富API）"

### 五、走势模式检查规范（2026-05-19 v3 更新）

**每次生成早盘报告前，必须执行走势模式检查：**

1. 读取前一交易日复盘报告 `daily-review-YYYY-MM-DD.md`
2. 识别昨日是否出现特殊走势模式：
   - **倒N字形**：早盘修复/反弹 → 午后冲高回落 → 尾盘跳水
   - **单边下跌**：全天持续走低，无明显反弹
   - **V字形**：早盘急跌 → 午后持续反弹
   - **缩量横盘**：全天窄幅震荡，成交额明显萎缩
3. 如果昨日出现特殊走势，早盘报告必须：
   - 将"走势延续"列为基准情景之一
   - 同时设置"走势反转"和"继续下跌"的预案
   - 大跌后的次日不能默认"修复反弹"，必须给出两种情景的概率评估
4. 连续两日出现相同模式（如连续两日倒N字形），必须提升风险预警等级
5. ⚠️ **新增：前日资金流向连续性分析**：提取前日复盘的主力资金净流入/流出TOP5板块，分析今日延续概率
6. ⚠️ **新增：期货市场监控**：碳酸锂/铜/原油/黄金期货，涨跌幅超3%必须标注对相关持仓影响
7. ⚠️ **新增：科技股宽区间设置**：强势科技股预判区间+1%~+5%（非+1%~+2%），弱势股-3%~0%

### 六、止盈条件动态调整规则（2026-05-19 v3 量化更新）

**止盈条件应为动态区间，非固定数值：**

1. 止盈条件设定时，同时给出"理想触发线"和"底线触发线"
   - 例：科创芯片理想止盈3.70，底线止盈3.60
2. 当市场大幅走弱时，应动态下调止盈线：
   - 下调触发阈值：指数较午间高点回落超过1%
   - 下调幅度：通常为理想值的5-10%
3. 下调后必须在报告中明确标注：
   - "⚠️ 止盈线已从3.70动态下调至3.65（市场走弱触发）"
4. 绝对不能固守早盘设定的数值不变
5. ⚠️ **新增量化触发条件（满足任一即触发下调）**：
   - 指数较午间高点回落超过1%
   - 持仓基金涨幅较午间预估回落超过0.5%
   - 市场出现重大利空消息
6. ⚠️ **新增量化调整规则**：
   - 理想止盈线 → 市场走弱时下调5-10%
   - 例：科创芯片午间设≥3.70减仓 → 若午后回落至3.56（跌3.8%），则动态调至≥3.62即可减仓
7. ⚠️ **新增止盈线分级体系（每个持仓都要有）**：
   - 理想触发线：市场强势时的目标
   - 底线触发线：市场走弱时的最低可接受值
   - 当前建议：基于当前市场状态的具体操作建议

### 七、尾盘加速预判规则（2026-05-19 v3 量化更新）

**尾盘报告必须包含量化尾盘加速预判：**

1. 尾盘加速方向判断：
   - 午后走强（指数较午间上涨）→ 尾盘大概率继续加速上涨
   - 午后走弱（指数较午间下跌）→ 尾盘可能加速下跌
   - 午后横盘（变化<0.2%）→ 尾盘大概率维持
2. ⚠️ **量化偏差区间（基于历史模式）**：
   - 午后走强：14:30→收盘可能再涨 +0.2%~0.5%（强势日可达+0.8%）
   - 午后走弱：14:30→收盘可能再跌 +0.3%~0.6%
   - 连续两日倒N字形：尾盘跳水概率>60%，偏差区间上调至 +0.5%~1.0%
3. ⚠️ **各持仓基金的尾盘偏差预判**：对每只基金给出尾盘偏差方向和收盘区间
   - 格式："科创AI 14:30估值+3.57%，尾盘加速概率高，收盘可能在+3.8%~+4.3%区间"
4. 关键支撑/压力位：预判加速下跌时列出跌破点位，预判加速上涨时列出突破点位
5. 如果预判尾盘加速下跌，必须同步调整操作建议：
   - 止损委托提前设好
   - 加仓计划推迟到次日

### 八、收盘前30分钟关键操作清单规则（2026-05-19 v3 新增）

**尾盘报告必须包含分级操作清单：**

1. 🔴 **必须收盘前执行（不可等到明天）**：
   - 止损委托设置（具体基金+具体价格）
   - 已触发止盈条件的减仓操作（具体基金+具体比例）
   - 跌破关键支撑位的应对操作
2. 🟡 **建议收盘前执行（如果条件允许）**：
   - 接近触发条件的预备操作
   - 资金调拨准备
3. 🟢 **可等收盘确认后执行**：
   - 加仓计划（说明收盘后确认什么条件才执行）
   - 明日操作预案（基于收盘数据的决策树）
4. ⚠️ **必须给出具体示例，不能只列框架**

### 八、数据验证

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

## 📧 邮件发送规则（最高优先级）

**⚠️ 永远不要用发件箱地址作为收件人！**

- 发件箱: `panbin5218@163.com`（仅用于SMTP发信，不是收件人）
- 收件人配置: `/root/.openclaw/share/send-email/recipients.yaml`
- 发送脚本: `/root/.openclaw/share/send-email/send_email_multi.py`
- 发送命令:
  ```bash
  cd /root/.openclaw/share/send-email
  python3 send_email_multi.py --group all --subject "标题" --html-file /path/to/report.html
  ```
- 收件人组 `all`: 主送 `panbin521@sina.com`（无抄送）
- 转换HTML: `python3 md_to_html.py input.md output.html`

**违规记录**: 2026-05-21 把发件箱地址当收件人发送，被老板纠正

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
