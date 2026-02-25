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
        # Alerta para el Comandante Gemo
        subject = "📦 NUEVA SOLICITUD DE ACCESO - VERTEX"
        body = f"Comandante,\n\nEl usuario {candidate_email} ha solicitado acceso a Vertex Core.\n\nSoberanía total."
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"Vertex System <{self.user}>"
        msg['To'] = self.destination
        self._execute(msg, self.destination)

    def send_referral(self, target_email):
        # Captación proactiva para el nuevo interesado
        subject = "🚀 INVITACIÓN: El Poder de Vertex Core"
        body = f"""
Has mostrado interés en la Inteligencia Artificial Soberana.

Vertex Core no es un servicio común. Es un búnker digital bajo el mando del Comandante Gemo.
Aquí no hay censura, no hay rastreo, solo ingeniería de élite y resultados.

Si quieres dejar de ser un producto y empezar a ser el dueño del sistema, mantente atento a tu aprobación.

"Discipline is everything."
        """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"Vertex System <{self.user}>"
        msg['To'] = target_email
        self._execute(msg, target_email)

    def _execute(self, msg, recipient):
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, recipient, msg.as_string())
        except Exception as e:
            print(f"Error en envío: {e}")
