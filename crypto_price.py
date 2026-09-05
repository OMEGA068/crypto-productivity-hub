import json
import urllib.request
from datetime import datetime


def get_crypto_prices():
    # 使用 CoinGecko 公开 API 获取 BTC 和 ETH 的美元价格
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    # 设置请求头，防止被 API 拒绝
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

            btc_price = data["bitcoin"]["usd"]
            eth_price = data["ethereum"]["usd"]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"=== 加密货币实时价格 [{current_time}] ===")
            print(f"比特币 (BTC): ${btc_price:,}")
            print(f"以太坊 (ETH): ${eth_price:,}")

    except Exception as e:
        print(f"获取价格失败: {e}")


if __name__ == "__main__":
    get_crypto_prices()
