from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.memory import VertexMemory
import os

app = Flask(__name__)

# Inicialización de módulos
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
        email = data.get("email", "anon")
        is_reg = data.get("is_registered", False)
        
        # 1. Recoger datos de las 20 APIs
        context = hub.get_context(query)
        
        # 2. Sintetizar respuesta con Groq
        vertex_res = brain.synthesize(query, context)
        
        # 3. Gestión de Sparks (Memoria)
        try:
            current = mem.get_data(f"sparks_{email}")
            if current is None:
                current = 30 if is_reg else 10
            else:
                current = int(current)
            
            if current > 0:
                mem.set_data(f"sparks_{email}", current - 1)
                display_sparks = current - 1
            else:
                vertex_res = "⚠️ Créditos insuficientes. Sincroniza tu cuenta para más Sparks."
                display_sparks = 0
        except:
            display_sparks = "∞"

        return jsonify({
            "vertex_response": vertex_res,
            "sparks_remaining": display_sparks
        })
    except Exception as e:
        return jsonify({"vertex_response": f"ERROR CRÍTICO: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
