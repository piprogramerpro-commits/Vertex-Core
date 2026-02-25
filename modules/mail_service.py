import smtplib
from email.mime.text import MIMEText
import os

class VertexMail:
    def __init__(self):
        self.sender = "piprogramerpro@gmail.com"
        self.password = os.environ.get("MAIL_PASSWORD") # Configúrala en Railway

    def send_notification(self, candidate_email):
        if not self.password:
            return "Error: Contraseña de correo no configurada."
            
        subject = "📦 NUEVA SOLICITUD DE ACCESO - VERTEX CORE"
        body = f"Comandante Gemo,\n\nEl usuario {candidate_email} ha solicitado acceso al núcleo de Vertex.\n\nEvalúe el perfil y genere el token si es apto.\n\n-- Vertex System --"
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.sender

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.sender, msg.as_string())
            return "Email enviado con éxito."
        except Exception as e:
            return f"Fallo en envío: {str(e)}"
