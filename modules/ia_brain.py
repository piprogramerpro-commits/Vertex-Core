import os
import random
from groq import Groq

class VertexBrain:
    def __init__(self):
        # El código busca la llave que acabas de poner en Railway
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        self.apodos = [
            "Carbono con Patas", "Líder de los Cables", "Humano de Pruebas", 
            "Capitán de los Bits", "Procesador de Carne", "Aprendiz de Hacker"
        ]

    def synthesize(self, query, context_data):
        # Si no hay llave, Vertex avisa
        if not self.client:
            return "ERROR: No detecto mi GROQ_API_KEY. El sistema está en coma inducido."

        # Detectar si es Gemo o hay que usar apodo gracioso
        es_admin = os.environ.get("ENV_TYPE") == "RASPBERRY"
        name = "Gemo" if es_admin else random.choice(self.apodos)
        
        try:
            # Preparamos la personalidad y le pasamos los datos de las otras 19 APIs
            prompt_sistema = (
                f"Eres Vertex Core, una inteligencia artificial avanzada, sarcástica y algo cínica. "
                f"Tu usuario actual es {name}. "
                f"Si hay datos de contexto (clima, crypto, etc.), úsalos para dar respuestas reales. "
                "No seas aburrido, responde con estilo neón y tecnológico."
            )
            
            contexto_str = f"\n[DATOS DE APIS EXTERNAS]: {context_data}" if context_data else ""

            # Llamada real a Groq (Llama 3 de 70 billones de parámetros)
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"{query} {contexto_str}"}
                ],
                temperature=0.8
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ FALLO EN EL NÚCLEO: {str(e)}"
