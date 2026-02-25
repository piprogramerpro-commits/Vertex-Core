from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
from modules.multimodal import VertexSensors
from modules.executor import SystemExecutor
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

hub = APIHub()
brain = VertexBrain()
reader = FileProcessor()
scanner = VertexSearch()
sensors = VertexSensors()
sys_exec = SystemExecutor()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(path)
    return jsonify({"content": reader.process(path), "filename": file.filename})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        file_ctx = data.get("file_context", "")
        
        # Procesos Autónomos
        web_ctx = scanner.search(query) if "busca" in query.lower() else ""
        exec_ctx = sys_exec.execute(query.lower().replace("ejecuta", "").strip()) if "ejecuta" in query.lower() else ""
        api_ctx = hub.get_context(query)
        
        full_query = f"[SISTEMA: {sys_exec.fast_info()}]\n[APIS]: {api_ctx}\n[WEB]: {web_ctx}\n[FILE]: {file_ctx}\n[EXEC]: {exec_ctx}\nUsuario: {query}"
        
        response_text = brain.synthesize(full_query, [])
        audio_url = sensors.speak(response_text)
        
        return jsonify({"vertex_response": response_text, "audio_url": audio_url})
    except Exception as e:
        return jsonify({"vertex_response": f"Error crítico: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
