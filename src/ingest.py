import argparse
import logging
import os
import sys
import time

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from tqdm import tqdm
from store import get_vector_store

load_dotenv()

# Configuração de Logs
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


# Função auxiliar com Tenacity para retry automático
@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=2, min=15, max=120),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def insert_batch(vector_store, batch, batch_ids):
    vector_store.add_documents(documents=batch, ids=batch_ids)


def ingest_pdf(pdf_path, collection_name, batch_size, batch_delay):
    if not pdf_path:
        print("Erro: O caminho do PDF não foi fornecido (via argumento ou variável de ambiente PDF_PATH).")
        return

    # Expandir caminho do usuário (ex: ~)
    pdf_path = os.path.expanduser(pdf_path)

    if not os.path.exists(pdf_path):
        print(f"Erro: O arquivo '{pdf_path}' não foi encontrado.")
        return

    print(f"Iniciando ingestão do arquivo: {pdf_path}")

    try:
        # 1. Carregar o PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        print(f"PDF carregado com sucesso. Total de páginas: {len(docs)}")

        # 2. Dividir o texto em chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        splits = text_splitter.split_documents(docs)
        if not splits:
            raise SystemExit(0)

        print(f"Texto dividido em {len(splits)} chunks.")

        # 3. Enriquecer documentos
        enriched = [
            Document(
                page_content=d.page_content,
                metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
            )
            for d in splits
        ]

        # 4 - Criar índice próprio
        ids = [f"doc-{i}" for i in range(len(enriched))]

        # 5. Inicializar Embeddings e Vector Store
        vector_store = get_vector_store(collection_name)

        print(f"Inserindo {len(splits)} vetores no banco de dados...")

        if batch_size <= 0:
            insert_batch(vector_store, enriched, ids)
        else:
            # Inserir documentos no banco em lotes
            print(f"Configuração: Batch Size = {batch_size}, Batch Delay = {batch_delay}s")

            for i in tqdm(range(0, len(enriched), batch_size), desc="Ingerindo batches"):
                batch = enriched[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]

                # Tenta inserir com retry automático
                insert_batch(vector_store, batch, batch_ids)

                # Pausa proativa para evitar Rate Limit
                if batch_delay > 0 and (i + batch_size < len(enriched)):
                    time.sleep(batch_delay)

        print("Ingestão concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro crítico durante a ingestão: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestão de PDF para Banco Vetorial")
    parser.add_argument("--pdf_path", type=str, help="Caminho para o arquivo PDF")
    parser.add_argument("--collection_name", type=str, help="Nome da coleção de vetores")
    parser.add_argument("--batch_size", type=int,
                        help="Tamanho do lote de documentos a serem inseridos por vez. Default 0 (sem batch)")
    parser.add_argument("--batch_delay", type=int,
                        help="Tempo de espera (em segundos) entre a inserção de lotes. Default 0")

    args = parser.parse_args()

    pdf_path = args.pdf_path or os.getenv("PDF_PATH")
    collection_name = args.collection_name or os.getenv("PG_VECTOR_COLLECTION_NAME", "document_vectors")
    batch_size = args.batch_size if args.batch_size is not None else int(os.getenv("BATCH_SIZE", 0))
    batch_delay = args.batch_delay if args.batch_delay is not None else int(os.getenv("BATCH_DELAY", 0))

    ingest_pdf(pdf_path, collection_name, batch_size, batch_delay)
