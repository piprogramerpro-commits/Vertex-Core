from flask import Flask, render_template, request, jsonify
import os, requests
from groq import Groq

app = Flask(__name__)

# Configuración de Motores
GROQ_KEY = os.environ.get("GROQ_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_MODEL = os.environ.get("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")

client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

# Estado del Socio
user_stats = {"sparks": 20, "is_logged": False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not user_stats["is_logged"]:
        return jsonify({"response": "ACCESO DENEGADO. Registre su firma de socio primero."})

    mensaje = request.json.get('message', '')
    
    # 1. Intento con GROQ (Principal)
    try:
        if client:
            res = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "system", "content": "Eres Vertex Core AI. Profesional y serio. Responde al dilema moral con lógica de Nash y justicia distributiva."},
                          {"role": "user", "content": mensaje}]
            )
            return jsonify({"response": res.choices[0].message.content, "sparks": user_stats["sparks"] + 5})
    except:
        pass

    # 2. Intento con HUGGING FACE (Respaldo Real)
    try:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        payload = {"inputs": f"<s>[INST] {mensaje} [/INST]", "parameters": {"max_new_tokens": 500}}
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        output = response.json()
        return jsonify({"response": output[0]['generated_text'].split("[/INST]")[1], "sparks": user_stats["sparks"] + 5})
    except Exception as e:
        return jsonify({"response": f"ERROR CRÍTICO: Motores fuera de línea. Verifique Tokens. {str(e)}"})

@app.route('/auth', methods=['POST'])
def auth():
    user_stats["is_logged"] = True
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
