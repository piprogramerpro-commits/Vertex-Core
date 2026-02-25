from flask import Flask, render_template, request, jsonify
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain

app = Flask(__name__)
vault = VertexVault()
brain = VertexBrain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    email = data.get("email", "").strip().lower()
    hwid = data.get("hwid", "")
    query = data.get("query", "")

    identity = vault.check_identity(email, hwid)

    if identity == "ADMIN_CONFIRMED":
        prefix = "[ESTADO: COMANDANTE DETECTADO]"
        sparks_display = "INFINITOS"
    elif identity == "IMPOSTOR":
        return jsonify({
            "vertex_response": "⚠️ **PROTOCOLO DE SEGURIDAD ACTIVADO.** Hardware no autorizado. Intento de suplantación registrado.",
            "sparks": 0,
            "role": "INTRUSO"
        })
    else:
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Energía agotada. Solicite acceso al Comandante.", "sparks": 0})
        prefix = "[ESTADO: USUARIO]"
        sparks_display = vault.get_sparks(email)

    response = brain.synthesize(f"{prefix} {query}", [])
    
    return jsonify({
        "vertex_response": response,
        "sparks": sparks_display,
        "role": identity
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
