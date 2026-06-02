#!/usr/bin/env python3
"""
尾盘报告数据采集脚本 - 并行采集所有数据，输出JSON
用法: python3 collect_tail_data.py [--portfolio /path/to/portfolio.md] [--output /path/to/output.json]
"""
import concurrent.futures
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
TIMEOUT = 15  # 单次请求超时(秒)
PORTFOLIO_PATH = Path("/home/obsidian_vault/2-Final-Memory/portfolio.md")

# ── 工具函数 ──────────────────────────────────────────
def web_fetch(url, max_chars=8000, encoding="utf-8"):
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


def web_fetch_curl(url, max_chars=8000):
    """用curl获取网页内容（用于东方财富push2等urllib被拦截的接口）"""
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", str(TIMEOUT),
             "-H", "User-Agent: Mozilla/5.0",
             "-H", "Referer: https://data.eastmoney.com/",
             url],
            capture_output=True, text=True, timeout=TIMEOUT + 5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
        return f"ERROR: curl failed (rc={result.returncode}): {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return "ERROR: curl timeout"
    except Exception as e:
        return f"ERROR: {e}"


def parse_tencent_index(text):
    """解析腾讯财经四大指数"""
    if text.startswith("ERROR"):
        return {"error": text}
    result = {}
    # 格式: v_sh000001="1~上证指数~000001~当前价~昨收~今开~成交量~...~涨跌额~涨跌幅~最高~最低~...~成交额~..."
    for item in text.strip().split(";"):
        if "~" not in item:
            continue
        # 提取代码
        code_match = re.search(r'v_(\w+)="', item)
        if not code_match:
            continue
        code = code_match.group(1)
        fields = item.split("~")
        if len(fields) < 40:
            continue
        try:
            result[code] = {
                "name": fields[1],
                "code": fields[2],
                "price": float(fields[3]),
                "last_close": float(fields[4]),
                "open": float(fields[5]),
                "vol": fields[6],  # 成交量(手)
                "change": float(fields[31]),
                "change_pct": float(fields[32]),
                "high": float(fields[33]),
                "low": float(fields[34]),
                "amount": float(fields[37]) if fields[37] else 0,  # 成交额(亿)
            }
        except (ValueError, IndexError):
            continue
    return result


def parse_eastmoney_fundflow(text):
    """解析东方财富push2资金流向"""
    if text.startswith("ERROR"):
        return {"error": text}
    try:
        data = json.loads(text)
        items = data.get("data", {}).get("diff", [])
        result = []
        for item in items[:15]:  # 取前15
            result.append({
                "name": item.get("f14", ""),
                "code": item.get("f12", ""),
                "change_pct": item.get("f3", 0),
                "net_inflow": item.get("f62", 0),  # 主力净流入(亿)
                "price": item.get("f2", 0),
            })
        return result
    except Exception as e:
        return {"error": str(e)}


def parse_tencent_funds(text):
    """解析腾讯财经基金净值（批量）"""
    if text.startswith("ERROR"):
        return {"error": text}
    result = {}
    for line in text.strip().split(";"):
        if "~" not in line or not line.strip():
            continue
        # 格式: v_sh021225="1~科创芯片ETF联接C~021225~净值~昨收~...~涨跌幅~..."
        code_match = re.search(r'v_(\w+)="', line)
        if not code_match:
            continue
        code = code_match.group(1)
        fields = line.split("~")
        if len(fields) < 35:
            continue
        try:
            result[code] = {
                "name": fields[1],
                "code": fields[2],
                "nav": float(fields[3]),  # 当前净值
                "last_nav": float(fields[4]),  # 昨收
                "change_pct": float(fields[32]) if len(fields) > 32 else 0,  # 涨跌幅
            }
        except (ValueError, IndexError):
            continue
    return result


def parse_peripheral(text):
    """解析外围市场（黄金/原油/港股等）"""
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
                "name": fields[1],
                "price": float(fields[3]),
                "change_pct": float(fields[32]) if len(fields) > 32 else 0,
            }
        except (ValueError, IndexError):
            continue
    return result


def extract_portfolio_codes(portfolio_path=PORTFOLIO_PATH):
    """从portfolio.md提取当前持仓区基金代码（不含长期关注区）"""
    try:
        content = portfolio_path.read_text(encoding="utf-8")
        # 只提取"🟢 持仓区"到"🏆 贵金属"之间的代码（不含长期关注区）
        in_holding = False
        codes = []
        for line in content.split("\n"):
            if "🟢 持仓区" in line or "🏆 贵金属" in line or "🛡️ 债券" in line:
                in_holding = True
            elif "长期关注区" in line or "已清仓" in line:
                in_holding = False
            elif in_holding and "|" in line:
                # 提取表格行中的6位数字代码
                matches = re.findall(r'\b(\d{6})\b', line)
                for m in matches:
                    if m not in codes:
                        codes.append(m)
        return codes
    except Exception as e:
        return []


# ── 采集函数（每个线程一个）────────────────────────────
def collect_index():
    """腾讯财经四大指数"""
    url = "https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688"
    text = web_fetch(url, encoding="gbk")
    return parse_tencent_index(text)


