from flask import Flask, render_template, request, jsonify
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain
from modules.search_engine import VertexSearch
from modules.mail_service import VertexMail
from modules.invites import VertexInvites

app = Flask(__name__)

vault = VertexVault()
brain = VertexBrain()
scanner = VertexSearch()
mail_bot = VertexMail()
inviter = VertexInvites()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        email = data.get("email", "invitado@vertex.com")
        query = data.get("query", "")
        
        vault.add_user(email)
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Error: Energía insuficiente en la cuenta.", "sparks": 0})

        # Búsqueda web solo si es necesario para mantener profesionalidad
        context = scanner.search(query) if any(x in query.lower() for x in ["busca", "investiga", "noticias"]) else ""
        
        response = brain.synthesize(f"[CONTEXTO: {context}] Usuario: {query}", [])
        
        return jsonify({
            "vertex_response": response,
            "sparks": vault.get_sparks(email)
        })
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo en el núcleo: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
