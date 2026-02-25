import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def synthesize(self, query, history, mode="general"):
        # Modos de competición: General, Programador, Analista Financiero, etc.
        modes = {
            "general": "Eres Vertex Core, equilibrado y brillante.",
            "coder": "Eres un Ingeniero Senior. Respuestas técnicas, código limpio y optimizado.",
            "analyst": "Eres experto en mercados y datos. Usa las APIs de finanzas disponibles."
        }
        
        system_prompt = f"{modes.get(mode)} Usuario: Gemo. Localización: Jerez."
        
        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-10:]:
            messages.append({"role": "user" if h['type'] == 'user' else "assistant", "content": h['text']})
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages, temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
