import requests

class APIHub:
    def __init__(self):
        self.headers = {'User-Agent': 'VertexCoreAI/1.0'}

    def safe_get(self, url1, url2):
        try:
            r = requests.get(url1, timeout=2)
            return r.json(), "Primary"
        except:
            try:
                r = requests.get(url2, timeout=2)
                return r.json(), "Backup"
            except:
                return None, "Offline"

    def get_context(self, query):
        query = query.lower()
        ctx = {}

        # Nivel 1-2: Finanzas & Clima (Ya configurados)
        if "precio" in query or "crypto" in query:
            ctx["fin"], _ = self.safe_get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        
        if "clima" in query or "tiempo" in query:
            ctx["cli"], _ = self.safe_get("https://wttr.in/?format=j1", "https://api.open-meteo.com/v1/forecast?latitude=40.41&longitude=-3.70&current_weather=true")

        # Nivel 3-4: Wiki & Noticias
        if "que es" in query or "quien" in query:
            ctx["knw"], _ = self.safe_get(f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}", f"https://api.duckduckgo.com/?q={query}&format=json")

        # Nivel 5-6: Espacio & Geolocalización
        if "espacio" in query or "nasa" in query:
            ctx["spa"], _ = self.safe_get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", "http://api.open-notify.org/iss-now.json")

        if "donde estoy" in query or "ip" in query:
            ctx["geo"], _ = self.safe_get("https://ipapi.co/json/", "http://ip-api.com/json/")

        # Nivel 7-10: Utilidades rápidas (Traducción, Hora, Curiosidades, Divisas)
        if "curiosidad" in query or "dato" in query:
            ctx["fun"], _ = self.safe_get("http://numbersapi.com/random/trivia?json", "https://uselessfacts.jsph.pl/random.json?language=en")

        return ctx
