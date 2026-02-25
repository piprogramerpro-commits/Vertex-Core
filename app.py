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
    try:
        data = request.json
        email = data.get("email", "").lower().strip()
        hwid = data.get("hwid", "")
        query = data.get("query", "")
        
        access = vault.check_access(email, hwid)
        
        # Solo el Comandante o Usuarios Aprobados reciben respuesta
        if access in ["COMMANDER", "USER_APPROVED"]:
            # Llamamos al cerebro para que responda
            response_text = brain.synthesize(query, [])
            return jsonify({
                "vertex_response": response_text, 
                "sparks": vault.get_sparks(email),
                "status": "success"
            })
        
        return jsonify({"vertex_response": "Acceso denegado. Su terminal no tiene los permisos necesarios.", "sparks": 0})
    except Exception as e:
        return jsonify({"vertex_response": f"Error en el núcleo: {str(e)}", "sparks": 0})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
