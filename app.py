from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.memory import VertexMemory
from modules.search_engine import VertexSearch
import os

app = Flask(__name__)
hub = APIHub()
brain = VertexBrain()
vault = VertexMemory()
scanner = VertexSearch()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "").lower()
        email = data.get("email", "invitado@vertex.com")
        
        # 1. CONTEXTO DE SENSORES (APIs)
        api_context = hub.get_context(query)
        
        # 2. CONTEXTO DE MEMORIA (Recuerdos de Gemo)
        user_prefs = vault.get_user_context(email)
        
        # 3. CONTEXTO DE INTERNET (Búsqueda Autónoma)
        # Si la pregunta parece requerir info actual o desconocida
        web_context = ""
        if any(x in query for x in ["busca", "internet", "quien es", "que paso", "actualidad"]):
            web_context = scanner.search(query)
        
        # 4. SÍNTESIS MAESTRA
        full_query = f"""
        [SENSORES]: {api_context}
        [MEMORIA]: {user_prefs}
        [WEB_RESEARCH]: {web_context}
        [USUARIO]: {query}
        """
        
        response = brain.synthesize(full_query, [])
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo de sistema: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
