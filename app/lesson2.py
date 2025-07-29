import os
import uuid
from dotenv import load_dotenv
from memos import MOS, MOSConfig

# --- Setup ---
# Carga la clave de API de Deepseek desde el archivo .env
load_dotenv()

# La clave de la persistencia: un ID de usuario fijo.
USER_ID = "jean_the_learner"

def chat_session():
    """
    Inicia y gestiona una sesión de chat persistente con el agente de MemOS.
    """
    # --- Configuración del Agente ---
    # CORRECCIÓN FINAL: Construimos el objeto de configuración con la estructura
    # jerárquica correcta que espera MemOS, similar a un archivo JSON.
    print("1. Creando configuración personalizada completa...")
    
    mos_config = MOSConfig(
        # Componente para generar respuestas de chat.
        chat_model={"backend": "deepseek", "config": {}},

        # Componente para procesar y estructurar el texto antes de guardarlo.
        mem_reader={"backend": "simple_struct", "config": {}},

        # Componente para la memoria. Aquí definimos la memoria de texto.
        text_mem={
            "backend": "general_text",
            "config": {
                # Dentro de la memoria, definimos el embedder y la BBDD de vectores.
                "embedder": {"backend": "deepseek", "config": {}},
                "vector_db": {"backend": "qdrant", "config": {}}, # Usa Qdrant local por defecto
            }
        }
    )

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