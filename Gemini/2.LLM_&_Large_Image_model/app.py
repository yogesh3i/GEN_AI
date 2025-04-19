from dotenv import load_dotenv
load_dotenv() # loading all the envi. variables 

import streamlit as st 
import os 
import google.generativeai as genai 

# configure API key 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load the gemini models and get response 

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Creating our streamlit app 

st.set_page_config(page_title="Gemini Q&A Demo")

st.header("Geminin LLM Application")

input=st.text_input("Input:",key="input")
submit = st.button("Submit")


# when submit is clicked 
if submit:
    response =get_gemini_response(input)
    st.subheader("Here is the response buddy !")
    st.write(response)