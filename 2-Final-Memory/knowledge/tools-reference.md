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

1. ✅ **Tavily** (web_search / tavily_search) — 首选
2. ⚠️ **web_fetch** — 备用
3. ❌ 避免直接 curl 抓取财经网站（易被拦截）

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

**适用场景**: 持仓截图识别、图片文字提取、image 工具不可用时的降级方案
