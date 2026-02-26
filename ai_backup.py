import requests

HF_TOKEN = "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"
# Usaremos Mistral como modelo de respaldo por su gran equilibrio
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def chat_backup(prompt):
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]['generated_text'].split("[/INST]")[-1]
    except Exception as e:
        return f"Error en el motor de respaldo: {e}"
