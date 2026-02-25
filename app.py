from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
import os

app = Flask(__name__)
hub = APIHub()
brain = VertexBrain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        history = data.get("history", [])
        
        # 🔍 EXTRACCIÓN DE CONTEXTO REAL (Jerez y APIs)
        context = hub.get_context(query)
        
        # 🧠 SÍNTESIS CONSCIENTE
        # Le pasamos el contexto a la IA para que no pregunte "dónde estás"
        full_query = f"[CONTEXTO ACTUAL: {context}] Usuario dice: {query}"
        
        response = brain.synthesize(full_query, history)
        
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Error en enlace: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
