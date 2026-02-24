from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.memory import VertexMemory
import os

app = Flask(__name__)

# Inicialización de núcleos
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
        user_email = data.get("email", "anon_user")
        query = data.get("query", "")
        is_registered = data.get("is_registered", False)

        # 1. LÓGICA DE SPARKS (30 si es pro, 10 si es free)
        limit = 30 if is_registered else 10
        current = mem.get_data(f"sparks_{user_email}")
        current = int(current) if current is not None else limit

        if current <= 0:
            return jsonify({"vertex_response": "🛑 CRÉDITOS AGOTADOS. Sincroniza una cuenta Pro para continuar."})

        # 2. PROCESAMIENTO MULTI-API (Sin simplificar)
        # Obtenemos datos de las APIs externas
        context_data = hub.get_context(query)
        
        # 3. GENERACIÓN DE RESPUESTA (Aquí estaba el fallo)
        # Pasamos el query y los datos de las APIs al cerebro
        raw_response = brain.synthesize(query, context_data)
        
        # Si por algún motivo sale vacío, forzamos una respuesta de seguridad
        final_response = raw_response if raw_response else "El núcleo Vertex no pudo sintetizar una respuesta. Reintentando..."

        # 4. ACTUALIZACIÓN DE MEMORIA
        mem.set_data(f"sparks_{user_email}", current - 1)

        return jsonify({
            "vertex_response": final_response,
            "sparks_remaining": current - 1,
            "status": "success"
        })
    except Exception as e:
        print(f"Error detectado: {e}")
        return jsonify({"vertex_response": f"⚠️ ERROR DE NÚCLEO: {str(e)}", "status": "error"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
