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
        user_name = data.get("user_name", "Invitado")
        query = data.get("query", "")

        # 1. Obtener contexto (Lo que antes se quedaba solo en "recogiendo")
        context_data = hub.get_context(query)
        
        # 2. Generar respuesta REAL con el cerebro
        # Forzamos a que devuelva el texto final
        response_text = brain.synthesize(query, context_data)
        
        # 3. Lógica de Sparks (Sin simplificar)
        if user_name.lower() != "gemo":
            current = int(mem.get_data(f"sparks_{user_name}") or 10)
            if current <= 0:
                return jsonify({"vertex_response": "⚠️ Sparks agotados."})
            mem.set_data(f"sparks_{user_name}", current - 1)
            sparks_info = current - 1
        else:
            sparks_info = "∞"

        return jsonify({
            "vertex_response": response_text,
            "sparks_remaining": sparks_info
        })
    except Exception as e:
        return jsonify({"vertex_response": f"ERROR CRÍTICO: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
