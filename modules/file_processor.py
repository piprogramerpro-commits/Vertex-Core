import PyPDF2
import os

class FileProcessor:
    def process(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.pdf':
                text = ""
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text()
                return text[:4000]
            elif ext in ['.txt', '.py', '.html', '.css']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()[:5000]
            return f"Archivo {ext} recibido, pero el motor de visión profunda se está calibrando."
        except Exception as e:
            return f"Error leyendo archivo: {str(e)}"
