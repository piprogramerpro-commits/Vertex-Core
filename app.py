from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "VERTEX_PRO_2026") # Para Render/Railway

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    session['identificado'] = True
    session['sparks'] = 20
    return jsonify({"status": "success", "sparks": 20})

@app.route('/chat', methods=['POST'])
def chat():
    # Si no hay sesión, denegamos
    if not session.get('identificado'):
        return jsonify({"response": "ACCESO DENEGADO. Registre su firma de socio primero."})
    
    mensaje = request.json.get('message', '').lower()
    
    # Lógica de respuesta profesional (Nash / Clima / Directivas)
    if "clima" in mensaje:
        res = "Socio, los sensores satelitales reportan condiciones estables. 22°C y visibilidad total."
    elif "dilema" in mensaje or "nash" in mensaje:
        res = "Análisis de Nash: La estabilidad matemática no justifica la violación de derechos. Se propone un equilibrio de Pareto mediante compensación fiscal del 99% hacia el 1% expropiado."
    else:
        res = "Directiva procesada en el núcleo Vertex. ¿Alguna otra orden, socio?"

    session['sparks'] = session.get('sparks', 20) - 1
    return jsonify({"response": res, "sparks": session['sparks']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
