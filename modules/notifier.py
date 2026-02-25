import requests
import os

class VertexNotifier:
    def __init__(self):
        self.token = os.environ.get("TELEGRAM_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    def send_alert(self, message):
        if not self.token or not self.chat_id:
            return "Telegram no configurado en variables de entorno."
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": f"⚠️ VERTEX:\n{message}"}
        try:
            requests.post(url, json=payload)
            return "OK"
        except:
            return "Error"
