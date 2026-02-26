from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from models import init_user_db, register_user, check_user_status
from ai_backup import chat_backup
# Nota: mail_service debe estar configurado para enviar el correo a piprogramerpro@gmail.com

app = Flask(__name__)
init_user_db()

GROQ_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth/register', methods=['POST'])
def do_register():
    data = request.json
    name, email, pwd = data['name'], data['email'], data['pwd']
    if register_user(name, email, pwd):
        # Aquí llamarías a tu función de mail: enviar_solicitud(email)
        return jsonify({"status": "success", "msg": "Registro enviado. Espera validación del Socio Principal."})
    return jsonify({"status": "error", "msg": "Error en registro."})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    status, username = check_user_status(email)

    if email != ADMIN_EMAIL and status != 1:
        return jsonify({"status": "denied", "msg": "Acceso no validado por el Socio Principal."}), 403

    mensaje = data.get('message')
    try:
        if client:
            res = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": mensaje}])
            respuesta = res.choices[0].message.content
        else:
            respuesta = chat_backup(mensaje)
    except:
        respuesta = chat_backup(mensaje)

    return jsonify({"status": "success", "response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
