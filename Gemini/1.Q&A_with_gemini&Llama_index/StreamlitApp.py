import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model
import os
    

def main():
    # Set page configuration
    
    st.title("📄 QA with Documents 😜 | Information Retrieval")

    # File uploader to accept user documents
    uploaded_file = st.file_uploader("📂 Upload your document (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])

    # Text input for user question
    user_question = st.text_input("💬 Ask your question:", placeholder="Type your query here...")

    if st.button("🚀 Submit & Process"):
        if not uploaded_file:
            st.warning("⚠️ Please upload a document before submitting.")
            return

        with st.spinner("🔄 Processing... Please wait."):
            # Load document from the user-uploaded file
            document = load_data(uploaded_file)

            # Load AI model
            model = load_model()

            # Generate query engine
            query_engine = download_gemini_embedding(model, document)

            # Get response from the model
            response = query_engine.query(user_question)

            # Display the response
            st.subheader("🤖 AI Response:")
            st.write(response.response)

if __name__ == "__main__":
    main()
