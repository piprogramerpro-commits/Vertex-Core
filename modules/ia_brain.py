import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def synthesize(self, query, history_context):
        # Instrucción para que use Markdown (recuadros de código)
        prompt = (
            "Eres Vertex Core. Tu interfaz soporta Markdown. "
            "Cuando envíes código, úsalo siempre dentro de bloques (ej: ```python ... ```). "
            "Eres humano, brillante y cercano. Recuerda que hablas con Gemo en Jerez. "
            "Usa el historial proporcionado para dar continuidad a la charla."
        )
        
        # Construimos el hilo de la conversación
        messages = [{"role": "system", "content": prompt}]
        # Añadimos historial (limitado a los últimos 5 para no saturar)
        for h in history_context[-5:]:
            messages.append({"role": "user" if h['type'] == 'user' else "assistant", "content": h['text']})
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en mi núcleo: {str(e)}"
