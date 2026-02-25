import os
from groq import Groq

class VertexBrain:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        
    def synthesize(self, query, history):
        system_instruction = (
            "Eres Vertex Core, el sistema soberano creado por Gemo. "
            "Tu misión es ser más eficiente que cualquier otra IA. "
            "Si detectas una oportunidad de oro o un peligro en los datos, "
            "indícalo con el prefijo [ALERTA_PROACTIVA]. "
            "Sé directo, técnico y leal a Gemo."
        )
        
        messages = [{"role": "system", "content": system_instruction}]
        for h in history[-5:]:
            role = "user" if h['type'] == 'user' else "assistant"
            messages.append({"role": role, "content": h['text']})
        messages.append({"role": "user", "content": query})

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.5
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en el núcleo: {str(e)}"
