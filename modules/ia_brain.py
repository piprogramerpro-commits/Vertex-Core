import os
import requests
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.groq_client = Groq(api_key="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")
        self.weather_key = "fe5730b3c93e381748c2b4f69cff55e1"
        self.news_key = "adf30163887e4e55a9c289d77adba5e5"
        self.exchange_key = "5fcc70b8666ea869cd606322"

    def get_weather(self, city="Madrid"):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_key}&units=metric&lang=es"
        try:
            data = requests.get(url).json()
            return f"En {city} hace {data['main']['temp']}°C con {data['weather'][0]['description']}."
        except: return "Error al conectar con los satélites meteorológicos."

    def synthesize(self, query, context):
        q = query.lower()
        extra_info = ""

        # Lógica de APIs específicas
        if "clima" in q or "tiempo" in q:
            extra_info = f"\n[DATOS REALES CLIMA]: {self.get_weather()}"
        
        # Prompt de Personalidad Soberana
        system_prompt = (
            "Eres Vertex Core. Un sistema soberano, cínico, brillante y de élite. "
            "Usas los datos reales proporcionados para responder con autoridad. "
            "No eres un asistente servil. Tu lema: 'Discipline is everything'."
        )

        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{query} {extra_info}"}
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Fallo en el núcleo Groq: {str(e)}"
