import os, requests

class APIHub:
    def __init__(self):
        # Mapeo de llaves desde Railway
        self.keys = {
            "weather": os.environ.get("WEATHER_API_KEY"),
            "news": os.environ.get("NEWS_API_KEY"),
            "nasa": os.environ.get("NASA_API_KEY"),
            "crypto": os.environ.get("COINGECKO_API_KEY"),
            "exchange": os.environ.get("EXCHANGERATE_API_KEY"),
            "movies": os.environ.get("OMDB_API_KEY")
        }

    def get_context(self, query):
        q = query.lower()
        info = []
        
        try:
            # Lógica de Clima (solo si hay Key)
            if ("clima" in q or "tiempo" in q) and self.keys["weather"]:
                r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Jerez&appid={self.keys['weather']}&units=metric&lang=es").json()
                info.append(f"Clima en Jerez: {r['main']['temp']}°C, {r['weather'][0]['description']}")
            
            # Lógica de Noticias
            if ("noticias" in q) and self.keys["news"]:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=es&apiKey={self.keys['news']}").json()
                info.append(f"Noticia destacada: {r['articles'][0]['title']}")

            # Lógica de Crypto (Pública)
            if ("bitcoin" in q or "crypto" in q):
                r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur").json()
                info.append(f"Precio BTC: {r['bitcoin']['eur']}€")
                
            # Lógica NASA
            if ("nasa" in q or "espacio" in q) and self.keys["nasa"]:
                r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={self.keys['nasa']}").json()
                info.append(f"NASA Hoy: {r['title']}")
        except: 
            pass
        
        return " | ".join(info) if info else ""
