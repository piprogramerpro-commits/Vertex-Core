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
        
        # Le pasamos la info al Hub para buscar el clima real
        context = hub.get_context(query)
        
        # Sintetizamos la respuesta
        vertex_res = brain.synthesize(query, context)
        
        sparks = mem.get_data(f"sparks_{email}")
        
        return jsonify({
            "vertex_response": vertex_res,
            "sparks_remaining": sparks if sparks else 0
        })
    except Exception as e:
        return jsonify({"vertex_response": f"Error: {str(e)}"})

if __name__ == '__main__':
    # Esto es lo que usaremos para detectar que estamos en Railway y NO en la Raspberry
    os.environ["ENV_TYPE"] = "RAILWAY" 
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
