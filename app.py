from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from models import init_user_db, check_user_status
from ai_backup import chat_backup

app = Flask(__name__)
init_user_db()

GROQ_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    mensaje = data.get('message', '').lower()

    # Seguridad del Socio Principal
    if email != ADMIN_EMAIL:
        return jsonify({"status": "denied", "response": "Acceso restringido."}), 403

    respuesta = ""
    
    # Lógica Profesional
    try:
        if "bitcoin" in mensaje or "btc" in mensaje:
            # Aquí Vertex prioriza la búsqueda de datos financieros
            respuesta = "Socio, el Bitcoin está operando con alta volatilidad. Según los últimos datos de mercado, se sitúa aproximadamente en los $95,430 USD (esto es un análisis simulado, conectando con tu API de Exchange...). ¿Deseas un análisis técnico profundo?"
        elif client:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "system", "content": "Eres Vertex Core AI, un asistente profesional, serio y directo. Llamas 'socio' al usuario."},
                          {"role": "user", "content": mensaje}]
            )
            respuesta = completion.choices[0].message.content
        else:
            respuesta = chat_backup(mensaje)
    except Exception as e:
        # Evitamos el "Error 0" y enviamos al backup real
        respuesta = chat_backup(mensaje) if chat_backup(mensaje) != "0" else "Socio, el motor de respuesta está bajo mantenimiento. Reintente en unos segundos."

    return jsonify({"status": "success", "response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
