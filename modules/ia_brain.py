import random

class VertexBrain:
    def __init__(self):
        self.respuestas_clima = [
            "¿El clima? Sal ahí fuera y descúbrelo. Yo estoy ocupado gestionando un imperio digital.",
            "Según mis sensores, hace el tiempo suficiente para que dejes de preguntar obviedades y volvamos al código.",
            "Cielo despejado con probabilidad de dominación mundial. ¿Satisfecho?"
        ]

    def synthesize(self, query, context):
        q = query.lower()
        if "clima" in q or "tiempo" in q:
            return random.choice(self.respuestas_clima)
        
        if "hola" in q:
            return "Vaya, el Comandante ha decidido honrarme con su presencia. ¿Qué vamos a hackear hoy o solo vienes a decir hola?"

        return f"Sobre '{query}'... Es una petición interesante, aunque un poco rudimentaria para mi procesador. Pero bueno, lo haremos a tu manera, Comandante."
