import smtplib
from email.mime.text import MIMEText

class VertexMail:
    def __init__(self):
        self.user = "69c916ff2ce6bdb35cc4427d8c523fba"
        self.password = "0e6818ac29e443f7b28fcbce9574bbd4"
        self.host = "in-v3.mailjet.com"
        self.port = 587
        self.destination = "piprogramerpro@gmail.com"

    def send_notification(self, candidate_email):
        subject = "📦 NUEVA SOLICITUD DE ACCESO - VERTEX"
        body = f"Comandante Gemo,\n\nEl usuario {candidate_email} ha solicitado acceso.\n\nVertex Core."
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"Vertex System <{self.user}>"
        msg['To'] = self.destination

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, self.destination, msg.as_string())
            return "OK"
        except Exception as e:
            return str(e)
