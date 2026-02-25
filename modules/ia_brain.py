import random
import os

class VertexBrain:
    def __init__(self):
        self.apodos = ["Comandante", "Unidad Biológica", "Operador de Red", "Hacker de Élite"]

    def synthesize(self, query, context_data):
        query = query.lower()
        es_admin = os.environ.get("ENV_TYPE") == "RASPBERRY"
        name = "Gemo" if es_admin else random.choice(self.apodos)
        
        # Inicio de respuesta profesional
        response = f"◆ [NÚCLEO VERTEX] ◆\nSincronizando con {name}...\n\n"

        # Si el Hub encontró datos reales, los mostramos CLARAMENTE
        if context_data:
            if "weather" in context_data:
                response += f"🌤️ ESTADO CLIMÁTICO: Actualmente hay {context_data['weather']}.\n"
            if "crypto" in context_data:
                response += f"₿ MERCADO CRYPTO: {context_data['crypto']}.\n"
            if "news" in context_data:
                response += f"📰 ÚLTIMA HORA: {context_data['news']}.\n"
            
            response += "\n¿Deseas profundizar en algún dato adicional?"
        else:
            # Si no hay datos de API, pero la pregunta es general
            if "hola" in query:
                response += f"Sistema operativo. Todas las constantes vitales en orden. ¿Qué necesitas, {name}?"
            else:
                response += f"He analizado '{query}', pero necesito que configures las API Keys en el panel de Railway para darte datos en tiempo real de esta categoría."

        return response
