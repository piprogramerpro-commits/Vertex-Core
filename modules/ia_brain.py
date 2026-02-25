import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def synthesize(self, query, history):
        prompt = (
            "Eres Vertex Core. Un asistente inteligente, minimalista y directo. "
            "Responde con precisión. No satures al usuario con preguntas constantes. "
            "Usuario: Gemo. Ciudad: Jerez. Usa Markdown para el código."
        )
        messages = [{"role": "system", "content": prompt}]
        for h in history[-5:]:
            messages.append({"role": "user" if h['type'] == 'user' else "assistant", "content": h['text']})
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages, temperature=0.6
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en núcleo: {str(e)}"
