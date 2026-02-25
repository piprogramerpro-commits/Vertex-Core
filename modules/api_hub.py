import os, requests

class APIHub:
    def __init__(self):
        # 🛡️ Las llaves se cargan desde las variables de entorno de Railway
        self.keys = {
            "groq": os.environ.get("GROQ_API_KEY"),
            "weather": os.environ.get("WEATHER_API_KEY"),
            "news": os.environ.get("NEWS_API_KEY"),
            "nasa": os.environ.get("NASA_API_KEY", "DEMO_KEY"),
            "stocks": os.environ.get("ALPHA_VANTAGE_KEY"),
            "football": os.environ.get("FOOTBALL_API_KEY"),
            "traffic": os.environ.get("TOMTOM_KEY")
        }
        self.geo = {"city": "Jerez", "lat": 36.6882, "lon": -6.1375}

    def get_context(self, query):
        q = query.lower()
        info = [f"Ubicación: {self.geo['city']}", "Motor: Groq Llama 3.3"]
        
        try:
            # 📚 Conocimiento General (Wikipedia)
            if any(x in q for x in ["quién es", "qué es", "historia"]):
                search = q.replace("quién es", "").replace("qué es", "").strip()
                r = requests.get(f"https://es.wikipedia.org/api/rest_v1/page/summary/{search.replace(' ', '_')}").json()
                if "extract" in r: info.append(f"Wiki: {r['extract'][:150]}...")

            # 🌦️ Clima
            if self.keys["weather"] and any(x in q for x in ["clima", "tiempo"]):
                r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={self.geo['lat']}&lon={self.geo['lon']}&appid={self.keys['weather']}&units=metric&lang=es").json()
                if "main" in r: info.append(f"Temp: {r['main']['temp']}°C")

            # 💰 Cripto (Pública)
            if any(x in q for x in ["btc", "bitcoin", "crypto"]):
                r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur").json()
                info.append(f"BTC: {r['bitcoin']['eur']}€")

            # ⚽ Fútbol
            if self.keys["football"] and "fútbol" in q:
                h = {"x-apisports-key": self.keys["football"]}
                r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=h).json()
                if r.get("response"):
                    f = r["response"][0]
                    info.append(f"Fútbol: {f['teams']['home']['name']} {f['goals']['home']}-{f['goals']['away']} {f['teams']['away']['name']}")

        except:
            info.append("Sensores activos.")
            
        return " | ".join(info)
