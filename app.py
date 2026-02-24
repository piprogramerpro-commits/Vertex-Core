from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.memory import VertexMemory
import os

app = Flask(__name__)
hub = APIHub()
brain = VertexBrain()
mem = VertexMemory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_name = data.get("user_name", "Invitado")
    query = data.get("query", "")
    
    # --- SISTEMA DE CRÉDITOS (SPARKS) ---
    if user_name.lower() != "gemo":
        sparks = int(mem.get_data(f"sparks_{user_name}") or 10)
        
        if sparks <= 0:
            return jsonify({"vertex_response": "⚠️ Te has quedado sin Sparks. ¡Vuelve mañana o invita a un amigo para recargar!"})
        
        # Consumir un Spark
        mem.set_data(f"sparks_{user_name}", sparks - 1)
    else:
        sparks = "∞" # Rango Dios tiene chispas infinitas

    # Lógica de respuesta
    a_data = hub.get_context(query)
    response_text = brain.synthesize(query, a_data)
    
    return jsonify({
        "vertex_response": response_text,
        "sparks_remaining": sparks,
        "is_admin": user_name.lower() == "gemo"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
