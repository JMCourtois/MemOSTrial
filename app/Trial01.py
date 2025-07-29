# --- Importaciones ---
# Importamos las librerías necesarias.
# - uuid: para generar identificadores únicos para los usuarios.
# - os: para interactuar con el sistema operativo, especialmente para manejar rutas de archivos.
# - shutil: para operaciones de alto nivel con archivos, como eliminar directorios.
# - MOSConfig y MOS: son los componentes centrales de la librería MemOS.
import uuid
import os
import shutil
from memos.configs.mem_os import MOSConfig
from memos.mem_os.main import MOS

# --- Configuración de Rutas ---
# Define y construye las rutas a los archivos y directorios necesarios.
# Hacerlo de forma dinámica asegura que el script funcione sin importar desde dónde se ejecute.
#
# PROJECT_ROOT: Se calcula la ruta raíz del proyecto para evitar problemas con rutas relativas.
try:
    # __file__ nos da la ruta del script actual. os.path.dirname() se usa dos veces
    # para subir del directorio 'app' a la raíz del proyecto.
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    # Si __file__ no está definido (ej. en un entorno interactivo), usamos el directorio actual.
    PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd()))

# Rutas a los archivos de configuración, el cubo de memoria y el directorio de volcado.
CONFIG_PATH = os.path.join(PROJECT_ROOT, "examples/data/config/simple_memos_config.json")
MEM_CUBE_PATH = os.path.join(PROJECT_ROOT, "examples/data/mem_cube_2")
DUMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
DUMP_PATH = os.path.join(DUMP_DIR, "my_mem_cube")


def initialize_mos(config_path: str) -> MOS:
    """
    Inicializa el sistema MemOS (MOS) a partir de un archivo de configuración.
    
    Esta función carga la configuración, crea una instancia del objeto MOS principal
    y la devuelve. También verifica que el archivo de configuración exista.

    Args:
        config_path (str): La ruta al archivo de configuración JSON.

    Returns:
        MOS: Una instancia inicializada del sistema MemOS.
    """
    print("1. Inicializando MemOS...")
    # Verificamos que el archivo de configuración exista antes de intentar cargarlo.
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Archivo de configuración no encontrado: {config_path}. "
            "Asegúrate de haber descargado los ejemplos con 'memos download_examples'."
        )
    # Creamos el objeto de configuración desde el archivo JSON y luego inicializamos MOS.
    mos_config = MOSConfig.from_json_file(config_path)
    mos = MOS(mos_config)
    print("✅ MemOS inicializado correctamente.")
    return mos


def setup_user_and_memory(mos: MOS, user_id: str, mem_cube_path: str):
    """
    Crea un nuevo usuario y registra un cubo de memoria para él.

    En MemOS, cada usuario tiene su propio espacio de memoria. Esta función
    se encarga de crear un usuario y asociarle un 'MemCube', que es donde
    se almacenarán sus memorias.

    Args:
        mos (MOS): La instancia del sistema MemOS.
        user_id (str): El identificador único para el nuevo usuario.
        mem_cube_path (str): La ruta al directorio del cubo de memoria a registrar.
    """
    print(f"\n2. Configurando el usuario '{user_id}'...")
    # Creamos el usuario en el sistema MOS.
    mos.create_user(user_id=user_id)
    print(f"   - Usuario '{user_id}' creado.")

    # Verificamos que el cubo de memoria exista.
    if not os.path.exists(mem_cube_path):
        raise FileNotFoundError(
            f"Cubo de memoria no encontrado: {mem_cube_path}. "
            "Asegúrate de haber descargado los ejemplos."
        )
    # Registramos (asociamos) el cubo de memoria con el usuario recién creado.
    mos.register_mem_cube(mem_cube_path, user_id=user_id)
    print(f"   - Cubo de memoria registrado para el usuario '{user_id}'.")
    print("✅ Configuración de usuario completa.")


