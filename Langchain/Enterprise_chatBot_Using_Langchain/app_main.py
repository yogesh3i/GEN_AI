import streamlit as st 
from dotenv import load_dotenv
load_dotenv()

from chains import get_qa_chain
from doc_ingest import ingest_document
from utils import save_chat_to_csv

st.set_page_config(page_title="Advance Enterprise RAG Assistant",page_icon=":fish:" )
st.title("Enterprise Chat Assistant with RAG + ChatHistory + multiPDF")

