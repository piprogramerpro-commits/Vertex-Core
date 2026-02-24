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
    
    # --- SISTEMA DE COMANDOS ---
    if query.lower() == "!top":
        try:
            all_keys = mem.db.keys("sparks_*")
            ranking = []
            for k in all_keys:
                u = k.replace("sparks_", "")
                s = mem.db.get(k)
                ranking.append(f"{u}: {s} ⚡")
            return jsonify({"vertex_response": "🏆 TOP USUARIOS: " + (" | ".join(ranking) if ranking else "¡Nadie aún!")})
        except Exception as e:
            return jsonify({"vertex_response": "Error accediendo al ranking."})

    # --- LÓGICA DE SPARKS ---
    if user_name.lower() != "gemo":
        current_sparks = int(mem.get_data(f"sparks_{user_name}") or 10)
        if current_sparks <= 0:
            return jsonify({"vertex_response": "❌ Te has quedado sin Sparks. ¡Vuelve mañana!"})
        mem.set_data(f"sparks_{user_name}", current_sparks - 1)
        display_sparks = current_sparks - 1
    else:
        display_sparks = "∞"
    
    # Respuesta IA
    a_data = hub.get_context(query)
    response_text = brain.synthesize(query, a_data)
    
    return jsonify({
        "vertex_response": response_text, 
        "sparks_remaining": display_sparks,
        "is_admin": user_name.lower() == "gemo"
    })

if __name__ == '__main__':
    # CRUCIAL PARA RAILWAY: Usar el puerto que nos asignan
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
