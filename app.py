from flask import Flask, request, jsonify
import os
from memory import init_db, save_interaction, get_history
from ai_backup import chat_backup

app = Flask(__name__)
init_db()

ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def home():
    return "VERTEX CORE AI: SISTEMA ONLINE - MOTOR HÍBRIDO ACTIVO"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    mensaje = data.get('message')

    if email != ADMIN_EMAIL:
        return jsonify({"status": "denied", "message": "Acceso restringido."}), 403

    # Lógica de Motor Híbrido
    try:
        # Aquí iría tu llamada a Groq... 
        # Si falla, saltamos al Plan B:
        respuesta = chat_backup(mensaje)
    except:
        respuesta = chat_backup(mensaje)

    save_interaction(email, mensaje, respuesta)
    return jsonify({"status": "success", "response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
