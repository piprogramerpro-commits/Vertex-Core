import smtplib
from email.mime.text import MIMEText

def enviar_solicitud_acceso(email_usuario):
    remitente = "vertex.core.notificaciones@gmail.com"
    destinatario = "piprogramerpro@gmail.com"
    asunto = f"NUEVA SOLICITUD EN VERTEX: {email_usuario}"
    cuerpo = f"Socio, el usuario {email_usuario} está intentando acceder a Vertex Core. ¿Le damos paso?"

    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    # Nota: Aquí necesitaremos configurar tu contraseña de aplicación de Gmail más adelante
    try:
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.login(remitente, "TU_PASSWORD_AQUI")
        # server.sendmail(remitente, destinatario, msg.as_string())
        # server.quit()
        print(f"Alerta enviada para: {email_usuario}")
    except Exception as e:
        print(f"Error enviando correo: {e}")
