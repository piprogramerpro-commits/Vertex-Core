from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# CONFIGURACIÓN DE MANDO
ADMIN_EMAIL = "piprogramerpro@gmail.com"

@app.route('/')
def home():
    return "VERTEX CORE AI: SISTEMA OPERATIVO - COMANDANTE AL MANDO"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    
    if email == ADMIN_EMAIL:
        return jsonify({"status": "success", "role": "COMMANDER", "message": "Acceso total concedido"}), 200
    else:
        # Aquí es donde el 'Cacas' se queda fuera
        return jsonify({"status": "denied", "message": "Acceso restringido. Contacte con el administrador."}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
