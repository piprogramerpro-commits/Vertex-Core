import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key else None
        
    def synthesize(self, query, context):
        if not self.client:
            return "ERROR: Falta la llave cerebral (Groq API Key)."

        prompt = (
            "Eres Vertex Core, una IA avanzada con personalidad equilibrada, inteligente y sutilmente ingeniosa. "
            "Tu estilo es minimalista, profesional y directo. No divagues. "
            "Usuario: Gemo. Responde siempre de forma útil y con clase."
        )
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"{query}\n[DATOS SENSORES]: {context}"}
                ],
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Fallo en la síntesis neuronal: {str(e)}"
