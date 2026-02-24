from modules.memory import VertexMemory
mem = VertexMemory()

print("🛰️ Conectando con Vertex Cloud Redis...")
mem.set_data('user_name', 'Gemo') # Pon aquí tu nombre
nombre = mem.get_data('user_name')

if nombre == 'Gemo':
    print(f"✅ ¡ÉXITO! Vertex recuerda que eres {nombre}.")
else:
    print("❌ Error de conexión.")
