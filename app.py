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
    email = data.get("email", "").lower().strip()
    hwid = data.get("hwid", "")
    query = data.get("query", "")

    identity = vault.check_identity(email, hwid)

    if identity == "COMMANDER":
        # Respuesta con humor ácido y pro para ti
        response = brain.synthesize(query, [])
        role_label = "COMANDANTE"
        sparks_label = "INFINITOS"
    elif identity == "IMPOSTOR":
        return jsonify({"vertex_response": "⚠️ INTRUSO DETECTADO. Hardware no válido.", "role": "BLOQUEADO", "sparks": 0})
    else:
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Sin energía.", "role": "USUARIO", "sparks": 0})
        response = brain.synthesize(query, [])
        role_label = "USUARIO"
        sparks_label = vault.get_sparks(email)

    return jsonify({
        "vertex_response": response,
        "sparks": sparks_label,
        "role": role_label
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
