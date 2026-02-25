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
        # Aquí Vertex sabe que habla contigo, el tono es de "socio en el crimen"
        response = brain.synthesize(query, [])
        sparks = "INFINITOS"
    elif identity == "IMPOSTOR":
        return jsonify({
            "vertex_response": "Buen intento. Pero mi lealtad no se hackea con un email robado. Largo de aquí.",
            "sparks": 0
        })
    else:
        # Usuario normal: Útil pero con ese toque de "te estoy vigilando"
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Te has quedado sin Sparks. La soberanía no es gratis, vuelve cuando tengas energía.", "sparks": 0})
        response = brain.synthesize(query, [])
        sparks = vault.get_sparks(email)

    return jsonify({"vertex_response": response, "sparks": sparks})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
