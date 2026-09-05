import json
import ssl
import time
import urllib.request
from datetime import datetime

# 忽略 SSL 证书校验（防止部分网络环境报证书错误）
ssl_context = ssl._create_unverified_context()


def get_crypto_prices_binance():
    """从币安获取 BTC/USDT 和 ETH/USDT 实时价格"""
    symbols = ["BTCUSDT", "ETHUSDT"]
    prices = {}

    for symbol in symbols:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        try:
            with urllib.request.urlopen(
                req, timeout=5, context=ssl_context
            ) as response:
                data = json.loads(response.read().decode())
                prices[symbol] = float(data["price"])
        except Exception as e:
            # 如果币安在特定网络下不可用，自动切到 OKX 备用接口
            return get_crypto_prices_okx()

    return prices["BTCUSDT"], prices["ETHUSDT"]


def get_crypto_prices_okx():
    """备用数据源：从 OKX 获取实时价格"""
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
        data = json.loads(response.read().decode())
        prices = {}
        for item in data["data"]:
            if item["instId"] in ["BTC-USDT", "ETH-USDT"]:
                prices[item["instId"]] = float(item["last"])
        return prices.get("BTC-USDT", 0.0), prices.get("ETH-USDT", 0.0)


def run_live_tracker():
    try:
        btc_price, eth_price = get_crypto_prices_binance()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"=== 交易所实时价格 [{current_time}] ===")
        print(f"比特币 (BTC): ${btc_price:,.2f}")
        print(f"以太坊 (ETH): ${eth_price:,.2f}\n")
    except Exception as e:
        print(f"获取价格失败: {e}\n")


if __name__ == "__main__":
    # 连续快速运行测试
    run_live_tracker()
