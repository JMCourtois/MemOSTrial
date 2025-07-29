# --- Importaciones ---
import uuid
import os
import shutil
from memos.configs.mem_os import MOSConfig
from memos.mem_os.main import MOS

# --- Configuración de Rutas ---
# Usamos la misma estructura de rutas que en el Trial01 para mantener la consistencia.
try:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd()))

CONFIG_PATH = os.path.join(PROJECT_ROOT, "examples/data/config/simple_memos_config.json")
MEM_CUBE_PATH = os.path.join(PROJECT_ROOT, "examples/data/mem_cube_2")


def initialize_mos(config_path: str) -> MOS:
    """Inicializa el sistema MemOS desde un archivo de configuración."""
    print("🤖 Inicializando MemOS para el chat...")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Archivo de configuración no encontrado: {config_path}. "
            "Asegúrate de haber descargado los ejemplos con 'memos download_examples'."
        )
    mos_config = MOSConfig.from_json_file(config_path)
    mos = MOS(mos_config)
    print("✅ ¡Listo para chatear!")
    return mos


def setup_user(mos: MOS, user_id: str, mem_cube_path: str):
    """
    Prepara al usuario para la sesión de chat.
    
    Crea el usuario si no existe y registra su cubo de memoria.
    """
    print(f"👤 Preparando al usuario '{user_id}'...")
    mos.create_user(user_id=user_id)
    mos.register_mem_cube(mem_cube_path, user_id=user_id)
    print("✅ Usuario listo.")


def chat_loop(mos: MOS, user_id: str):
    """
    Inicia un bucle de chat interactivo con el usuario.
    
    El asistente buscará en la memoria antes de responder y guardará
    automáticamente la información relevante de la conversación.
    """
    print("\n--- 💬 Inicio del Chat Interactivo ---")
    print("Escribe tu mensaje y presiona Enter. Escribe 'salir' o 'exit' para terminar.")
    
    conversation_history = []

    while True:
        user_input = input("Tú > ")
        if user_input.lower() in ["salir", "exit"]:
            print("🤖 ¡Hasta luego! La conversación ha sido guardada en la memoria.")
            break

        # Paso 1: Buscar en la memoria antes de generar una respuesta.
        # Esto permite al asistente usar contexto de conversaciones pasadas.
        print("🧠  Buscando en la memoria...")
        search_results = mos.search(query=user_input, user_id=user_id)
        found_memories = search_results.get("text_mem")

        # Paso 2: Generar una respuesta simple basada en si se encontraron memorias.
        assistant_response = ""
        if found_memories:
            # El recuerdo encontrado es un diccionario. Gracias al DEBUG, ahora conocemos su estructura.
            print(f"DEBUG: Estructura del resultado: {found_memories[0]}")
            
            # CORRECCIÓN FINAL: Navegamos la estructura de datos correcta.
            # 1. Obtenemos el primer diccionario de resultados.
            search_result = found_memories[0]
            # 2. Obtenemos la lista de objetos de memoria de la clave 'memories'.
            memory_items = search_result.get('memories')

            if memory_items:
                # 3. Tomamos el primer objeto de memoria (el más relevante).
                most_relevant_memory = memory_items[0]
                # 4. Accedemos a su atributo '.memory' para obtener el texto.
                memory_text = most_relevant_memory.memory

                assistant_response = f"Recuerdo que hablamos de algo relacionado. Mencionaste: '{memory_text}'. ¿Es correcto?"
                print(f"Asistente > {assistant_response}")
            else:
                # Si el resultado no contenía una lista de 'memories', lo notificamos.
                assistant_response = "He encontrado un recuerdo relevante, pero no he podido procesar su contenido. Lo tendré en cuenta."
                print(f"Asistente > {assistant_response}")
        else:
            # Si no hay memoria, damos una respuesta genérica.
            assistant_response = "Entendido. He tomado nota de eso."
            print(f"Asistente > {assistant_response}")

        # Paso 3: Añadir la nueva interacción a la memoria.
        # MemOS procesará esta conversación y decidirá qué es importante guardar.
        print("📝 Guardando conversación en la memoria...")
        
        # Construimos el formato de mensajes que `mos.add` espera.
        messages_to_add = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ]
        
        mos.add(messages=messages_to_add, user_id=user_id)
        print("-" * 20)


def main():
    """
    Función principal para ejecutar el chat interactivo con memoria.
    """
    # Usaremos un ID de usuario fijo para que la memoria persista entre sesiones.
    # En una aplicación real, esto sería el ID de inicio de sesión del usuario.
    USER_ID = "chat_user_01"
    
    mos = initialize_mos(CONFIG_PATH)
    setup_user(mos, USER_ID, MEM_CUBE_PATH)
    chat_loop(mos, USER_ID)


if __name__ == "__main__":
    main() 