from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
from modules.multimodal import VertexSensors
from modules.executor import SystemExecutor
from modules.notifier import VertexNotifier
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
notifier = VertexNotifier()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    content = reader.process(path)
    return jsonify({"filename": filename, "content": content})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        file_ctx = data.get("file_context", "")
        
        # 1. Ejecución de Terminal
        exec_ctx = sys_exec.execute(query.lower().replace("ejecuta", "").strip()) if "ejecuta" in query.lower() else ""
        
        # 2. Búsqueda Web
        web_ctx = scanner.search(query) if any(x in query.lower() for x in ["busca", "internet", "actualidad"]) else ""
        
        # 3. Datos de Sensores (APIs)
        api_ctx = hub.get_context(query)
        
        # 4. Síntesis Final
        full_query = f"[SYS: {sys_exec.fast_info()}]\n[FILE: {file_ctx}]\n[WEB: {web_ctx}]\n[EXEC: {exec_ctx}]\n[APIS: {api_ctx}]\nUsuario: {query}"
        
        response_text = brain.synthesize(full_query, [])
        audio_url = sensors.speak(response_text)
        
        return jsonify({"vertex_response": response_text, "audio_url": audio_url})
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo de núcleo: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
