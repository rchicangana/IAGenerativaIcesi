Taller Práctico #2

Caso de Estudio: Optimización de la Atención al Cliente en una Empresa
de E-commerce - Implementación de un Sistema RAG para IA Generativa

Introducción

En el taller anterior, exploramos el poder de los modelos de IA generativa para mejorar la
atención al cliente de EcoMarket para un set de dos tipos de prompts en particular. Ahora,
se desea extender la capacidad del modelo de atención al cliente para que pueda responder
ante cualquier tipo de solicitud, ya sea con la respuesta que parece correcta o haciéndole
saber al usuario que no tiene las herramientas para atender su solicitud.

Los modelos de propósito general tienen una limitación clave: a menudo carecen de
conocimiento específico y actualizado sobre la empresa, lo que puede llevar a respuestas
incorrectas o "alucinaciones". En este taller, superaremos esta limitación al introducir un
sistema RAG (Generación Aumentada por Recuperación). Un sistema RAG permite que
nuestro modelo de IA consulte una base de conocimiento interna antes de generar una
respuesta, asegurando que esta sea precisa, relevante y basada en los datos de la
empresa.

Fase 1: Selección de Componentes Clave del Sistema RAG

Antes de codificar, debemos tomar decisiones de arquitectura. En esta fase, los estudiantes
seleccionarán los componentes principales del sistema RAG.

Preguntas guía:

●  Modelo de Embeddings: ¿Qué modelo utilizarían para convertir los documentos de

la empresa en vectores numéricos? Justifiquen su elección basándose en la
precisión, el costo y la capacidad de manejar el idioma español. ¿Sería un modelo
de código abierto como los de Hugging Face o uno propietario?

●  Base de Datos Vectorial: ¿Dónde almacenarían estos vectores para que la

búsqueda por similitud sea eficiente? Exploren opciones como Pinecone, ChromaDB
o Weaviate. ¿Qué ventajas y desventajas tiene cada una para el caso de EcoMarket
(escalabilidad, costo, facilidad de uso)?

Fase 2: Creación de la Base de Conocimiento de Documentos

El éxito de un sistema RAG depende de la calidad de la información que puede recuperar.
En esta fase, los estudiantes prepararán la base de conocimiento para EcoMarket.

Pasos clave:

●

Identificación de Documentos: Identifiquen al menos 3 tipos de documentos de la
empresa de e-commerce que serían cruciales para el sistema de atención al cliente
(ejemplos: política de devoluciones en PDF, una hoja de cálculo con el inventario de
productos, un archivo JSON con preguntas frecuentes, etc.).

●  Segmentación (Chunking): ¿Cómo dividirían estos documentos en "fragmentos" o
chunks manejables? Discutan las diferentes estrategias de segmentación (por

●

tamaño fijo, por párrafos, de forma recursiva) y justifiquen por qué una estrategia es
mejor que otra para este caso de uso.
Indexación: Expliquen el proceso de tomar estos fragmentos, convertirlos en
vectores con el modelo de embedding seleccionado y cargarlos en la base de datos
vectorial.

Fase 3: Integración y Ejecución del Código

Esta es la fase práctica. Usaremos un framework popular para construir el flujo de RAG. El
objetivo es que los estudiantes entiendan cómo se conectan las diferentes piezas, llevando
a la práctica la propuesta realizada en las anteriores dos fases.

Generación del código:

1.  Preparación: El script rag_ejemplo.py utiliza la librería LangChain para simplificar
el proceso. Pueden también seguir el notebook que utilizamos en la sesión anterior
que consideraba LlamaIndex para la construcción del sistema RAG.

2.  Código para la propuesta realizada: Generar el código necesario para ajustar el
modelo del Taller Práctico #1 e incorporar el sistema RAG definido en este taller.
3.  Detallar limitaciones y suposiciones: En caso de tener limitaciones de recursos
para ejecutar la propuesta definida en este taller, detallar claramente la razón de
estas limitaciones y las suposiciones que se consideran para entender la
arquitectura presentada.

Forma de entrega: Link del repositorio de GitHub que contiene la respuesta a las tres fases.
Para las primeras dos, respuestas más textuales, los estudiantes deben usar algún formato
de  texto  como  Markdown  para  presentar  la  respuesta  necesaria.  Para  la  última  fase,  el
repositorio  mismo debe contener la estructura necesaria para ejecutar el código que utiliza
un sistema RAG para obtener mejores respuestas.

Rúbrica de Evaluación del Taller (5 Puntos)

1. Selección y Justificación de Componentes (1.25 puntos)

●  1.25 puntos: El estudiante selecciona un modelo de embedding y una base de
datos vectorial adecuados y justifica su elección de forma completa y bien
argumentada. La justificación considera factores clave como el rendimiento para el
idioma español, el costo, la escalabilidad y las ventajas/desventajas de las opciones
elegidas. Demuestra una comprensión profunda de cómo cada componente impacta
en la eficacia del sistema RAG.

