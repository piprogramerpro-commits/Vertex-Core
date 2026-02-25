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
        # Recogemos contexto de las APIs activas
        context = hub.get_context(query)
        # Procesamos con la IA (Llama 3.3 vía Groq)
        response = brain.synthesize(query, context)
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Error de sistema: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
