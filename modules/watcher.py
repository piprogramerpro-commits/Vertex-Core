import requests

class VertexWatcher:
    def __init__(self, notifier_ref):
        self.notifier = notifier_ref

    def check_crypto(self, coin_id="bitcoin", target_price=50000):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=eur"
            r = requests.get(url).json()
            current_price = r[coin_id]['eur']
            
            if current_price >= target_price:
                self.notifier.send_alert(f"🚀 ¡OPORTUNIDAD DE ORO! {coin_id.upper()} ha alcanzado los {current_price}€")
            return current_price
        except Exception as e:
            return f"Error en vigilancia: {str(e)}"
