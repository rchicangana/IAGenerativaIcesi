# Fase 1 — Diseño de la Arquitectura del Agente

Se selecciona el RAG como herramienta para consultar_politicas_ecomarket. El LLM con tool calling puede enrutar de forma implícita, es decir, si el prompt del sistema lo obliga a citar las políticas, el modelo aprende a llamar la tool antes de responder. Se gana simplicidad arquitectónica y se mantiene la observabilidad porque toda llamada a la tool queda registrada.

| Característica           | Router + RAG separado | RAG como Tool |
| ------------------------ | --------------------- | ------------- |
| Complejidad              | Media                 | Alta          |
| Flexibilidad             | Media                 | Alta          |
| Autonomía del agente     | Baja                  | Alta          |
| Escalabilidad            | Buena                 | Excelente     |
| Conversaciones complejas | Limitadas             | Muy buenas    |
| Control del flujo        | Determinístico        | Dinámico      |

## 3. Definición de las herramientas

Cumpliendo el mínimo de dos herramientas además del RAG, se definen tres:

### 3.1 `consultar_informacion_pedido`

| Atributo  | Detalle                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------ |
| Objetivo | Consultar la información del pedido sin disparar el flujo de devolución completo.                       |
| Entrada   | numero_pedido: string                                                                                  |
| Salida    | Datos básicos del pedido (cliente, productos, estado, fecha).    

### 3.2 `consultar_politicas_ecomarket`

| Atributo  | Detalle                                                                                                          |
| --------- | ---------------------------------------------------------------------------------------------------------------- |
| Objetivo | Búsqueda semántica sobre el la política de devoluciones que aplique a los productos del pedido. |
| Entrada   | consulta: string en lenguaje natural.                                                                             |
| Salida   | Chunks relacionados con la consulta    |

### 3.3 `generar_etiqueta_devolucion`

| Atributo        | Detalle                                                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Objetivo       | Producir la etiqueta de envío para retornar el producto.                                                                     |
| Entrada         | numero_pedido: string, listado_identificadores_productos: string[]                                                                                                                  |
| Seguridad       | Re-valida la elegibilidad internamente, aunque el agente ya lo haya hecho. Nunca confiar solo en el LLM para decisiones críticas. |
| Salida          | {exito: bool, codigo_etiqueta: str\|None, url_etiqueta: str\|None, mensaje: str}.    

## 4. Selección del marco de agentes

Se selecciona LanChain debido a:

- **Integración sencilla de herramientas :** LangChain permite registrar funciones de Python como herramientas (Tools) de manera simple y estructurada.

- **Compatibilidad con agentes:** Incluye múltiples tipos de agentes, como:

  - ReAct Agent
  - Tool Calling Agent
  - Conversational Agent

- **Facilidad para integrar RAG :** LangChain ya cuenta con componentes como:

  - Loaders
  - Embeddings
  - Vector Stores
  - Retrievers

- **Modularidad :** Permite separar claramente componentes como:

  - Router
  - Memoria
  - Herramientas
  - LLM
  - Recuperación documental

Aunque LlamaIndex es muy fuerte en recuperación documental y RAG, LangChain ofrece:

- mejor ecosistema de agentes
- mayor flexibilidad para tools y flujos de automatización más simples para este caso práctico.

## 5. Planificación del flujo de trabajo

# Diagrama de flujo del Agente EcoMarket

![Diagrama de flujo](flujo_agente_ecomarket.svg)

El flujo planteado inicia con el mensaje del usuario, el cual es procesado por el LLM para detectar la intención principal de la consulta. A partir de esta clasificación, el agente puede dirigir la conversación hacia uno de cuatro escenarios posibles:

- Consulta de información de un pedido.
- Solicitud de devolución.
- Solicitud de información general sobre documentos o políticas de la empresa.
- Mensajes fuera del alcance del agente o intentos de prompt injection.

En el flujo de devolución, el agente solicita inicialmente el identificador del pedido al usuario. Con este identificador, ejecuta la tool consultar_informacion_pedido, la cual permite obtener los datos asociados al pedido y sus productos.

De forma complementaria, el agente consulta el RAG mediante la tool consultar_politicas_ecomarket, con el objetivo de recuperar las políticas de devolución aplicables según las características de los productos del pedido.

Con la información obtenida desde ambas fuentes, el agente evalúa qué productos son elegibles para devolución y comunica al usuario las opciones disponibles. Posteriormente, el usuario selecciona el producto que desea devolver y el agente procede a ejecutar la tool generar_etiqueta_devolucion.

Finalmente, el agente entrega al usuario la información generada por la tool, incluyendo los datos y pasos necesarios para completar el proceso de devolución.