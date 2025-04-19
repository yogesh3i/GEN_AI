from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 

import streamlit as st 
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Settign up the tracing and environment variables 

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] ="true"  # this is for langsmith tracking 
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

# Definign prompt template 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant, Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

# Defining the streamlit framework 

st.title("The ChatBot with Langchain and OPENAI API")
input_text = st.text_input("Search the topic u want")

# Calling OPENAI LLM 

llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parsers = StrOutputParser()
chain = prompt | llm | output_parsers

if input_text:
    st.write(chain.invoke({'question':input_text}))