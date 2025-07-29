# MemOS: Conceptos Clave Explicados

Este documento profundiza en algunos de los conceptos más importantes que encontramos durante nuestro aprendizaje de MemOS.

## La Arquitectura de Doble LLM: Chat vs. Memoria

En nuestra configuración actual, MemOS no usa un solo modelo de lenguaje (LLM), sino dos, cada uno con una función muy especializada. Comprender esta separación es clave para dominar MemOS.

### 1. El LLM de Chat (Externo, vía API)

-   **Modelo**: En nuestro caso, **Deepseek**.
-   **Función**: Es el responsable de la interacción directa con el usuario. Cuando nuestro `agent.chat()` envía una pregunta, es Deepseek quien genera la respuesta conversacional.
-   **Características**:
    -   Suele ser un modelo muy potente y de propósito general.
    -   Se accede a él a través de una API, por lo que requiere una clave (`API_KEY`) y una conexión a internet.
    -   Su uso puede tener un coste asociado por cada llamada a la API.

### 2. El LLM de Procesamiento de Memoria (Local)

-   **Modelo**: Un modelo descargado desde Hugging Face (por ejemplo, `microsoft/phi-2` o similar), especificado en el archivo de configuración `simple_memos_config.json`.
-   **Función**: Este es el "cerebro" interno de MemOS. No habla con el usuario. Su única tarea es recibir el texto de una conversación y realizar tareas de procesamiento sobre él, como:
    -   **Extracción de entidades**: Identificar personas, lugares, fechas...
    -   **Resumen**: Crear un resumen conciso de un bloque de texto.
    -   **Análisis de relevancia**: Decidir si un dato es lo suficientemente importante como para guardarlo en la memoria a largo plazo.
    -   **Estructuración**: Convertir texto plano en un formato de memoria más útil (como un grafo de conocimiento).
-   **Características**:
    -   Se ejecuta **localmente** en tu máquina (CPU/GPU).
    -   Se descarga automáticamente la primera vez que se usa.
    -   Una vez descargado, no requiere conexión a internet para funcionar.
    -   Su uso es gratuito (más allá del coste computacional de tu máquina).

### ¿Por qué esta separación?

Esta arquitectura es muy inteligente y eficiente:

-   **Coste**: Se utiliza el LLM de API (potencialmente caro) solo para las interacciones con el usuario, mientras que el trabajo pesado de procesar la memoria se realiza de forma gratuita a nivel local.
-   **Privacidad**: Las conversaciones se pueden procesar internamente para extraer recuerdos sin necesidad de enviar toda la transcripción a un servicio de terceros.
-   **Especialización**: Permite usar el mejor modelo para cada tarea: un LLM grande y creativo para el chat, y un LLM más pequeño y rápido optimizado para tareas de análisis de texto para la memoria. 