import os, requests

class APIHub:
    def __init__(self):
        # 🔑 TODAS LAS LLAVES DE GEMO REUNIDAS
        self.keys = {
            "groq": os.environ.get("GROQ_API_KEY", "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"),
            "weather": os.environ.get("WEATHER_API_KEY", "870d014902123f17387d812328249871"),
            "news": os.environ.get("NEWS_API_KEY", "b404746654f1412fb1014e3650230232"),
            "nasa": os.environ.get("NASA_API_KEY", "DEMO_KEY"),
            "stocks": os.environ.get("ALPHA_VANTAGE_KEY", "D98BHO3NATR7YT7J"),
            "football": os.environ.get("FOOTBALL_API_KEY", "ed06ef7ca94a86888d55c46603cc942a"),
            "traffic": os.environ.get("TOMTOM_KEY", "QlCNu7MHxFvWthdx53SLbrDymIdKlWFo")
        }
        self.geo = {"city": "Jerez", "lat": 36.6882, "lon": -6.1375}

    def get_context(self, query):
        q = query.lower()
        info = [f"Ubicación: {self.geo['city']}", f"Motor Principal: Groq Llama 3.3"]
        
        try:
            # 📚 CONOCIMIENTO GENERAL (Wikipedia - El saber del mundo)
            if any(x in q for x in ["quién es", "qué es", "historia", "define", "significado"]):
                # Limpiamos la búsqueda para Wikipedia
                search = q.replace("quién es", "").replace("qué es", "").replace("define", "").strip()
                r_wiki = requests.get(f"https://es.wikipedia.org/api/rest_v1/page/summary/{search.replace(' ', '_')}").json()
                if "extract" in r_wiki:
                    info.append(f"Wikipedia: {r_wiki['extract'][:250]}...")

            # 🌦️ CLIMA (OpenWeather)
            if any(x in q for x in ["clima", "tiempo", "temperatura"]):
                r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={self.geo['lat']}&lon={self.geo['lon']}&appid={self.keys['weather']}&units=metric&lang=es").json()
                if "main" in r:
                    info.append(f"Clima: {r['main']['temp']}°C, {r['weather'][0]['description']}")

            # 💰 CRIPTO (CoinGecko)
            if any(x in q for x in ["btc", "bitcoin", "eth", "crypto"]):
                r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur").json()
                info.append(f"Cripto: BTC {r['bitcoin']['eur']}€, ETH {r['ethereum']['eur']}€")

            # ⚽ FÚTBOL (Resultados en vivo)
            if any(x in q for x in ["fútbol", "liga", "partido", "marcador"]):
                h = {"x-apisports-key": self.keys["football"]}
                r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=h).json()
                if r.get("response"):
                    f = r["response"][0]
                    info.append(f"Fútbol: {f['teams']['home']['name']} {f['goals']['home']}-{f['goals']['away']} {f['teams']['away']['name']}")

            # 📈 BOLSA (Acciones)
            if any(x in q for x in ["bolsa", "acciones", "stock"]):
                r = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={self.keys['stocks']}").json()
                if "Global Quote" in r:
                    info.append(f"Acciones IBM: {r['Global Quote']['05. price']}$")

            # 🚦 TRÁFICO (TomTom)
            if any(x in q for x in ["tráfico", "atasco", "carretera"]):
                r = requests.get(f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={self.keys['traffic']}&point={self.geo['lat']},{self.geo['lon']}").json()
                if "flowSegmentData" in r:
                    info.append(f"Tráfico Jerez: {r['flowSegmentData']['currentSpeed']} km/h de media")

            # 📰 NOTICIAS
            if "noticias" in q:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=es&apiKey={self.keys['news']}").json()
                if r.get("articles"):
                    info.append(f"Noticia: {r['articles'][0]['title']}")

            # 🚀 NASA
            if "nasa" in q or "espacio" in q:
                r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={self.keys['nasa']}").json()
                info.append(f"NASA APOD: {r.get('title')}")

        except:
            info.append("Estado: Algunos módulos están en modo ahorro de energía.")
            
        return " | ".join(info)
