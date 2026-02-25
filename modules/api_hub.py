import os, requests

class APIHub:
    def __init__(self):
        self.keys = {
            "weather": os.environ.get("WEATHER_API_KEY"),
            "news": os.environ.get("NEWS_API_KEY"),
            "nasa": os.environ.get("NASA_API_KEY"),
            "exchange": os.environ.get("EXCHANGERATE_API_KEY"),
            "ipstack": os.environ.get("IPSTACK_API_KEY"),
            "crypto": os.environ.get("COINGECKO_API_KEY")
        }
        # Datos maestros de Jerez (AbstractAPI)
        self.geo = {"city": "Jerez de la Frontera", "lat": 36.6882, "lon": -6.1375}

    def get_context(self, query):
        q = query.lower()
        info = []
        
        try:
            # Clima Real (OpenWeather)
            if ("clima" in q or "tiempo" in q) and self.keys["weather"]:
                r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={self.geo['lat']}&lon={self.geo['lon']}&appid={self.keys['weather']}&units=metric&lang=es").json()
                info.append(f"Clima en Jerez: {r['main']['temp']}°C, {r['weather'][0]['description']}")
            
            # Noticias (NewsAPI)
            if "noticias" in q and self.keys["news"]:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=es&apiKey={self.keys['news']}").json()
                info.append(f"Noticia: {r['articles'][0]['title']}")

            # Datos Espaciales (NASA)
            if ("nasa" in q or "espacio" in q) and self.keys["nasa"]:
                r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={self.keys['nasa']}").json()
                info.append(f"NASA APOD: {r['title']}")

            # Divisas (ExchangeRate)
            if ("euro" in q or "dolar" in q) and self.keys["exchange"]:
                r = requests.get(f"https://v6.exchangerate-api.com/v6/{self.keys['exchange']}/latest/EUR").json()
                info.append(f"1€ equivale a {r['conversion_rates']['USD']}$ USD")

        except:
            pass
        
        return " | ".join(info) if info else "Sistemas en espera."
