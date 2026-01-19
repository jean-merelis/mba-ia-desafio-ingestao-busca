import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector


def get_embeddings():
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")

    if openai_key:
        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model)
    elif gemini_key:
        model = os.getenv("GOOGLE_EMBEDDING_MODEL", "gemini-embedding-001")
        return GoogleGenerativeAIEmbeddings(model=model)
    else:
        raise ValueError("Nenhuma chave de API de embeddings configurada. Defina OPENAI_API_KEY ou GOOGLE_API_KEY.")


def get_vector_store(collection_name):
    connection_string = os.getenv("DATABASE_URL")
    if not connection_string:
        raise ValueError(
            "Erro: A connection_string do banco de dados não foi fornecida (variável de ambiente DATABASE_URL).")

    embeddings = get_embeddings()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection_string,
    )
    return vector_store
