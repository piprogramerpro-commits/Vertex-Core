from flask import Flask, render_template, request, jsonify
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain

app = Flask(__name__)

# Inicializamos los módulos con el arsenal de APIs
vault = VertexVault()
brain = VertexBrain()

@app.route('/')
def index():
    # El punto de entrada al búnker
    return render_template('index.html')

@app.route('/check_auth', methods=['POST'])
def check_auth():
    try:
        data = request.json
        email = data.get("email", "").lower().strip()
        hwid = data.get("hwid", "")
        
        # Validación de rango y bypass
        access = vault.check_access(email, hwid)
        sparks = vault.get_sparks(email)
        
        return jsonify({
            "status": "success",
            "access": access,
            "sparks": sparks
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        email = data.get("email", "").lower().strip()
        hwid = data.get("hwid", "")
        query = data.get("query", "")
        
        # Verificamos autoridad antes de despertar a la IA
        access = vault.check_access(email, hwid)
        if access in ["COMMANDER", "USER_APPROVED"]:
            # Vertex procesa usando Groq y las APIs conectadas
            response = brain.synthesize(query, [])
            return jsonify({
                "vertex_response": response,
                "sparks": vault.get_sparks(email)
            })
        
        return jsonify({"vertex_response": "Acceso denegado. Este incidente será reportado.", "sparks": 0})
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo crítico en el núcleo: {str(e)}", "sparks": 0})

if __name__ == '__main__':
    # Configuración para Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
