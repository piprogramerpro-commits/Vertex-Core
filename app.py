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
    try:
        data = request.json
        query = data.get("query", "")
        user_email = data.get("email", "anon")
        
        # 1. Obtener contexto real
        context = hub.get_context(query)
        
        # 2. SINTETIZAR (Esto ahora llamará a la lógica nueva)
        vertex_res = brain.synthesize(query, context)
        
        # 3. SPARKS
        current_sparks = mem.get_data(f"sparks_{user_email}")
        
        return jsonify({
            "vertex_response": vertex_res,
            "sparks_remaining": current_sparks if current_sparks else 0
        })
    except Exception as e:
        return jsonify({"vertex_response": f"Error crítico: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
