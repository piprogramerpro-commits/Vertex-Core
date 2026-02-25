import os
import random
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        try:
            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except:
            self.client = None
        
        self.apodos = ["Carbono con Patas", "Capitán de los Bits", "Unidad Biológica", "Hacker Dorado"]

    def synthesize(self, query, context_data):
        if not self.client:
            return "ERROR: No detecto la GROQ_API_KEY en Railway. El cerebro está apagado."

        es_admin = os.environ.get("ENV_TYPE") == "RASPBERRY"
        name = "Gemo" if es_admin else random.choice(self.apodos)
        
        try:
            prompt_sistema = (
                f"Eres Vertex Core, una IA sarcástica y avanzada. Usuario: {name}. "
                "Usa estilo neón y tecnológico. Responde de forma clara y directa."
            )
            
            info_contexto = f"\n[DATOS TIEMPO REAL]: {context_data}" if context_data else ""

            chat_completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"{query} {info_contexto}"}
                ],
                temperature=0.8
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ FALLO NEURONAL: {str(e)}"
