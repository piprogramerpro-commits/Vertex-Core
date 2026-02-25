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
    email = data.get("email", "").lower()
    hwid = data.get("hwid", "")
    query = data.get("query", "")

    identity = vault.check_identity(email, hwid)

    if identity == "COMMANDER":
        response = brain.synthesize(f"[ORDEN PRIORITARIA] {query}", [])
        sparks = "INFINITOS"
    elif identity == "IMPOSTOR":
        return jsonify({"vertex_response": "⚠️ **ACCESO DENEGADO.** Hardware no reconocido para el rango de Comandante.", "sparks": "BLOQUEADO"})
    else:
        # Aquí el sistema para usuarios normales
        sparks = vault.get_sparks(email)
        response = brain.synthesize(query, [])

    return jsonify({"vertex_response": response, "sparks": sparks})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
