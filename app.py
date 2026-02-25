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

@app.route('/check_auth', methods=['POST'])
def check_auth():
    data = request.json
    email = data.get("email", "").lower().strip()
    hwid = data.get("hwid", "")
    access = vault.check_access(email, hwid)
    sparks = vault.get_sparks(email)
    return jsonify({"access": access, "sparks": sparks})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    email = data.get("email", "").lower().strip()
    hwid = data.get("hwid", "")
    query = data.get("query", "")
    
    access = vault.check_access(email, hwid)
    if access in ["COMMANDER", "USER_APPROVED"]:
        response = brain.synthesize(query, [])
        return jsonify({"vertex_response": response, "sparks": vault.get_sparks(email)})
    return jsonify({"vertex_response": "Acceso denegado. Solicitud pendiente.", "sparks": 0})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
