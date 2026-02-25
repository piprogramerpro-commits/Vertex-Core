from modules.search_engine import VertexSearch
import datetime

class VertexNewsAgent:
    def __init__(self, brain_ref, notifier_ref):
        self.brain = brain_ref
        self.notifier = notifier_ref
        self.scanner = VertexSearch()

    def get_morning_briefing(self, topic="Inteligencia Artificial y Criptomonedas"):
        today = datetime.date.today().strftime("%d/%m/%Y")
        print(f"[NEWS_AGENT]: Escaneando noticias para {today}...")
        
        # 1. Buscamos en la red
        raw_news = self.scanner.search(f"noticias última hora {topic}")
        
        # 2. Vertex procesa y resume
        prompt = f"Resume de forma ejecutiva y audaz las siguientes noticias del día {today} sobre {topic}. Enfócate en lo que pueda ser una oportunidad de oro o un peligro: {raw_news}"
        summary = self.brain.synthesize(prompt, [])
        
        # 3. Envío proactivo
        self.notifier.send_alert(f"📊 INFORME ESTRATÉGICO {today}:\n\n{summary}")
        return "Informe enviado."
