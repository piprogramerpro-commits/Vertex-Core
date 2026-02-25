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
        email = data.get("email", "anon")
        is_reg = data.get("is_registered", False)
        
        context = hub.get_context(query)
        vertex_res = brain.synthesize(query, context)
        
        # Intentar obtener sparks, si falla Redis seguimos vivos
        try:
            current = mem.get_data(f"sparks_{email}")
            current = int(current) if current is not None else (30 if is_reg else 10)
            mem.set_data(f"sparks_{email}", current - 1)
        except:
            current = "∞"

        return jsonify({
            "vertex_response": vertex_res,
            "sparks_remaining": current
        })
    except Exception as e:
        return jsonify({"vertex_response": f"ERROR EN EL NÚCLEO: {str(e)}"})

if __name__ == '__main__':
    # IMPORTANTE: Railway necesita que el host sea 0.0.0.0
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
