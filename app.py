from flask import Flask, render_template, request, jsonify
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
from modules.multimodal import VertexSensors
from modules.executor import SystemExecutor
from modules.notifier import VertexNotifier
from modules.mail_service import VertexMail
from modules.invites import VertexInvites

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicialización
vault = VertexVault()
brain = VertexBrain()
reader = FileProcessor()
scanner = VertexSearch()
sensors = VertexSensors()
sys_exec = SystemExecutor()
notifier = VertexNotifier()
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
            return jsonify({"vertex_response": "Energía insuficiente. Solicite recarga."})

        web_ctx = scanner.search(query) if "busca" in query.lower() else ""
        response = brain.synthesize(f"[WEB: {web_ctx}] Usuario: {query}", [])
        
        return jsonify({
            "vertex_response": response,
            "sparks": vault.get_sparks(email)
        })
    except Exception as e:
        return jsonify({"vertex_response": f"Error: {str(e)}"})

@app.route('/request_access', methods=['POST'])
def request_access():
    email = request.json.get("email")
    if inviter.request_access(email):
        notifier.send_alert(f"SOLICITUD: {email}")
        mail_bot.send_notification(email)
        return jsonify({"status": "Solicitud enviada a piprogramerpro@gmail.com."})
    return jsonify({"status": "Solicitud ya existente."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
