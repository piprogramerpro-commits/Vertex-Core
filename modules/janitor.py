import os
import time
import shutil

class VertexJanitor:
    def __init__(self, folders=['static/uploads', 'static']):
        self.folders = folders

    def clean_old_files(self, max_age_seconds=3600):
        # Por defecto, borra lo que tenga más de 1 hora
        now = time.time()
        for folder in self.folders:
            if not os.path.exists(folder): continue
            for f in os.listdir(folder):
                f_path = os.path.join(folder, f)
                # No borramos el manifest ni carpetas esenciales
                if os.path.isfile(f_path) and not f.endswith(('.json', '.py', '.html')):
                    if os.stat(f_path).st_mtime < now - max_age_seconds:
                        os.remove(f_path)
                        print(f"[JANITOR]: Eliminado {f}")

    def get_disk_usage(self):
        total, used, free = shutil.disk_usage("/")
        return f"Disco: {used // (2**30)}GB usado de {total // (2**30)}GB"
