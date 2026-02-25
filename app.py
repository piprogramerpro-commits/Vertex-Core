from flask import Flask, render_template, request, jsonify
from modules.security import VertexSecurity
# ... (otras importaciones)

app = Flask(__name__)
security = VertexSecurity()

@app.route('/ask', methods=['POST'])
def ask():
    # Anonimizamos al usuario inmediatamente
    user_ip = security.anonymize_ip(request.remote_addr)
    print(f"[SECURE_LOG]: Petición desde {user_ip}")
    
    data = request.json
    query = data.get("query", "")
    
    # Ciframos el rastro antes de cualquier proceso interno
    encrypted_query = security.encrypt_msg(query)
    
    # ... (lógica de procesamiento)
    response = brain.synthesize(query, [])
    
    return jsonify({
        "vertex_response": response,
        "security_status": "ENCRYPTED_AES256"
    })
