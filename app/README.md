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

-   **ID de Usuario Persistente**: Usamos un `user_id` constante (`"jean_the_learner"`) para que MemOS pueda cargar la misma memoria en cada ejecución.
-   **Configuración Explícita por Diccionario**: La forma más robusta de configurar MemOS en código es construir un diccionario que defina cada componente y pasarlo al constructor de `MOSConfig` usando el operador de desempaquetado de Python (`**`), así: `MOSConfig(**config_dict)`. Esto evita ambigüedades y nos da un control total.
-   **Jerarquía de Componentes**: Hemos aprendido que la configuración es jerárquica. El `mem_reader` (Lector de Memoria) es un componente complejo que tiene sus propios `llm`, `embedder` y `chunker` internos para procesar los recuerdos antes de almacenarlos.
-   **Separación de Tareas**: Nuestra configuración final usa:
    -   **Deepseek API** para el `chat_model` (hablar con el usuario).
    -   **Qwen (local)** para el `llm` del `mem_reader` (analizar recuerdos).
    -   **Sentence-Transformers (local)** para el `embedder` (vectorizar recuerdos).
    -   **Qdrant (local)** para la `vector_db` (almacenar y buscar vectores).
-   **Método `mos.chat()`**: El método de alto nivel que orquesta la recuperación de memoria, la generación de respuestas y el almacenamiento de nuevos recuerdos.

### Mini-Ejercicios

1.  **Crea un segundo perfil**: Copia `lesson2.py` a `lesson2_friend.py`. Dentro del nuevo archivo, cambia el `USER_ID` a otro nombre (ej: `"amigo_1"`). Habla con ambos bots y comprueba que sus memorias son completamente independientes.
2.  **Prueba los límites de la memoria**: En una conversación, dale al bot información contradictoria (ej: "Mi coche es rojo." y más tarde "Mi coche es azul."). En la siguiente sesión, pregúntale de qué color es tu coche y observa cómo maneja la contradicción. 