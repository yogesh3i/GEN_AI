# creating chains 
from langchain.chains import retrieval_qa
from langchain_openai import ChatOpenAI

def get_qa_chain(retriever):
    llm = ChatOpenAI(temperature=0)
    chain = retrieval_qa.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return chain