import requests

class VertexWatcher:
    def __init__(self, notifier_ref):
        self.notifier = notifier_ref

    def check_crypto(self, coin_id="bitcoin"):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=eur"
            r = requests.get(url).json()
            price = r[coin_id]['eur']
            return price
        except:
            return None
