from dotenv import load_dotenv
import streamlit as st 
import os 
import google.generativeai as genai 

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# loading the model and 
model = genai.GenerativeModel("models/gemini-1.5-pro")

chat = model.start_chat(history=[])

# function to get the response 

def get_gemini_response(question):

    response = chat.send_message(question,stream=True)
    return response 

# initializing the streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# initialize the  session state for the chat history 

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input",key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # adding user query an the response to the chat history 
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))

st.subheader("The chat history is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")