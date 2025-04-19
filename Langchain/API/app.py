from fastapi import FastAPI 
from langchain.prompts import ChatPromptTemplate 
from langchain_openai import ChatOpenAI 
from langserve import add_routes 
import uvicorn 
import os 
from langchain_ollama.llms import OllamaLLM  # Corrected import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Creating FastAPI app  
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server"
)

# Define OpenAI model
model = ChatOpenAI()

# Define Open-source Llama2 model
lama = OllamaLLM(model="llama2")  # Corrected instantiation

# Creating the prompts 
prompt1 = ChatPromptTemplate.from_template("Write an essay about {topic} with 100 words.")
prompt2 = ChatPromptTemplate.from_template("Write a poem about {topic} with 100 words.")

# Adding routes 
add_routes(app, prompt1 | model, path="/essay")
add_routes(app, prompt2 | lama, path="/poem")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
