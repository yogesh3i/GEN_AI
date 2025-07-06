from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn 

from langserve import add_routes

load_dotenv()
# 1. Create the prompt template 
system_template = "Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ("system",system_template),
    ("user","{text}")
])

# 2. create the model

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",convert_system_message_to_human=True)

#3  output parser 

parser = StrOutputParser()

# 4. buil the chain

chain = prompt_template | model | parser 


# 5.Built the app langchain provide built in support to build API 

app = FastAPI(
    title ="Serving_with_Langserve",
    description="This is serve by Langserve",
    version="0.0.1"
)
# 6. 
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)