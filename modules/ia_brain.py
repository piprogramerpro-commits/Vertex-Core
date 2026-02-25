import os
import random
import requests
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.apodos = ["Carbono con Patas", "Líder de los Cables", "Unidad Biológica", "Hacker Dorado"]

    def get_location(self):
        try:
            # Geolocalización por IP rápida y gratuita
            res = requests.get('https://ipapi.co/json/').json()
            return f"{res.get('city')}, {res.get('country_name')}"
        except:
            return "Localización Desconocida"

    def synthesize(self, query, context_data):
        if not self.client:
            return "ERROR: Sistema sin GROQ_API_KEY. Estoy ciego."

        es_admin = os.environ.get("ENV_TYPE") == "RASPBERRY"
        name = "Gemo" if es_admin else random.choice(self.apodos)
        
        # Si pide el clima y no hay ciudad, auto-detectamos
        loc = ""
        if "clima" in query.lower():
            loc = f" (Detectado en: {self.get_location()})"

        try:
            prompt_sistema = (
                f"Eres Vertex Core, una IA avanzada, cínica y brillante. Usuario: {name}. "
                "No pidas datos al usuario como un formulario aburrido. Si falta info, invéntatela o búscala. "
                "Tu estilo es 'High Tech, Low Life'. Sé directo y sarcástico."
            )
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"{query} {loc} {context_data}"}
                ],
                temperature=0.8
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ FALLO NEURONAL: {str(e)}"
