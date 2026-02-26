from flask import Flask, request, jsonify
import os
from groq import Groq
from memory import init_db, save_interaction, get_history
from ai_backup import chat_backup

app = Flask(__name__)
init_db()

# --- CARGA DE VARIABLES DESDE RAILWAY ---
# El sistema las lee automáticamente de tu configuración
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
NASA_KEY = os.environ.get("NASA_API_KEY")
NEWS_KEY = os.environ.get("NEWS_API_KEY")
EXCHANGE_KEY = os.environ.get("EXCHANGERATE_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def home():
    status = "SISTEMA INTEGRADO: "
    status += "Groq OK, " if GROQ_API_KEY else "Groq OFF, "
    status += "NASA OK, " if NASA_KEY else "NASA OFF"
    return status

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    mensaje = data.get('message').lower()

    if email != ADMIN_EMAIL:
        return jsonify({"status": "denied", "message": "Acceso restringido."}), 403

    # LÓGICA DE RESPUESTA INTELIGENTE
    try:
        if "clima" in mensaje and WEATHER_KEY:
            # Aquí Vertex sabrá que tiene que usar la API del clima
            respuesta = f"Socio, detecto que quieres saber el clima. Usando tu clave: {WEATHER_KEY[:5]}..."
        elif "espacio" in mensaje or "nasa" in mensaje:
            respuesta = f"Consultando base de datos de la NASA con tu acceso..."
        elif client:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta = completion.choices[0].message.content
        else:
            respuesta = chat_backup(mensaje)
    except:
        respuesta = chat_backup(mensaje)

    save_interaction(email, mensaje, respuesta)
    return jsonify({"status": "success", "response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
