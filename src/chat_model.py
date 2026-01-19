import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


def get_chat_model():
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")

    if openai_key:
        model = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
        return ChatOpenAI(model=model)
    elif gemini_key:
        model = os.getenv("GOOGLE_CHAT_MODEL", "gemini-2.5-flash")
        return ChatGoogleGenerativeAI(model=model)
    else:
        raise ValueError("Nenhuma chave de API de chat configurada. Defina OPENAI_API_KEY ou GOOGLE_API_KEY.")
