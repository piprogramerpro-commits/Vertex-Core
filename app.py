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
