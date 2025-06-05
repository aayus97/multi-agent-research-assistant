from langchain.chains import RetrievalQAWithSourcesChain
from models.ollama_model import get_llm
from app.chunking import load_vectorstore

def answer_question_with_sources(question):
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    result = chain({"question": question})
    return {
        "answer": result["answer"],
        "sources": [doc.page_content for doc in result["source_documents"]]
    }
