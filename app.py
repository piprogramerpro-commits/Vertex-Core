from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

hub = APIHub()
brain = VertexBrain()
reader = FileProcessor()
scanner = VertexSearch()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"})
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
        
        # 1. Radar de Internet (Si es necesario)
        web_ctx = ""
        if any(x in query.lower() for x in ["busca", "internet", "investiga", "actualidad"]):
            web_ctx = scanner.search(query)
            
        # 2. Sensores API
        api_ctx = hub.get_context(query)
        
        # 3. Síntesis
        full_query = f"[ARCHIVO]: {file_ctx}\n[WEB]: {web_ctx}\n[APIS]: {api_ctx}\nUsuario: {query}"
        response = brain.synthesize(full_query, [])
        
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Error de núcleo: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
