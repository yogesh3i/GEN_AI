from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SentenceSplitter

from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model

import sys
from exception import CustomException
from logger import logging


def download_gemini_embedding(model,document):
    try:
        logging.info("")
        Settings.embed_model = GeminiEmbedding(model_name="models/embedding-001")
        Settings.transformations = [SentenceSplitter(chunk_size=800,chunk_overlap=20)]
        logging.info("")
        index = VectorStoreIndex.from_documents(document)
        index.storage_context.persist()

        logging.info("")
        query_engine = index.as_query_engine()
        return query_engine
    except Exception as e:
        raise CustomException(e,sys)