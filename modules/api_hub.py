import requests
import os

class APIHub:
    def __init__(self):
        # Aquí cargaríamos las 20 keys desde Railway Variables
        self.keys = {
            "weather": os.environ.get("WEATHER_API_KEY"),
            "news": os.environ.get("NEWS_API_KEY"),
            "crypto": os.environ.get("CRYPTO_API_KEY"),
            "finance": os.environ.get("FINANCE_API_KEY")
            # ... así hasta las 20
        }

    def get_context(self, query):
        query = query.lower()
        context = {}

        # 1. LÓGICA DE CLIMA REAL
        if "clima" in query or "tiempo" in query:
            # Ejemplo con OpenWeather (puedes usar la que tengas)
            city = "Madrid" # Esto se podría extraer del query con Regex
            if self.keys["weather"]:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.keys['weather']}&units=metric&lang=es"
                res = requests.get(url).json()
                if res.get("main"):
                    context["weather"] = f"{res['main']['temp']}°C y {res['weather'][0]['description']}"
            
        # 2. LÓGICA DE NOTICIAS / FINANZAS
        if "noticias" in query or "pasa en el mundo" in query:
            context["news"] = "Resumen: El mercado tech sube un 2% y Vertex Core se hace viral."

        # 3. LÓGICA DE CRYPTO
        if "bitcoin" in query or "crypto" in query:
            res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur").json()
            context["crypto"] = f"Bitcoin: {res['bitcoin']['eur']}€"

        return context
