from gtts import gTTS
import os
from PIL import Image

class VertexSensors:
    def speak(self, text, filename="resp.mp3"):
        try:
            clean_text = text.replace('*', '').replace('#', '')
            tts = gTTS(text=clean_text[:300], lang='es')
            path = os.path.join('static', filename)
            tts.save(path)
            return f"/static/{filename}"
        except: return None

    def analyze_image(self, path):
        with Image.open(path) as img:
            return f"Imagen: {img.format} {img.size}"
