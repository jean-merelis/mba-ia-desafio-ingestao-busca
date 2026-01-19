import argparse
import os

from dotenv import load_dotenv
from chat_model import get_chat_model
from search import search_prompt

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="RAG Chat Application")
    parser.add_argument("--collection_name", type=str, help="Nome da coleção de vetores")
    args = parser.parse_args()
    collection_name = args.collection_name or os.getenv("PG_VECTOR_COLLECTION_NAME", "document_vectors")

    model = get_chat_model()
    if not model:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Bem-vindo ao RAG Chat!")
    print(f"Usando coleção: {collection_name}")
    print("Este programa responde perguntas sobre o documento PDF ingerido.")
    print("Nota: Este chat não possui memória. Cada pergunta é tratada independentemente.")
    print("Digite sua pergunta abaixo. Para sair, digite 'sair', 'exit' ou 'q'.")
    print("-" * 50)

    while True:
        try:
            question = input("\nVocê: ").strip()
            if not question:
                continue

            if question.lower() in ["sair", "exit", "q"]:
                print("Encerrando o chat. Até logo!")
                break

            print("Processando...")
            response = search_prompt(collection_name, model, question)
            print(f"\nResposta: {response}")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nEncerrando o chat. Até logo!")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()
