from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
from modules.multimodal import VertexSensors
from modules.executor import SystemExecutor
from modules.notifier import VertexNotifier
from modules.watcher import VertexWatcher

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
watcher = VertexWatcher(notifier)

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
        
        web_ctx = scanner.search(query) if "busca" in query.lower() else ""
        exec_ctx = sys_exec.execute(query.lower().replace("ejecuta", "").strip()) if "ejecuta" in query.lower() else ""
        
        full_query = f"[SYS: {sys_exec.fast_info()}]\n[FILE: {file_ctx}]\n[WEB: {web_ctx}]\n[EXEC: {exec_ctx}]\nUsuario: {query}"
        
        response_text = brain.synthesize(full_query, [])
        audio_url = sensors.speak(response_text)
        
        return jsonify({"vertex_response": response_text, "audio_url": audio_url})
    except Exception as e:
        return jsonify({"vertex_response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
from modules.janitor import VertexJanitor
janitor = VertexJanitor()

@app.route('/clean', methods=['POST'])
def clean_system():
    # Solo Gemo puede dar esta orden
    janitor.clean_old_files(max_age_seconds=0) # Borrado inmediato
    return jsonify({"status": "Sistema purificado", "storage": janitor.get_disk_usage()})
from modules.news_agent import VertexNewsAgent

news_bot = VertexNewsAgent(brain, notifier)

@app.route('/briefing', methods=['POST'])
def briefing():
    topic = request.json.get("topic", "IA y Economía")
    status = news_bot.get_morning_briefing(topic)
    return jsonify({"status": status})
