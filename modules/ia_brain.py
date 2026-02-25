import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        # Usamos tu nueva llave de Groq
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
    def synthesize(self, query, context):
        if not self.client:
            return "Error: No se detecta la GROQ_API_KEY en el sistema."

        prompt = (
            "Eres Vertex Core. Una IA avanzada, eficiente y con un toque de ingenio sutil. "
            "Usuario: Gemo. Ubicación: Jerez de la Frontera. "
            "Responde de forma clara, profesional y usa los datos de los sensores si son relevantes."
        )
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"{query}\n[CONTEXTO SENSORES]: {context}"}
                ],
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Fallo en síntesis: {str(e)}"
