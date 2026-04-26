from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / "chroma_db_ollama"
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.1:8b"


def cargar_documentos() -> List:
    documentos = []
    loaders = [
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True,
            silent_errors=True,
        ),
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
            silent_errors=True,
        ),
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,
            silent_errors=True,
        ),
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.csv",
            loader_cls=CSVLoader,
            show_progress=True,
            silent_errors=True,
        ),
        DirectoryLoader(
            str(DATA_DIR),
            glob="**/*.json",
            loader_cls=JSONLoader,
            loader_kwargs={"jq_schema": ".", "text_content": False},
            show_progress=True,
            silent_errors=True,
        ),
    ]

    for loader in loaders:
        documentos.extend(loader.load())

    return documentos


def crear_vectorstore(documentos: List) -> Chroma:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
    )
    return vectorstore


def abrir_vectorstore_existente() -> Chroma:
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )


def construir_cadena_rag(vectorstore: Chroma):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template(
        """Eres un asistente de atencion al cliente de EcoMarket.
Responde unicamente con base en el contexto recuperado.
Si la informacion no aparece en el contexto, responde exactamente:
"No tengo informacion suficiente en la base de conocimiento para responder esa solicitud".

Contexto:
{context}

Pregunta:
{question}
"""
    )

    llm = ChatOllama(model=CHAT_MODEL, temperature=0)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def preparar_vectorstore() -> Chroma:
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            "No existe la carpeta 'data'. Crea la carpeta y agrega documentos."
        )

    if PERSIST_DIR.exists():
        return abrir_vectorstore_existente()

    documentos = cargar_documentos()
    if not documentos:
        raise ValueError("No se encontraron documentos compatibles en 'data'.")

    return crear_vectorstore(documentos)


def main():
    load_dotenv()

    print("Inicializando sistema RAG con Ollama...")
    print(
        f"Modelos esperados en Ollama: chat='{CHAT_MODEL}', embeddings='{EMBEDDING_MODEL}'"
    )
    vectorstore = preparar_vectorstore()
    rag_chain = construir_cadena_rag(vectorstore)
    print("Sistema RAG listo. Escribe 'salir' para terminar.")

    while True:
        pregunta = input("\nCliente: ").strip()
        if pregunta.lower() in {"salir", "exit", "quit"}:
            print("Sesion finalizada.")
            break
        if not pregunta:
            continue

        respuesta = rag_chain.invoke(pregunta)
        print(f"Asistente: {respuesta}")


if __name__ == "__main__":
    main()
