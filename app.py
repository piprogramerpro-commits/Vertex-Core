from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from modules.vault import VertexVault
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
from modules.multimodal import VertexSensors
from modules.executor import SystemExecutor
from modules.notifier import VertexNotifier

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

vault = VertexVault()
brain = VertexBrain()
reader = FileProcessor()
scanner = VertexSearch()
sensors = VertexSensors()
sys_exec = SystemExecutor()
notifier = VertexNotifier()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        email = data.get("email", "invitado@vertex.com")
        query = data.get("query", "")
        file_ctx = data.get("file_context", "")
        
        vault.add_user(email)
        if not vault.use_spark(email):
            return jsonify({"vertex_response": "Energía insuficiente. Contacte con el administrador."})

        web_ctx = scanner.search(query) if "busca" in query.lower() else ""
        exec_ctx = sys_exec.execute(query.lower().replace("ejecuta", "").strip()) if "ejecuta" in query.lower() else ""
        
        full_query = f"CONTEXTO_SISTEMA: {sys_exec.fast_info()}\nCONTEXTO_ARCHIVO: {file_ctx}\nCONTEXTO_WEB: {web_ctx}\nCOMANDO_EJECUTADO: {exec_ctx}\nUSUARIO: {query}"
        
        response = brain.synthesize(full_query, [])
        audio_url = sensors.speak(response)
        
        return jsonify({
            "vertex_response": response, 
            "audio_url": audio_url,
            "sparks": vault.get_sparks(email)
        })
    except Exception as e:
        return jsonify({"vertex_response": f"Error de núcleo: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
