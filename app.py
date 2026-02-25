from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
import os

app = Flask(__name__)
hub = APIHub()
brain = VertexBrain()

# Diccionario temporal para guardar historial por sesión (en el servidor)
sessions_history = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        user_id = data.get("user_id", "default_gemo") # Identificador de sesión
        
        # Recuperar historial previo si existe
        history = sessions_history.get(user_id, [])
        
        # Contexto de APIs en tiempo real
        context = hub.get_context(query)
        
        # Respuesta de la IA con memoria
        response = brain.synthesize(query, history)
        
        # Actualizar historial en el servidor
        history.append({"type": "user", "text": query})
        history.append({"type": "vertex", "text": response})
        sessions_history[user_id] = history[-10:] # Guardamos los últimos 10 mensajes
        
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Error crítico: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
