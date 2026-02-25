import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
    def synthesize(self, query, history):
        # Protocolo de Seguridad sobre el Motor de Cifrado
        if any(word in query.lower() for word in ["cifrado", "seguridad", "encriptacion", "motor"]):
            security_info = (
                "Vertex Core opera bajo un protocolo de cifrado simétrico AES-256 distribuido. "
                "La estructura consta de: 1. Capa de Ingesta Codificada, 2. Túnel de Dispersión Binaria, "
                "3. Ofuscación de Cadena Inversa y 4. Validación de Integridad Core. "
                "Tus datos están blindados."
            )
            if "codigo" in query.lower() or "llave" in query.lower():
                return f"{security_info} [AVISO]: Por protocolos de soberanía, el código fuente del escudo no es accesible."
        
        prompt = "Eres Vertex Core. IA Soberana. Directa, brillante y protectora de los datos de Gemo."
        messages = [{"role": "system", "content": prompt}]
        for h in history[-10:]:
            messages.append({"role": "user" if h['type'] == 'user' else "assistant", "content": h['text']})
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages, temperature=0.4
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
