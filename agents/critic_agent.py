from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from models.ollama_model import get_llm

def critique_paper(text):
    prompt = PromptTemplate(
        input_variables=["content"],
        template="Critique the following academic paper content. Focus on strengths, weaknesses, and clarity:\n\n{content}"
    )
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(content=text)
