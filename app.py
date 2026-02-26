from flask import Flask, request, jsonify
import os
from groq import Groq
from memory import init_db, save_interaction, get_history
from ai_backup import chat_backup

app = Flask(__name__)
init_db()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
ADMIN_EMAIL = "piprogramerpro@gmail.com"

# Intentamos inicializar Groq de forma segura
try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
    else:
        client = None
except Exception as e:
    print(f"Error iniciando Groq: {e}")
    client = None

@app.route('/')
def home():
    return "VERTEX CORE AI: MODO RESCATE ACTIVO"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    mensaje = data.get('message')

    if email != ADMIN_EMAIL:
        return jsonify({"status": "denied"}), 403

    # Si Groq falló en el arranque, usamos el backup directamente
    if client:
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta = completion.choices[0].message.content
        except:
            respuesta = chat_backup(mensaje)
    else:
        respuesta = chat_backup(mensaje)

    save_interaction(email, mensaje, respuesta)
    return jsonify({"status": "success", "response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
