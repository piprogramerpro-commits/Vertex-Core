from flask import Flask, render_template, request, jsonify
from modules.api_hub import APIHub
from modules.ia_brain import VertexBrain
from modules.executor import SystemExecutor
from modules.file_processor import FileProcessor
from modules.search_engine import VertexSearch
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

hub = APIHub()
brain = VertexBrain()
sys_exec = SystemExecutor()
reader = FileProcessor()
scanner = VertexSearch()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get("query", "")
        
        # 1. ¿Es un comando de ejecución?
        exec_ctx = ""
        if "ejecuta" in query.lower() or "terminal" in query.lower():
            # Extraemos el comando (ej: "ejecuta ls -la")
            cmd = query.lower().replace("ejecuta", "").strip()
            exec_ctx = sys_exec.execute(cmd)
        
        # 2. Otros contextos
        api_ctx = hub.get_context(query)
        sys_info = sys_exec.fast_info()
        
        # 3. Síntesis
        full_query = f"[SISTEMA LOCAL: {sys_info}]\n[OUTPUT_COMANDO: {exec_ctx}]\n[APIS]: {api_ctx}\nUsuario: {query}"
        response = brain.synthesize(full_query, [])
        
        return jsonify({"vertex_response": response})
    except Exception as e:
        return jsonify({"vertex_response": f"Fallo en ejecución: {str(e)}"})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    return jsonify({"content": reader.process(path)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
