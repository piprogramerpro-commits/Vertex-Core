from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from models import init_user_db
from ai_backup import chat_backup

app = Flask(__name__)
init_user_db()

# Carga de Configuración de Socio
GROQ_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
ADMIN_EMAIL = "piprogramerpro@gmail.com"

# Estado de la cuenta (En memoria para este test)
session_data = {"sparks": 20, "version": "v2.3.2-Final", "status": "ONLINE"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje = data.get('message', '')
    
    if session_data["sparks"] <= 0:
        return jsonify({"status": "error", "response": "Socio, sistema bloqueado. Insuficientes Sparks."})

    respuesta = ""
    try:
        # LLAMADA REAL AL NÚCLEO (Sin respuestas predeterminadas)
        if client:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Eres Vertex Core AI. Profesional, serio, directo. Usa 'socio'. Responde con lógica técnica avanzada a cualquier tema (moral, mates, economía)."},
                    {"role": "user", "content": mensaje}
                ],
                temperature=0.5
            )
            respuesta = completion.choices[0].message.content
        else:
            respuesta = chat_backup(mensaje)

        # Lógica de Recompensa de Sparks (Basada en longitud/complejidad del input)
        if len(mensaje) > 150:
            recompensa = 5
            session_data["sparks"] += recompensa
            msg_sparks = f"\n\n[SISTEMA]: Reto complejo detectado. +{recompensa} Sparks abonados."
        else:
            session_data["sparks"] -= 1
            msg_sparks = ""

        return jsonify({
            "status": "success", 
            "response": respuesta + msg_sparks, 
            "sparks": session_data["sparks"]
        })

    except Exception as e:
        # Si todo falla, el backup procesa el mensaje real
        res_backup = chat_backup(mensaje)
        return jsonify({"status": "success", "response": f"[MODO EMERGENCIA]: {res_backup}"})

@app.route('/info')
def info():
    return jsonify(session_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
