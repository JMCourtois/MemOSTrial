# MemOS with Deepseek: Learning Journal

This document tracks my progress learning the MemOS library with Deepseek.

## Lesson 1: Storing and Retrieving Your First Memory

### Purpose

Following the [official Quick Start guide](https://memos-docs.openmem.net/getting_started/quick_start), this lesson demonstrates the fundamental workflow of MemOS: configuring the system, creating a user, adding a memory, and then searching for it. This moves beyond a simple chat and into the core memory management features.

### Setup & Commands

1.  **Create a Virtual Environment (Recommended):**
    From the project root (`MemOSTrial/`), create and activate a virtual environment.
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate
    ```

2.  **Install & Run Ollama:**
    This setup uses Ollama to run a local AI model for memory processing.
    -   **Install Ollama:** Download and install the application from [ollama.com](https://ollama.com/download).
    -   **Download the model:** Open your terminal and run the following command. This will download the necessary model (`qwen:0.5b`) and start the Ollama service in the background. This download is only needed once.
    ```bash
    ollama run qwen:0.5b
    ```
    *You can close the chat that appears after the download finishes. The service will remain active.*

3.  **Install Python Dependencies:**
    With your virtual environment active, install all required packages using the `requirements.txt` file.
    ```bash
    # It's a good idea to ensure pip is up to date
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    This will install `MemoryOS` and its dependencies, including `torch`, `accelerate`, and `chonkie` for local model and memory processing.

4.  **Download MemOS Examples:**
    The script uses configuration files provided by the MemOS team. Run the following command from your project root to download them. This will create a new `examples/` directory.
    ```bash
    memos download_examples
    ```

5.  **Set API Key:**
    Create a file named `.env` inside the `/app` directory. Add your Deepseek API key to this file.
    ```
    DEEPSEEK_API_KEY="your_actual_api_key_here"
    ```

6.  **Run the Example:**
    Execute the script from the project root directory:
    ```bash
    python app/lesson1.py
    ```

### Key Concepts Introduced

This example uses the core, low-level components of MemOS:

-   **`MOS` (Memory Operating System)**: The central orchestrator for all memory-related operations.
-   **`MOSConfig`**: A configuration object that tells the `MOS` *how* to behave. The `simple_memos_config.json` file we use specifies a local `Qwen` model for memory analysis, which requires PyTorch, Accelerate, and Chonkie.
-   **User Management**: All memories are sandboxed per user via `create_user()`.
-   **`MemCube`**: A dedicated memory space for a user, registered with `register_mem_cube()`.
-   **`.add()` and `.search()`**: The fundamental methods for writing to and reading from a user's memory.

*Para una explicación más profunda de cómo MemOS utiliza diferentes modelos para el chat y la memoria, consulta nuestro [documento de conceptos clave](./concepts_explained.md).*

### Relevant Links
- [MemOS Docs: Quick Start](https://memos-docs.openmem.net/getting_started/quick_start)

---

## Lección 2: Chatbot con Memoria Persistente

### Propósito

El objetivo de esta lección es construir un chatbot interactivo en la terminal que recuerde la información entre diferentes sesiones. Esto demuestra la capacidad de persistencia de MemOS, que es su característica más potente.

### Setup y Comandos

La configuración es la misma que en la lección anterior. Asegúrate de que tu entorno virtual está activado.

1.  **Ejecutar el Chatbot:**
    Desde la carpeta raíz del proyecto (`MemOSTrial/`), ejecuta el siguiente comando:
    ```bash
    python app/lesson2.py
    ```

2.  **Interactuar con el Agente:**
    - Habla con el agente. Prueba a decirle algo sobre ti, como "Mi color favorito es el azul" o "Trabajo como desarrollador".
    - Cierra la conversación escribiendo `exit`.
    - Vuelve a ejecutar `python app/lesson2.py`.
    - Pregúntale al agente: "¿Cuál es mi color favorito?" o "¿A qué me dedico?". Debería responderte correctamente, demostrando que ha guardado y recuperado la memoria.

### Conceptos Clave

-   **ID de Usuario Persistente**: En lugar de generar un `uuid` nuevo cada vez, usamos un `user_id` constante (ej: `"jean_the_learner"`). Esto es fundamental, ya que MemOS asocia toda la memoria a este identificador único.
-   **`mos.get_or_create_user()`**: Este método es ideal para aplicaciones reales. Comprueba si un usuario con ese ID ya existe en su base de datos (`.memos/memos_users.db`) y carga su estado. Si no existe, lo crea por primera vez.
-   **Configuración por Backend**: La forma correcta de configurar MemOS en código es pasar un diccionario al constructor de `MOSConfig`. Este diccionario debe replicar la estructura jerárquica de la librería, especificando el `backend` y un `config` (aunque esté vacío) para cada componente principal:
    -   `chat_model`: El modelo que genera las respuestas.
    -   `mem_reader`: El componente que procesa el texto.
    -   `text_mem`: La configuración para la memoria textual, que a su vez contiene las configuraciones para el `embedder` y la `vector_db`.
-   **Método `mos.chat()`**: Este es el método de alto nivel para interactuar con el agente. Orquesta todo el proceso de forma automática:
    1.  **Recuperación**: Busca en la base de datos de vectores (Qdrant) recuerdos relevantes para la consulta actual del usuario.
    2.  **Aumentación**: Inserta los recuerdos encontrados en el *prompt* que se enviará al LLM (Deepseek), dándole contexto.
    3.  **Generación**: Envía el *prompt* aumentado a Deepseek para obtener una respuesta contextualizada.
    4.  **Almacenamiento**: Procesa la nueva interacción (pregunta + respuesta) y la añade a la memoria para futuras conversaciones.
-   **Persistencia Automática**: No necesitamos guardar nada manualmente. MemOS, a través de su `MOS` y la base de datos Qdrant configurada localmente, gestiona el almacenamiento y la carga de recuerdos en la carpeta `.memos/` cada vez que se ejecuta el script.

### Mini-Ejercicios

1.  **Crea un segundo perfil**: Copia `lesson2.py` a `lesson2_friend.py`. Dentro del nuevo archivo, cambia el `USER_ID` a otro nombre (ej: `"amigo_1"`). Habla con ambos bots y comprueba que sus memorias son completamente independientes.
2.  **Prueba los límites de la memoria**: En una conversación, dale al bot información contradictoria (ej: "Mi coche es rojo." y más tarde "Mi coche es azul."). En la siguiente sesión, pregúntale de qué color es tu coche y observa cómo maneja la contradicción. 