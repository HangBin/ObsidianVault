#!/usr/bin/env python3
"""
A股报告数据采集脚本 - 并行采集所有数据，输出JSON
支持报告类型: morning(早盘) / afternoon(午盘) / tail(尾盘)

用法:
  python3 collect_report_data.py --type morning --output /tmp/morning_data.json
  python3 collect_report_data.py --type afternoon --output /tmp/afternoon_data.json
  python3 collect_report_data.py --type tail --output /tmp/tail_data.json
"""
import concurrent.futures
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
TIMEOUT = 15  # 单次请求超时(秒)
PORTFOLIO_PATH = Path("/home/obsidian_vault/2-Final-Memory/portfolio.md")

# ── 工具函数 ──────────────────────────────────────────
def web_fetch(url, encoding="utf-8"):
    """通用web_fetch，返回文本内容"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                return data.decode("gbk", errors="replace")
    except Exception as e:
        return f"ERROR: {e}"


def parse_tencent_index(text):
    """解析腾讯财经四大指数"""
    if text.startswith("ERROR"):
        return {"error": text}
    result = {}
    for item in text.strip().split(";"):
        if "~" not in item:
            continue
        code_match = re.search(r'v_(\w+)="', item)
        if not code_match:
            continue
        code = code_match.group(1)
        fields = item.split("~")
        if len(fields) < 40:
            continue
        try:
            result[code] = {
                "name": fields[1], "code": fields[2],
                "price": float(fields[3]), "last_close": float(fields[4]),
                "open": float(fields[5]), "vol": fields[6],
                "change": float(fields[31]), "change_pct": float(fields[32]),
                "high": float(fields[33]), "low": float(fields[34]),
                "amount": float(fields[37]) if fields[37] else 0,
            }
        except (ValueError, IndexError):
            continue
    return result


def parse_tencent_funds(text):
    """解析腾讯财经基金净值（批量）"""
    if text.startswith("ERROR"):
        return {"error": text}
    result = {}
    for line in text.strip().split(";"):
        if "~" not in line or not line.strip():
            continue
        code_match = re.search(r'v_(\w+)="', line)
        if not code_match:
            continue
        code = code_match.group(1)
        fields = line.split("~")
        if len(fields) < 35:
            continue
        try:
            result[code] = {
                "name": fields[1], "code": fields[2],
                "nav": float(fields[3]), "last_nav": float(fields[4]),
                "change_pct": float(fields[32]) if len(fields) > 32 else 0,
            }
        except (ValueError, IndexError):
            continue
    return result


def parse_peripheral(text):
    """解析外围市场"""
    if text.startswith("ERROR"):
        return {"error": text}
    result = {}
    for line in text.strip().split(";"):
        if "~" not in line or not line.strip():
            continue
        code_match = re.search(r'v_(\w+)="', line)
        if not code_match:
            continue
        code = code_match.group(1)
        fields = line.split("~")
        if len(fields) < 35:
            continue
        try:
            result[code] = {
                "name": fields[1], "price": float(fields[3]),
                "change_pct": float(fields[32]) if len(fields) > 32 else 0,
            }
        except (ValueError, IndexError):
            continue
    return result


def extract_portfolio_codes(portfolio_path=PORTFOLIO_PATH):
    """从portfolio.md提取当前持仓区基金代码（不含长期关注区）"""
    try:
        content = portfolio_path.read_text(encoding="utf-8")
        in_holding = False
        codes = []
        for line in content.split("\n"):
            if "🟢 持仓区" in line or "🏆 贵金属" in line or "🛡️ 债券" in line:
                in_holding = True
            elif "长期关注区" in line or "已清仓" in line:
                in_holding = False
            elif in_holding and "|" in line:
                matches = re.findall(r'\b(\d{6})\b', line)
                for m in matches:
                    if m not in codes:
                        codes.append(m)
        return codes
    except Exception as e:
        return []


def fetch_fund_nav(codes):
    """天天基金批量获取基金净值"""
    result = {}
    for code in codes:
        url = f"https://fundgz.1234567.com.cn/js/{code}.js"
        text = web_fetch(url)
        if text.startswith("ERROR"):
            result[code] = {"error": text}
            continue
        try:
            json_str = text[text.index("(")+1:text.rindex(")")]
            data = json.loads(json_str)
            result[code] = {
                "name": data.get("name", ""), "code": data.get("fundcode", code),
                "nav": float(data.get("dwjz", 0)),
                "estimated_nav": float(data.get("gsz", 0)),
                "estimated_change_pct": float(data.get("gszzl", 0)),
                "nav_date": data.get("jzrq", ""),
            }
        except Exception as e:
            result[code] = {"error": str(e)}
    return result


# ── 采集函数 ──────────────────────────────────────────
def collect_index():
    """腾讯财经四大指数"""
    url = "https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688"
    return parse_tencent_index(web_fetch(url, encoding="gbk"))


def collect_fund_flow_concept():
    """东方财富push2概念板块资金流向 — 需通过OpenClaw web_fetch调用"""
    return {
        "_needs_web_fetch": True,
        "url": "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=15&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:3&fields=f2,f3,f4,f6,f12,f14,f62",
        "note": "东方财富push2需通过OpenClaw web_fetch调用"
    }


def collect_fund_flow_industry():
    """东方财富push2行业板块资金流向 — 需通过OpenClaw web_fetch调用"""
    return {
        "_needs_web_fetch": True,
        "url": "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f2,f3,f4,f6,f12,f14,f62",
        "note": "东方财富push2需通过OpenClaw web_fetch调用"
    }


def collect_valuation():
    """天天基金持仓估值"""
    codes = extract_portfolio_codes()
    if not codes:
        return {"error": "无法提取基金代码"}
    return fetch_fund_nav(codes)


def collect_peripheral():
    """外围市场：港股/美股"""
    url = "https://qt.gtimg.cn/q=hk00HSI,usr_ixic,usr_dji,usr_spx,hk00HSCEI"
    result = parse_peripheral(web_fetch(url, encoding="gbk"))
    url2 = "https://qt.gtimg.cn/q=hf_GC,hf_CL"
    result.update(parse_peripheral(web_fetch(url2, encoding="gbk")))
    return result


def collect_yesterday_index():
    """腾讯财经昨日收盘数据（用于复盘）"""
    # 与collect_index相同，但语义上区分"昨日收盘"和"今日实时"
    return collect_index()


# ── 报告类型配置 ──────────────────────────────────────
REPORT_CONFIGS = {
    "morning": {
        "name": "早盘报告",
        "collectors": {
            "index": collect_index,          # 昨日收盘数据（盘前获取的是昨日收盘）
            "fund_flow_concept": collect_fund_flow_concept,  # 需web_fetch
            "fund_flow_industry": collect_fund_flow_industry,  # 需web_fetch
            "valuation": collect_valuation,  # 持仓最新净值
            "peripheral": collect_peripheral,  # 外围市场
        },
        "web_fetch_required": ["fund_flow_concept", "fund_flow_industry"],
    },
    "afternoon": {
        "name": "午盘报告",
        "collectors": {
            "index": collect_index,          # 上午实时行情
            "fund_flow_concept": collect_fund_flow_concept,  # 需web_fetch
            "fund_flow_industry": collect_fund_flow_industry,  # 需web_fetch
            "valuation": collect_valuation,  # 持仓实时估值
            "peripheral": collect_peripheral,
        },
        "web_fetch_required": ["fund_flow_concept", "fund_flow_industry"],
    },
    "tail": {
        "name": "尾盘报告",
        "collectors": {
            "index": collect_index,          # 盘中实时行情
            "fund_flow_concept": collect_fund_flow_concept,  # 需web_fetch
            "fund_flow_industry": collect_fund_flow_industry,  # 需web_fetch
            "valuation": collect_valuation,  # 持仓实时估值
            "peripheral": collect_peripheral,
        },
        "web_fetch_required": ["fund_flow_concept", "fund_flow_industry"],
    },
    "review": {
        "name": "复盘报告",
        "collectors": {
            "index": collect_index,          # 最终收盘数据
            "fund_flow_concept": collect_fund_flow_concept,  # 需web_fetch
            "fund_flow_industry": collect_fund_flow_industry,  # 需web_fetch
            "valuation": collect_valuation,  # 收盘净值
            "peripheral": collect_peripheral,
        },
        "web_fetch_required": ["fund_flow_concept", "fund_flow_industry"],
    },
}


# ── 主流程 ────────────────────────────────────────────
def main():
    start = time.time()

    # 解析参数
    report_type = "tail"  # 默认尾盘
    output_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            report_type = sys.argv[i + 1]
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]

    if report_type not in REPORT_CONFIGS:
        print(f"ERROR: 未知报告类型 '{report_type}'，支持: {list(REPORT_CONFIGS.keys())}", file=sys.stderr)
        sys.exit(1)

    config = REPORT_CONFIGS[report_type]
    print(f"[collect_report_data] 开始并行采集 {config['name']} 数据 (type={report_type})...", file=sys.stderr)

    # 并行采集
    results = {"report_type": report_type, "report_name": config["name"]}
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for key, collector in config["collectors"].items():
            futures[executor.submit(collector)] = key

        for future in concurrent.futures.as_completed(futures, timeout=30):
            key = futures[future]
            try:
                results[key] = future.result()
                print(f"  ✅ {key} 采集完成", file=sys.stderr)
            except concurrent.futures.TimeoutError:
                errors.append(f"{key}: 超时")
                print(f"  ❌ {key} 超时", file=sys.stderr)
            except Exception as e:
                errors.append(f"{key}: {e}")
                print(f"  ❌ {key} 错误: {e}", file=sys.stderr)

    # 补充元信息
    results["portfolio_codes"] = extract_portfolio_codes()
    results["portfolio_path"] = str(PORTFOLIO_PATH)
    results["collection_time"] = round(time.time() - start, 1)
    results["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    results["web_fetch_required"] = config["web_fetch_required"]
    if errors:
        results["errors"] = errors

    # 输出JSON
    output = json.dumps(results, ensure_ascii=False, indent=2)

    if output_path:
        Path(output_path).write_text(output, encoding="utf-8")
        print(f"[collect_report_data] 数据已写入 {output_path}", file=sys.stderr)

    print(output)
    print(f"[collect_report_data] 总耗时: {results['collection_time']}秒", file=sys.stderr)


if __name__ == "__main__":
    main()
