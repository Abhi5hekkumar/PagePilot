import os
from langchain_ollama import ChatOllama


def get_llm(provider="ollama", model=None, api_key=None):
    provider = (provider or "ollama").lower()

    if provider == "ollama":
        selected_model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        return ChatOllama(
            model=selected_model,
            temperature=0,
            num_ctx=2048,
        )

    if provider == "groq":
        from langchain_groq import ChatGroq

        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError(
                "Enter a Groq API key in the sidebar or configure "
                "GROQ_API_KEY in your deployment secrets."
            )

        selected_model = (
            model
            or os.getenv("GROQ_MODEL")
            or "openai/gpt-oss-20b"
        )

        return ChatGroq(
            model=selected_model,
            temperature=0,
            api_key=key,
        )

    raise ValueError("Unsupported provider. Choose ollama or groq.")


def generate_text(llm, prompt):
    response = llm.invoke(prompt)
    content = response.content
    return content if isinstance(content, str) else str(content)
