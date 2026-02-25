from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.memory import VertexMemory
import os

app = Flask(__name__)
hub = APIHub()
brain = VertexBrain()
vault = VertexMemory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        email = data.get("email", "invitado@vertex.com") # Capturamos el email del usuario
        
        # 1. Sacamos contexto de APIs (Clima, bolsa, etc)
        api_context = hub.get_context(query)
        
        # 2. Sacamos contexto de MEMORIA (Lo que Vertex sabe de Gemo)
        user_prefs = vault.get_user_context(email)
        
        # 3. Mezcla maestra
        full_query = f"[SENSORS: {api_context}] [MEMORIA_USUARIO: {user_prefs}] Usuario: {query}"
        
        response = brain.synthesize(full_query, [])
        
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo en el sistema de memoria: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
