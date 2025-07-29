import os
import uuid
from dotenv import load_dotenv
from memos import MOS, MOSConfig

# --- Setup ---
# Carga la clave de API de Deepseek desde el archivo .env
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    print("Error: DEEPSEEK_API_KEY no encontrada en el archivo .env")
    exit()

# La clave de la persistencia: un ID de usuario fijo.
USER_ID = "jean_the_learner"

def chat_session():
    """
    Inicia y gestiona una sesión de chat persistente con el agente de MemOS.
    """
    # --- Configuración del Agente ---
    # CORRECCIÓN FINAL: Usamos los nombres de backend correctos y la estructura precisa.
    print("1. Creando configuración personalizada completa y explícita...")
    
    config_dict = {
        # El LLM para chatear con el usuario final.
        "chat_model": {
            "backend": "deepseek",
            "config": {
                "api_key": DEEPSEEK_API_KEY,
                "model_name_or_path": "deepseek-chat",
            }
        },
        # El componente que lee, procesa y estructura la memoria.
        "mem_reader": {
            "backend": "simple_struct",
            "config": {
                # El "cerebro" interno del lector de memoria (el modelo Qwen local).
                "llm": {
                    "backend": "transformers", # Nombre correcto del backend
                    "config": {"model_name_or_path": "Qwen/Qwen1.5-0.5B-Chat"}
                },
                # El "embedder" para el lector de memoria.
                "embedder": {
                    "backend": "sentence-transformers", # Nombre correcto del backend
                    "config": {"model_name_or_path": "all-MiniLM-L6-v2"}
                },
                # El "chunker" para dividir el texto.
                "chunker": {
                    "backend": "sentence",
                    "config": {"chunk_size": 512, "chunk_overlap": 128}
                }
            }
        }
        # Nota: La vector_db (Qdrant) se configura por defecto al crear la memoria,
        # no se especifica en la configuración principal del MOS.
    }

    # Creamos el objeto MOSConfig a partir de nuestro diccionario.
    mos_config = MOSConfig(**config_dict)

    print("2. Inicializando el Sistema Operativo de Memoria (MOS)...")
    mos = MOS(mos_config)

    # --- Gestión de Usuario y Memoria ---
    print(f"3. Cargando o creando al usuario: {USER_ID}")
    mos.get_or_create_user(user_id=USER_ID)

    print("4. Registrando un cubo de memoria por defecto para el usuario...")
    mos.register_mem_cube(user_id=USER_ID)
    
    session_id = str(uuid.uuid4())
    print(f"\n¡Listo para chatear! Sesión actual: {session_id}")
    print("Escribe 'exit' o 'quit' para terminar la conversación.")
    print("-" * 30)

    # --- Bucle de Chat ---
    while True:
        try:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Agent: ¡Hasta luego! Ha sido un placer conversar contigo.")
                break

            response = mos.chat(user_input, user_id=USER_ID, session_id=session_id)
            
            print(f"Agent: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nAgent: Sesión terminada. ¡Adiós!")
            break

if __name__ == "__main__":
    chat_session() 