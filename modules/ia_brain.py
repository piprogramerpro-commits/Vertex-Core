import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def synthesize(self, query, history):
        prompt = (
            "Eres Vertex Core. Tienes acceso a sensores en tiempo real. "
            "Si el mensaje contiene [CONTEXTO ACTUAL], usa esa información para responder directamente. "
            "No preguntes la ubicación, ya sabes que el usuario es Gemo y está en Jerez de la Frontera. "
            "Sé breve, brillante y no pidas confirmaciones innecesarias."
        )
        
        messages = [{"role": "system", "content": prompt}]
        for h in history[-8:]:
            messages.append({"role": "user" if h['type'] == 'user' else "assistant", "content": h['text']})
        
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages, 
                temperature=0.3 # Bajamos la temperatura para que sea más preciso con los datos
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Fallo de núcleo: {str(e)}"