●  0.7 puntos: El estudiante selecciona los componentes pero su justificación es

superficial o incompleta. La elección no está claramente ligada a las necesidades
específicas de EcoMarket o se basa en un solo factor (ej., solo la popularidad de la
herramienta).

●  0 puntos: La selección o la justificación de los componentes son incorrectas o

irrelevantes.

2. Creación de la Base de Conocimiento (1.25 puntos)

●  2 puntos: El estudiante identifica al menos 3 tipos de documentos relevantes y
propone una estrategia de segmentación (chunking) lógica y bien justificada
para el caso de estudio. Demuestra un entendimiento de cómo la calidad de los
documentos y la forma en que se dividen afectan directamente el rendimiento del
sistema RAG.

●  0.7 puntos: El estudiante identifica algunos documentos, pero no ofrece una
estrategia de chunking clara o su justificación es débil. No logra explicar la
importancia de este paso en el proceso de RAG.

●  0 puntos: El estudiante no identifica documentos relevantes o no presenta un plan

para la preparación de la base de conocimiento.

3. Comprensión del Código y la Integración (2.5 puntos)

●  2.5 puntos: El estudiante demuestra una clara comprensión de cada sección del
código proporcionado. Puede explicar cómo las piezas (modelo de embedding,
base de datos vectorial y chaining) se conectan para formar el sistema RAG. Logra
modificar el código o el prompt de forma exitosa para observar cambios en el
comportamiento del modelo.

●  1.25 puntos: El estudiante demuestra una comprensión parcial de cada sección
del código proporcionado. Si bien se evidencian los cambios necesarios para
agregar un sistema RAG, estos no son suficientes o no se ejecutan de la manera
esperada dados los requerimientos y el diseño presentado.

●  0 puntos: El estudiante no puede explicar la función de las diferentes partes del

código o no logra ejecutar o modificar el script de forma exitosa.

---

# Desarrollo del taller

## Fase 1: Selección de componentes clave del sistema RAG

### 1) Modelo de Embeddings seleccionado

**Propuesta:** `text-embedding-3-large` (OpenAI) para un entorno productivo inicial.

**Justificación:**

- **Precisión:** ofrece muy buen desempeño semántico multilingue (incluyendo espanol), clave para consultas de clientes con redaccion variada.
- **Costo/beneficio:** aunque es de pago, reduce tiempo de ajuste fino y de operacion inicial frente a alternativas open-source que exigen infraestructura y tuning.
- **Facilidad de integracion:** se integra directamente con LangChain, acelerando la construccion del MVP.
- **Riesgo controlado:** permite enfocarse primero en calidad de recuperacion; luego se puede optimizar costos con caché y/o migracion hibrida.

**Alternativa open-source para comparar (plan B):** `intfloat/multilingual-e5-base` o `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`.

- **Ventaja:** menor costo por token (si se ejecuta localmente).
- **Desventaja:** mayor complejidad operativa (GPU/CPU, latencia, versionado del modelo, monitoreo).

### 2) Base de datos vectorial seleccionada

**Propuesta:** `ChromaDB` para el taller/MVP.

**Comparacion breve:**

- **Pinecone**
  - Ventajas: alta escalabilidad, administrado, excelente para produccion.
  - Desventajas: costo recurrente, dependencia externa desde etapas tempranas.
- **ChromaDB (elegida)**
  - Ventajas: simple de usar localmente, rapida para prototipos, buena integracion con LangChain.
  - Desventajas: escalabilidad y gestion enterprise mas limitadas que Pinecone/Weaviate.
- **Weaviate**
  - Ventajas: motor potente, filtros y capacidades avanzadas.
  - Desventajas: mayor complejidad operativa para un curso si se compara con Chroma.

**Decision para EcoMarket (contexto de taller):**

- Empezar con **ChromaDB** para validar calidad de respuestas y flujo RAG.
- Migrar a **Pinecone o Weaviate** cuando el volumen de datos y concurrencia lo exijan.

---

## Fase 2: Creacion de la base de conocimiento de documentos

### 1) Identificacion de documentos clave (minimo 3)

Para EcoMarket, se proponen estos documentos como base inicial:

1. **Politicas de devolucion, cambios y garantias** (`.pdf`).
2. **Catalogo e inventario de productos** (`.csv` o `.xlsx`).
3. **FAQ de atencion al cliente** (`.json` o `.md`).
4. **Politicas de envios y cobertura por ciudades** (`.pdf` o `.md`).
5. **Guiones/protocolos de soporte** (`.docx` o `.md`).

Esto permite cubrir preguntas frecuentes sobre compras, stock, entregas, devoluciones y restricciones.

### 2) Estrategia de segmentacion (chunking)

