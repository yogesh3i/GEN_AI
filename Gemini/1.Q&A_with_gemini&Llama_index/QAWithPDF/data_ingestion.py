import os
import sys
from llama_index.core import SimpleDirectoryReader
from logger import logging
from exception import CustomException

def load_data(uploaded_file=None):
    """
    Loads data from a user-uploaded file or the default 'Data' folder.
    """
    try:
        logging.info("🔄 Data loading started...")

        # If user uploads a file
        if uploaded_file:
            logging.info(f"📂 Processing user-uploaded file: {uploaded_file.name}")

            # Create a temporary folder for storing uploaded files
            temp_folder = "temp_data"
            os.makedirs(temp_folder, exist_ok=True)

            # Save the uploaded file temporarily
            temp_file_path = os.path.join(temp_folder, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Read the uploaded document
            loader = SimpleDirectoryReader(temp_folder)

        else:
            logging.info("📁 No file uploaded. Loading default 'Data' folder...")
            loader = SimpleDirectoryReader("Data")  # Load from default folder

        # Load documents
        documents = loader.load_data()
        logging.info("✅ Data loading completed.")

        return documents

    except Exception as e:
        logging.error("❌ Exception in loading data.")
        raise CustomException(e, sys)
