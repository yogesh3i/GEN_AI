import os
from dotenv import load_dotenv
import sys

from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from IPython.display import Markdown, display
import google.generativeai as genai
from exception import CustomException
from logger import logging

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

def load_model():
    
    """
    Loads a Gemini-Pro model for natural language processing.

    Returns:
    - Gemini: An instance of the Gemini class initialized with the 'gemini-pro' model.
    """
    try:
        Settings.llm = Gemini(model='models/gemini-1.5-pro',api_key=GOOGLE_API_KEY)
        return Settings.llm
    except Exception as e:
        raise CustomException(e,sys)
