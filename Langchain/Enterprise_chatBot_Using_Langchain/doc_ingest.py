from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS    

import os 

# function building 

def ingest_document(files):

    all_chunks=[]
    # files may be one or more 
    for file in files:
        temp_path = f"temp/{file.name}"
        with open(temp_path,"wb") as f:
            f.write(file.read())

        loader = PyPDFLoader(temp_path)
        document = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20
        )
        chunks = splitter.split_documents(document)
        all_chunks.extend(chunks)
        os.remove(temp_path)

    vector_store = FAISS.from_documents(all_chunks,OpenAIEmbeddings())
    return vector_store.as_retriever()