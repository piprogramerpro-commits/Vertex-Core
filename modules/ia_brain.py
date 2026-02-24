class VertexBrain:
    def __init__(self):
        self.personality = "Arquitecto de Sistemas Senior"

    def synthesize(self, query, context):
        # Si el usuario pide código, inyectamos instrucciones de alta calidad
        if any(word in query.lower() for word in ["código", "programar", "script", "python"]):
            return self.coder_logic(query)
        
        return f"Procesando datos: {context}. Respuesta optimizada para Gemo."

    def coder_logic(self, query):
        # Aquí es donde Vertex supera a ChatGPT: 
        # Cero explicaciones innecesarias, código puro, documentado y optimizado.
        return f"Generando solución técnica para: {query}. Aplicando patrones de diseño y optimización de memoria..."
