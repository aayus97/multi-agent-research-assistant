from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from models.ollama_model import get_llm

def get_summary(text):
    prompt = PromptTemplate(
        input_variables=["content"],
        template="Summarize the following academic content:\n\n{content}"
    )
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(content=text)
