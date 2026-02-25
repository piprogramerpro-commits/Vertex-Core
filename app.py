from flask import Flask, render_template, request, jsonify
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain
from modules.mail_service import VertexMail
from modules.invites import VertexInvites

app = Flask(__name__)
vault = VertexVault()
brain = VertexBrain()
mail_bot = VertexMail()
inviter = VertexInvites()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    email = data.get("email", "").lower()
    hwid = data.get("hwid", "")
    query = data.get("query", "")
    identity = vault.check_identity(email, hwid)

    if identity == "COMMANDER":
        response = brain.synthesize(f"[ORDEN_ALTA] {query}", [])
        sparks = "INFINITOS"
    elif identity == "IMPOSTOR":
        return jsonify({"vertex_response": "⚠️ ALERTA: Hardware no autorizado.", "sparks": 0})
    else:
        vault.add_user(email) # Aseguramos que el usuario exista
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Energía agotada.", "sparks": 0})
        response = brain.synthesize(query, [])
        sparks = vault.get_sparks(email)

    return jsonify({"vertex_response": response, "sparks": sparks})

@app.route('/request_access', methods=['POST'])
def request_access():
    email = request.json.get("email", "").lower()
    if inviter.request_access(email):
        mail_bot.send_notification(email) # Te avisa a ti
        mail_bot.send_referral(email)     # Lo seduce a él
        return jsonify({"status": "Solicitud procesada. Revisa tu correo."})
    return jsonify({"status": "Ya estás registrado en el sistema."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
