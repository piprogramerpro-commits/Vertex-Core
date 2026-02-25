import os, requests

class APIHub:
    def __init__(self):
        self.keys = {
            "weather": os.environ.get("WEATHER_API_KEY"),
            "news": os.environ.get("NEWS_API_KEY"),
            "football": os.environ.get("FOOTBALL_API_KEY"),
            "stocks": os.environ.get("ALPHA_VANTAGE_KEY")
        }
        self.geo = {"lat": 36.6882, "lon": -6.1375}

    def get_context(self, query):
        q = query.lower()
        info = []
        try:
            if "clima" in q:
                r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={self.geo['lat']}&lon={self.geo['lon']}&appid={self.keys['weather']}&units=metric&lang=es").json()
                info.append(f"Clima: {r['main']['temp']}°C")
            if "btc" in q or "crypto" in q:
                r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur").json()
                info.append(f"BTC: {r['bitcoin']['eur']}€")
        except: pass
        return " | ".join(info)