def main():
    """
    Función principal que ejecuta el pipeline de ejemplo de MemOS.
    
    Esta función orquesta todos los pasos: inicialización, creación de usuario,
    adición de memoria, búsqueda, guardado y carga.
    """
    print("--- MemOS Quick Start: Ejemplo Estructurado ---")
    
    # Paso 1: Inicializar MemOS
    # Obtenemos una instancia del sistema MOS lista para usar.
    mos = initialize_mos(CONFIG_PATH)

    # Paso 2: Crear un usuario y configurar su memoria
    # Generamos un ID de usuario único para esta sesión y lo configuramos.
    user_id = str(uuid.uuid4())
    setup_user_and_memory(mos, user_id, MEM_CUBE_PATH)

    # Paso 3: Añadir una memoria para el usuario
    # Simulamos una interacción y la guardamos en la memoria del usuario.
    # El método `add` procesa los mensajes y extrae la información para almacenarla.
    print("\n3. Añadiendo memoria...")
    mos.add(
        messages=[
            {"role": "user", "content": "Me encanta jugar al fútbol."},
            {"role": "assistant", "content": "¡Qué genial!"}
        ],
        user_id=user_id
    )
    print("✅ Memoria añadida: 'Me encanta jugar al fútbol.'")

    # Paso 4: Buscar en la memoria
    # Realizamos una búsqueda semántica para recuperar la información que acabamos de guardar.
    print("\n4. Buscando en la memoria...")
    query = "¿Qué le encanta al usuario?"
    result = mos.search(query=query, user_id=user_id)
    # El resultado es un diccionario; la memoria de texto está en la clave "text_mem".
    found_memories = result.get("text_mem", "No se encontraron memorias.")
    print(f"   - Pregunta: '{query}'")
    print(f"   - Resultado: {found_memories}")
    print("✅ Búsqueda completada.")

    # Paso 5: Guardar el estado de la memoria (dump)
    # Persistimos el estado actual de todas las memorias en el disco para poder reanudar sesiones.
    print("\n5. Guardando el estado de la memoria...")

    # La función 'dump' requiere que el directorio de destino esté vacío.
    # Si el script se ha ejecutado antes, el directorio ya existirá y contendrá archivos.
    # Para evitar el error, lo eliminamos si existe.
    if os.path.exists(DUMP_PATH):
        print(f"   - El directorio de volcado '{DUMP_PATH}' ya existe. Limpiando...")
        shutil.rmtree(DUMP_PATH)

    # Creamos un directorio de volcado nuevo y vacío para la operación de guardado.
    os.makedirs(DUMP_PATH)

    # Pasamos el user_id para que sepa qué memoria de usuario guardar.
    mos.dump(DUMP_PATH, user_id=user_id)
    print(f"✅ Estado de la memoria guardado en: {DUMP_PATH}")

    # --- Fin de la Sesión 1 ---
    # Antes de iniciar una nueva sesión, debemos liberar la instancia anterior.
    # Esto suelta el bloqueo sobre la base de datos local (Qdrant), permitiendo
    # que la nueva sesión pueda acceder a ella.
    print("\n--- Terminando la primera sesión ---")
    print("   - Liberando la instancia de MOS para soltar el bloqueo de la base de datos...")
    del mos

    # Paso 6: Cargar el estado de la memoria en una nueva sesión
    print("\n6. Cargando el estado de la memoria en una nueva sesión...")
    new_mos_session = initialize_mos(CONFIG_PATH)

    # IMPORTANTE: El 'dump' guarda el *contenido* de la memoria, pero no la configuración
    # del usuario o qué cubos de memoria tiene. Por eso, debemos registrar al usuario
    # y su cubo de memoria en la nueva sesión antes de poder cargar los datos.
    print("   - Re-registrando el usuario y su cubo de memoria...")
    setup_user_and_memory(new_mos_session, user_id, MEM_CUBE_PATH)

    # Ahora, cargamos los datos del dump en el cubo de memoria recién registrado.
    print(f"   - Cargando contenido de la memoria desde '{DUMP_PATH}'...")
    try:
        # Primero, obtenemos el cubo de memoria que acabamos de registrar para el usuario.
        accessible_cubes = new_mos_session.user_manager.get_accessible_cubes(user_id)
        if not accessible_cubes:
            print("❌ Error: No se encontró un cubo de memoria accesible para el usuario después de registrarlo.")
            return

        mem_cube_id = accessible_cubes[0].cube_id
        mem_cube = new_mos_session.mem_cubes[mem_cube_id]
        
        # Luego, llamamos al método `load` directamente en el objeto MemCube.
        # Esto es simétrico a cómo funciona `dump`.
        mem_cube.load(DUMP_PATH)
        print("✅ Estado de la memoria cargado.")
    except AttributeError:
        print("❌ Error: El método `load` no se encuentra en el objeto MemCube. La API de la librería puede haber cambiado.")
        return
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al cargar la memoria: {e}")
        return


    # Paso 7: Verificar que la memoria se cargó correctamente
    # Realizamos la misma búsqueda en la nueva sesión para confirmar que los datos están ahí.
    print("\n7. Verificando la memoria cargada...")
    result_after_load = new_mos_session.search(query=query, user_id=user_id)
    verified_memories = result_after_load.get("text_mem", "No se encontraron memorias.")
    print(f"   - Buscando la misma memoria en la nueva sesión...")
    print(f"   - Resultado: {verified_memories}")

    if verified_memories:
        print("✅ ¡Verificación exitosa!")
    else:
        print("❌ Falló la verificación.")

    print("\n--- Ejemplo Finalizado ---")


# --- Punto de Entrada del Script ---
# El bloque `if __name__ == "__main__":` es el punto de entrada estándar para un script de Python.
# El código dentro de este bloque solo se ejecuta cuando el archivo se corre directamente.
if __name__ == "__main__":
    main()