"""
Tool: consultar_politicas_ecomarket
Entrada : consulta en lenguaje natural (str)
Salida  : chunks relevantes recuperados del vector store (str)

Esta tool encapsula el RAG sobre los documentos de la carpeta data/.
Se construye con `build_consultar_politicas_ecomarket()` para inyectar
el vector store ya inicializado y evitar recrearlo en cada llamada.
"""

from pathlib import Path
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / "chroma_db_ollama"
EMBEDDING_MODEL = "nomic-embed-text-v2-moe:latest"


def _cargar_o_abrir_vectorstore() -> Chroma:
    """Carga documentos y crea el vectorstore si no existe, o lo reutiliza."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    if PERSIST_DIR.exists():
        return Chroma(
            persist_directory=str(PERSIST_DIR),
            embedding_function=embeddings,
        )

    # Construir desde cero
    loaders = [
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=False,
            silent_errors=True,
        ),
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=False,
            silent_errors=True,
        ),
    ]
    documentos = []
    for loader in loaders:
        documentos.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
    )


def build_consultar_politicas_ecomarket():
    """
    Fábrica que inicializa el vectorstore una vez y devuelve la tool lista
    para ser registrada en el agente.

    Uso:
        consultar_politicas = build_consultar_politicas_ecomarket()
        tools = [consultar_politicas, ...]
    """
    vectorstore = _cargar_o_abrir_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    @tool
    def consultar_politicas_ecomarket(consulta: str) -> str:
        """Realiza una búsqueda semántica sobre las políticas de EcoMarket.

        Recupera los fragmentos más relevantes de los documentos internos
        (política de devoluciones, FAQ, políticas de envío) según la consulta
        del cliente. Úsala siempre antes de evaluar la elegibilidad de una
        devolución o de responder preguntas sobre normas de la empresa.

        Args:
            consulta: Pregunta o descripción del cliente en lenguaje natural,
                      por ejemplo: '¿puedo devolver un shampoo sin abrir?'

        Returns:
            Texto con los fragmentos relevantes encontrados en la base de
            conocimiento, separados por líneas.
        """
        docs = retriever.invoke(consulta)
        if not docs:
            return (
                "No se encontró información relevante en la base de "
                "conocimiento de EcoMarket para esa consulta."
            )

        fragmentos = []
        for i, doc in enumerate(docs, start=1):
            fuente = doc.metadata.get("source", "documento interno")
            fragmentos.append(f"[Fragmento {i} — {fuente}]\n{doc.page_content}")

        return "\n\n---\n\n".join(fragmentos)

    return consultar_politicas_ecomarket