def collect_fund_flow():
    """东方财富push2资金流向（概念板块TOP15）
    
    ⚠️ 注意：东方财富push2接口在服务器端拦截了urllib/requests/curl，
    只有通过 OpenClaw 的 web_fetch 工具才能调用。
    此函数返回标记，提示需要通过 web_fetch 单独采集。
    """
    return {
        "_needs_web_fetch": True,
        "url": (
            "https://push2.eastmoney.com/api/qt/clist/get"
            "?pn=1&pz=15&po=1&np=1&fltt=2&invt=2&fid=f62"
            "&fs=m:90+t:3"
            "&fields=f2,f3,f4,f6,f12,f14,f62"
        ),
        "parser": "eastmoney_fundflow",
        "note": "东方财富push2需通过OpenClaw web_fetch调用，urllib/curl均被拦截"
    }


def collect_fund_flow_industry():
    """东方财富push2资金流向（行业板块外资流向）
    
    ⚠️ 同上，需通过 web_fetch 调用
    """
    return {
        "_needs_web_fetch": True,
        "url": (
            "https://push2.eastmoney.com/api/qt/clist/get"
            "?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f62"
            "&fs=m:90+t:2"
            "&fields=f2,f3,f4,f6,f12,f14,f62"
        ),
        "parser": "eastmoney_fundflow",
        "note": "东方财富push2需通过OpenClaw web_fetch调用，urllib/curl均被拦截"
    }


def collect_valuation():
    """天天基金批量获取基金净值（腾讯财经返回的是股票行情，不适用于基金）"""
    codes = extract_portfolio_codes()
    if not codes:
        return {"error": "无法提取基金代码"}
    result = {}
    for code in codes:
        url = f"https://fundgz.1234567.com.cn/js/{code}.js"
        text = web_fetch(url)
        if text.startswith("ERROR"):
            result[code] = {"error": text}
            continue
        # 解析: jsonpgz({"fundcode":"021225","name":"科创芯片ETF联接C","jzrq":"2026-05-27","dwjz":"3.9736","gsz":"3.9736","gszzl":"-1.98",...})
        try:
            json_str = text[text.index("(")+1:text.rindex(")")]
            data = json.loads(json_str)
            result[code] = {
                "name": data.get("name", ""),
                "code": data.get("fundcode", code),
                "nav": float(data.get("dwjz", 0)),  # 单位净值
                "estimated_nav": float(data.get("gsz", 0)),  # 估算净值
                "estimated_change_pct": float(data.get("gszzl", 0)),  # 估算涨跌幅
                "nav_date": data.get("jzrq", ""),  # 净值日期
            }
        except Exception as e:
            result[code] = {"error": str(e), "raw": text[:200]}
    return result


def collect_peripheral():
    """外围市场：黄金/原油/港股/A50"""
    # 恒生指数/纳斯达克/道琼斯/标普500
    url = "https://qt.gtimg.cn/q=hk00HSI,usr_ixic,usr_dji,usr_spx,hk00HSCEI"
    text = web_fetch(url, encoding="gbk")
    result = parse_peripheral(text)
    # 补充黄金和原油（用商品代码）
    url2 = "https://qt.gtimg.cn/q=hf_GC,hf_CL"
    text2 = web_fetch(url2, encoding="gbk")
    result2 = parse_peripheral(text2)
    result.update(result2)
    return result


# ── 主流程 ────────────────────────────────────────────
def main():
    start = time.time()
    print(f"[collect_tail_data] 开始并行采集数据...", file=sys.stderr)

    # 从命令行参数获取portfolio路径
    portfolio_path = PORTFOLIO_PATH
    for i, arg in enumerate(sys.argv):
        if arg == "--portfolio" and i + 1 < len(sys.argv):
            portfolio_path = Path(sys.argv[i + 1])
            break

    # 并行采集
    results = {}
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        tasks = {
            executor.submit(collect_index): "index",
            executor.submit(collect_fund_flow): "fund_flow_concept",
            executor.submit(collect_fund_flow_industry): "fund_flow_industry",
            executor.submit(collect_valuation): "valuation",
            executor.submit(collect_peripheral): "peripheral",
        }

        for future in concurrent.futures.as_completed(tasks, timeout=30):
            key = tasks[future]
            try:
                results[key] = future.result()
                print(f"  ✅ {key} 采集完成", file=sys.stderr)
            except concurrent.futures.TimeoutError:
                errors.append(f"{key}: 超时")
                print(f"  ❌ {key} 超时", file=sys.stderr)
            except Exception as e:
                errors.append(f"{key}: {e}")
                print(f"  ❌ {key} 错误: {e}", file=sys.stderr)

    # 提取基金代码列表
    results["portfolio_codes"] = extract_portfolio_codes(portfolio_path)
    results["portfolio_path"] = str(portfolio_path)
    results["collection_time"] = round(time.time() - start, 1)
    results["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if errors:
        results["errors"] = errors

    # 输出JSON到stdout
    output = json.dumps(results, ensure_ascii=False, indent=2)

    # 如果指定了--output，写入文件
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            out_path = sys.argv[i + 1]
            Path(out_path).write_text(output, encoding="utf-8")
            print(f"[collect_tail_data] 数据已写入 {out_path}", file=sys.stderr)
            break

    print(output)  # stdout输出JSON
    print(f"[collect_tail_data] 总耗时: {results['collection_time']}秒", file=sys.stderr)


if __name__ == "__main__":
    main()
