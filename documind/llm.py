import os
from langchain_ollama import ChatOllama

def get_llm(provider="ollama", model="llama3.2", api_key=None):
    provider = provider.lower()
    if provider == "ollama":
        return ChatOllama(model=model or os.getenv("OLLAMA_MODEL", "llama3.2"), temperature=0, num_ctx=2048)
    if provider == "groq":
        from langchain_groq import ChatGroq
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("Enter a Groq API key in the sidebar or configure GROQ_API_KEY in your deployment secrets.")
        return ChatGroq(model=model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"), temperature=0, api_key=key)
    raise ValueError("Unsupported provider. Choose ollama or groq.")

def generate_text(llm, prompt):
    response = llm.invoke(prompt)
    content = response.content
    return content if isinstance(content, str) else str(content)

