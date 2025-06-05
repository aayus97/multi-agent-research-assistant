# app/chunking.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

CHROMA_PATH = "chroma_store"

def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def embed_chunks(chunks):
    embeddings = OllamaEmbeddings(model="llama3.2")  # or llama3, phi, etc.
    vectordb = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    vectordb.persist()
    return vectordb

def load_vectorstore():
    embeddings = OllamaEmbeddings(model="llama3.2")
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
