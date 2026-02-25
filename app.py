from flask import Flask, render_template, request, jsonify, redirect
from modules.invites import VertexInvites
# ... (todas las importaciones previas)

app = Flask(__name__)
inviter = VertexInvites()

@app.route('/register/<token>')
def register_with_token(token):
    if inviter.validate_token(token):
        # Aquí podrías redirigir a una página de bienvenida especial
        return render_template('index.html', msg="ACCESO CONCEDIDO")
    return "TOKEN INVÁLIDO O YA USADO", 403

@app.route('/generate_invite', methods=['POST'])
def get_new_invite():
    # Solo Gemo puede generar invitaciones (protección por email)
    data = request.json
    if data.get("email") == "gemo@vertex.com":
        token = inviter.generate_token()
        return jsonify({"invite_link": f"/register/{token}"})
    return jsonify({"error": "No autorizado"}), 401

# (Mantenemos la ruta /ask con el cifrado y la lógica anterior)

@app.route('/request_access', methods=['POST'])
def request_access():
    email = request.json.get("email")
    if inviter.request_access(email):
        # Vertex te avisa por Telegram que alguien quiere entrar
        notifier.send_alert(f"NUEVA SOLICITUD: El usuario {email} quiere unirse a la red.")
        return jsonify({"status": "Solicitud enviada. Vertex evaluará tu perfil."})
    return jsonify({"status": "Ya tienes una solicitud pendiente."})
from modules.mail_service import VertexMail

mail_bot = VertexMail()

@app.route('/request_access', methods=['POST'])
def request_access():
    email = request.json.get("email")
    if inviter.request_access(email):
        # 1. Alerta por Telegram (Inmediata)
        notifier.send_alert(f"NUEVA SOLICITUD: {email}")
        # 2. Notificación por Email (Formal)
        mail_bot.send_notification(email)
        
        return jsonify({"status": "Solicitud enviada a la central. Espere confirmación."})
    return jsonify({"status": "Solicitud ya existente."})
