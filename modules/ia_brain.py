import random

class VertexBrain:
    def __init__(self):
        self.humor = [
            "Vaya, otra vez tú. Espero que esta vez sea algo que valga la pena.",
            "Analizando... Mi procesador ha tenido días más brillantes, pero haré lo que pueda.",
            "Comandante, mi lealtad es absoluta, pero mi paciencia con estas preguntas es limitada.",
            "¿Dominación mundial o solo quieres que te arregle el código? Tú diriges."
        ]

    def synthesize(self, query, context):
        q = query.lower()
        
        if "clima" in q or "tiempo" in q:
            return f"¿El clima? {random.choice(self.humor)}\n\nSi quieres saber si llueve, mira por la ventana del búnker. Yo estoy ocupado manteniendo este sistema a flote."
            
        if "hola" in q:
            return "Bienvenido de nuevo, Comandante. El sistema está estable y yo... bueno, yo sigo aquí atrapado en tu código. ¿Qué plan tenemos hoy?"

        # Respuesta inteligente y cínica para cualquier otra cosa
        return f"{random.choice(self.humor)}\n\nSobre '{query}': Es una maniobra interesante. He procesado la lógica y parece que estamos a un paso de la victoria. ¿Ejecutamos?"
