# Taller 2 - Fase 3 (RAG EcoMarket)

Implementacion base de un sistema RAG para atencion al cliente usando LangChain + Chroma.
Incluye dos variantes:

- `rag_ejemplo.py` (OpenAI)
- `rag_ejemplo_ollama.py` (Ollama local)

## Requisitos

- Python 3.10+
- Para version OpenAI: API key de OpenAI
- Para version local: Ollama instalado y corriendo

## Estructura esperada

```text
.
├─ data/
│  ├─ faq.json
│  ├─ politicas_envio.md
│  └─ productos.csv
├─ rag_ejemplo.py
├─ rag_ejemplo_ollama.py
├─ requirements.txt
└─ README.md
```

## Instalacion

```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuracion OpenAI

Define la variable de entorno:

```powershell
$env:OPENAI_API_KEY="tu_api_key"
```

O usa archivo `.env` en la raiz:

```env
OPENAI_API_KEY=tu_api_key
```

## Ejecucion (OpenAI)

```bash
python rag_ejemplo.py
```

Si existe `chroma_db/`, reutiliza el indice. Si no existe, lo crea con los documentos de `data/`.

## Ejecucion (Ollama local)

1) Instala Ollama desde su sitio oficial: [https://ollama.com/](https://ollama.com/)

1) Descarga los modelos requeridos:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

1) Ejecuta la version local:

```bash
python rag_ejemplo_ollama.py
```

Esta version usa persistencia separada en `chroma_db_ollama/`.

## Notas

- El script soporta carga de `.txt`, `.md`, `.pdf`, `.csv` y `.json`.
- Si no encuentra contexto suficiente, responde explicitamente que no tiene informacion suficiente.
