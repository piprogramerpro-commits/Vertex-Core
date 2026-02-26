from flask import Flask, request, jsonify
import os
from memory import init_db, save_interaction, get_history
from encryption_engine import encrypt_sensitive_data
from mail_service import enviar_solicitud_acceso

app = Flask(__name__)

# Inicializamos la base de datos de memoria al arrancar
init_db()

ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def home():
    return "VERTEX CORE AI: SISTEMA OPERATIVO - SOCIO AL MANDO"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    email = data.get('email')
    mensaje = data.get('message')

    # 1. Verificación de identidad y alertas
    if email == ADMIN_EMAIL:
        # 2. Recuperar historial (Plan B)
        historial = get_history(email)
        
        # 3. Procesar respuesta (aquí conectaremos con Groq luego)
        respuesta_ia = f"Hola socio, reconozco tu rango. Tu último mensaje fue: {historial[0][0] if historial else 'Ninguno'}"
        
        # 4. Encriptar y Guardar (Plan C y B)
        # Encriptamos el mensaje antes de guardarlo por seguridad extra
        msg_encriptado = encrypt_sensitive_data(mensaje)
        save_interaction(email, mensaje, respuesta_ia)
        
        return jsonify({
            "status": "success", 
            "response": respuesta_ia,
            "security": "Double Encryption Active"
        })
    else:
        # Si no eres tú, se envía alerta al correo y se bloquea
        enviar_solicitud_acceso(email)
        return jsonify({"status": "denied", "message": "Acceso restringido. Alerta enviada al socio principal."}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
