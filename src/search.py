from langchain.prompts import PromptTemplate
from store import get_vector_store

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(collection_name, model, question):
    template = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )
    store = get_vector_store(collection_name)
    search_result = store.similarity_search_with_score(question, k=10)

    if not search_result:
        return "Não tenho informações necessárias para responder sua pergunta. Nenhum documento encontrado"

    context = "\n\n".join([doc.page_content for doc, score in search_result])

    prompt = template.format(pergunta=question, contexto=context)

    response = model.invoke(prompt)
    return response.content
