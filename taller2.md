# Desarrollo del taller

## Fase 1: Selección de componentes clave del sistema RAG

### 1) Modelo de Embeddings seleccionado

**Propuesta:** `text-embedding-3-large` (OpenAI) para un entorno productivo.

**Justificación:**

- **Precisión:** ofrece muy buen desempeño semántico multilingue (incluyendo español), clave para consultas de clientes con redaccion variada. Debido a que el modelo de embeddings tiene una dimensión de hasta 3072 se capturan mejor los matices semanticos lo que mejora directamente la calidad de los chunks recuperados y, por ende, la pertinencia de las respuestas.
- **Costo/beneficio:** aunque es de pago, reduce tiempo de ajuste fino y de operacion inicial frente a alternativas open-source que exigen infraestructura y tuning.
- **Riesgo controlado:** permite enfocarse primero en calidad de recuperacion; luego se puede optimizar costos con caché.

**Alternativa open-source para comparar (plan B):** `intfloat/multilingual-e5-base`.

- **Ventaja:** sin costo por token. Dimensión de 1024 vectores ofrece buena fidelidad semántica.
- **Desventaja:** mayor complejidad operativa (GPU/CPU, latencia, versionado del modelo, monitoreo). Menor precisión al realizar la búsqueda semántica.

### 2) Base de datos vectorial seleccionada

**Propuesta:** `ChromaDB` para el taller.

**Comparacion breve:**

- **Pinecone**
  - Ventajas: alta escalabilidad, administrado, excelente para produccion.
  - Desventajas: costo recurrente, dependencia externa desde etapas tempranas.
- **Weaviate**
  - Ventajas: alta escalabilidad, open source y capacidades avanzadas.
  - Desventajas: mayor complejidad de configuración y operativa.
- **ChromaDB (elegida)**
  - Ventajas: open source, simple de usar localmente, rapida para prototipos, buena integracion con LangChain.
  - Desventajas: escalabilidad y gestion enterprise mas limitadas que Pinecone/Weaviate.

**Decision para EcoMarket:**

- Empezar con **ChromaDB** para validar calidad de respuestas y flujo RAG.
- Migrar a **Pinecone** cuando el volumen de datos y concurrencia lo exijan.

---

## Fase 2: Creacion de la base de conocimiento de documentos

### 1) Identificacion de documentos clave (minimo 3)

Para EcoMarket, se proponen estos documentos como base inicial:

1. **Politicas de devolución, cambios y garantias** (`.md`).
2. **Catalogo e inventario de productos** (`.csv`).
3. **FAQ de atención al cliente** (`.json`).
4. **Politicas de envios** (`.md`).

Esto permite cubrir preguntas frecuentes sobre compras, stock, entregas, devoluciones y restricciones.

### 2) Estrategia de segmentación (chunking)

**Estrategia elegida:** chunking recursivo, con:
- chunk_size = 800 caracteres
- chunk_overlap = 150 caracteres

El splitter intenta cortar respetando esta jerarquía de separadores:
["\n\n", "\n", ".", " "], es decir, primero intenta partir entre párrafos,
luego entre oraciones, y solo como último recurso entre palabras.

**¿Por qué 800 caracteres y no menos?**

Los documentos de EcoMarket (políticas, FAQs, catálogo) contienen reglas
de negocio que rara vez se expresan en una sola oración. Una política de
devolución típica requiere 3-5 oraciones para completarse: condición,
plazo, excepción y procedimiento. Con chunk_size de 800 caracteres se
garantiza que esa unidad lógica completa cabe en un solo fragmento, sin
necesidad de ensamblar información de múltiples chunks. Valores menores
(ej. 300-400) fragmentarían estas reglas, obligando al modelo a inferir
información que no está en el contexto recuperado.

**¿Por qué no más de 800?**

Chunks muy grandes (1500+) reducen la precisión de la recuperación:
el vector resultante promedia demasiado contenido que no está relacionado, haciendo que el chunk sea "poco específico" y quede lejos semánticamente de la
consulta del usuario, aunque contenga la respuesta correcta.

**¿Por qué overlap de 150 caracteres?**

- 150 caracteres equivalen aproximadamente a 1-2 oraciones, que es
suficiente para capturar el "puente" entre dos chunks adyacentes.
- Evita perder continuidad entre fragmentos contiguos.
- Mejora respuestas a preguntas que dependen de condiciones y excepciones en texto cercano.

### 3) Indexacion

Proceso propuesto:

1. Cargar documentos desde carpeta de conocimiento (data/).
2. Dividir con RecursiveCharacterTextSplitter.
3. Generar embeddings por chunk.
4. Exponer retriever con k=4.

---

## Fase 3: Integracion y ejecucion del codigo

- Implementación con OPEN AI : [rag_ejemplo.py](https://github.com/rchicangana/IAGenerativaIcesi/blob/main/rag_ejemplo.py)
- Implementación con Ollama : [rag_ejemplo_ollama.py](http://github.com/rchicangana/IAGenerativaIcesi/blob/main/rag_ejemplo_ollama.py)

## Limitaciones y supuestos

### Limitaciones

1. Solo se sportan documentos con extensión MD, CSV, PDF y JSON. En caso de requerir otro tipo de extensión se debe adicionar en el código de forma manual.
2. Dependencia de API externa (OpenAI) para embeddings y chat.
3. Sin reranking de los resultado del RAG, ni evaluacion automatica de calidad.
4. Chroma local no es ideal para alta concurrencia en produccion.

### Supuestos

1. Los documentos de EcoMarket estan actualizados y versionados.
2. El dominio principal es espanol.
3. Existe una variable de entorno `OPENAI_API_KEY`.

### Preguntas de la entrega

- Cuando utilizábamos el modelo Qwen 3.5, independientemente de su tamaño, la herramienta entraba en un bucle de “razonamiento” y no llegaba a generar una respuesta. Sin embargo, al configurar reasoning=False, el problema desaparecía y el modelo respondía con normalidad. ¿A qué se debe este comportamiento?
