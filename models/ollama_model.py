from langchain.llms import Ollama

def get_llm():
    return Ollama(model="llama3.2")  # or "phi" / "llama3"
