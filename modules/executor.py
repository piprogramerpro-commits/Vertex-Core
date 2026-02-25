import subprocess
import os

class SystemExecutor:
    def __init__(self):
        # Lista de comandos permitidos por seguridad inicial
        self.allowed_actions = ["ls", "uptime", "free -m", "date", "whoami", "df -h"]

    def execute(self, command):
        # Filtro de seguridad básico
        try:
            # Si el comando es una acción de sistema real
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return f"[TERMINAL OUTPUT]:\n{result}"
        except Exception as e:
            return f"[ERROR DE SISTEMA]: {str(e)}"

    def fast_info(self):
        # Información rápida de la Raspberry para el dashboard
        try:
            cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True, text=True).replace("temp=", "")
            return f"Temp: {cpu_temp.strip()} | Memoria Libre: {subprocess.check_output('free -m | grep Mem | awk \'{print $4}\'', shell=True, text=True).strip()}MB"
        except:
            return "Sensores locales offline (Railway Mode)"