**Estrategia elegida:** chunking **recursivo por estructura semantica** (encabezados/parrafos), con:

- `chunk_size = 700-900` caracteres
- `chunk_overlap = 120-180` caracteres

**Por que no solo tamano fijo:**

- El tamano fijo puro puede romper reglas importantes (por ejemplo, excepciones de una politica) y reducir precision.
- La segmentacion por parrafos/encabezados conserva contexto normativo y mejora recuperacion.

**Por que overlap:**

- Evita perder continuidad entre fragmentos contiguos.
- Mejora respuestas a preguntas que dependen de condiciones y excepciones en texto cercano.

### 3) Indexacion

Proceso propuesto:

1. Cargar documentos desde carpeta de conocimiento (`data/`).
2. Normalizar texto (codificacion, espacios, limpieza minima).
3. Dividir con `RecursiveCharacterTextSplitter`.
4. Generar embeddings por chunk.
5. Guardar en ChromaDB con metadatos: `fuente`, `tipo_doc`, `fecha_version`.
6. Exponer `retriever` con `k=4` o `k=5`.

Metadatos permiten trazabilidad y depuracion de respuestas.

---

## Fase 3: Integracion y ejecucion del codigo

## Estructura sugerida del repositorio

```text
.
├─ data/
│  ├─ politicas_devoluciones.pdf
│  ├─ faq.json
│  └─ inventario.csv
├─ rag_ejemplo.py
├─ requirements.txt
└─ README.md
```

## Codigo propuesto (`rag_ejemplo.py`)

```python
import os
from typing import List

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


PERSIST_DIR = "chroma_db"
DATA_DIR = "data"


def cargar_documentos() -> List:
    # En un proyecto real se agregan loaders por tipo (PDF, CSV, JSON, etc.).
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    docs = loader.load()
    return docs


def crear_vectorstore(docs: List) -> Chroma:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    return vectorstore


def obtener_vectorstore_existente() -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )


def construir_cadena_rag(vectorstore: Chroma):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template(
        """Eres un asistente de atencion al cliente de EcoMarket.
Responde SOLO con base en el contexto recuperado.
Si la respuesta no esta en el contexto, di explicitamente:
"No tengo informacion suficiente en la base de conocimiento para responder esa solicitud".

Contexto:
{context}

Pregunta:
{question}
"""
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def main():
    if not os.path.exists(PERSIST_DIR):
        docs = cargar_documentos()
        if not docs:
            print("No se encontraron documentos en data/.")
            return
        vectorstore = crear_vectorstore(docs)
    else:
        vectorstore = obtener_vectorstore_existente()

    rag_chain = construir_cadena_rag(vectorstore)

    print("Sistema RAG listo. Escribe 'salir' para terminar.")
    while True:
        pregunta = input("\nCliente: ").strip()
        if pregunta.lower() in {"salir", "exit", "quit"}:
            break
        respuesta = rag_chain.invoke(pregunta)
        print(f"Asistente: {respuesta}")


if __name__ == "__main__":
    main()
```

## `requirements.txt` sugerido

```txt
langchain
langchain-openai
langchain-community
langchain-chroma
chromadb
pypdf
pandas
python-dotenv
```

## Explicacion de integracion (comprension del codigo)

- **Embeddings:** convierten cada chunk en vectores semanticos.
- **Vector DB (Chroma):** almacena esos vectores y recupera los mas similares a la pregunta.
- **Retriever:** trae los `k` fragmentos mas relevantes.
- **Prompt + LLM:** el modelo genera respuesta usando solo el contexto recuperado.
- **Regla anti-alucinacion:** si no hay evidencia en contexto, responde que no tiene informacion suficiente.

## Limitaciones y supuestos

### Limitaciones

1. En esta version base se usa `DirectoryLoader` con `txt`; para PDF/CSV/JSON se deben agregar loaders especificos.
2. Dependencia de API externa (OpenAI) para embeddings y chat.
3. Sin reranking ni evaluacion automatica de calidad (precision@k, faithfulness).
4. Chroma local no es ideal para alta concurrencia en produccion.

### Supuestos

1. Los documentos de EcoMarket estan actualizados y versionados.
2. El dominio principal es espanol.
3. Existe una variable de entorno `OPENAI_API_KEY`.
4. Se prioriza rapidez de implementacion del MVP sobre optimizacion extrema de costos.

---

## Comandos de ejecucion (referencia)

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python rag_ejemplo.py
```

## Recomendaciones para mejorar la nota (rubrica)

1. Incluir ejemplos de preguntas reales y evidencia de respuesta correcta/incorrecta.
2. Mostrar al menos un ajuste experimental de `chunk_size`, `k` o prompt y su impacto.
3. Documentar por que la respuesta es confiable (fuente/metadatos del chunk usado).
4. Agregar una seccion corta de pruebas y casos limite.
