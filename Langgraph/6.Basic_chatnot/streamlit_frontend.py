'''
import streamlit as st

# THE PLACE HOLDER OF THE CHATS OF HUMAN AND THE AI 
with st.chat_message("user",avatar="🧑‍💻"):
    st.write("Hi")

# THE PLACE HOLDER OF THE CHATS OF HUMAN AND THE AI 
with st.chat_message("Assistat",avatar="🦖"):
    st.text("How can I help You ?")

# The chat input field 
user_input = st.chat_input("Type here....")

# to show the user inout on the UI as chat 
if user_input:
    with st.chat_message("user",avatar="🧑‍💻"):
        st.text(user_input)

# Try running the above code first and understand the flow 
'''

import streamlit as st 
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph_backend import bot

st.title("Hello😎, ChatBot Built Using Langgraph")

CONFIG = {'configurable': {'thread_id': 'thread-1'}}
# st.sesion_state helps to maintain the conversasion history in the chat 
if "message_history" not in st.session_state:
    st.session_state["message_history"]=[]

# load the full conversasion in the page 
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])


# user_inputs 
user_input = st.chat_input("Type here...")

if user_input:
    st.session_state["message_history"].append({'role':'user','content':user_input})
    with st.chat_message("user",avatar="🧑‍💻"):
        st.text(user_input)

    response = bot.invoke({"messages":[HumanMessage(content=user_input)]},config=CONFIG)
    ai_message = response['messages'][-1].content
    
    st.session_state["message_history"].append({'role':'assistant','content':ai_message})
    with st.chat_message("user",avatar="🧑"):
        st.text(ai_message)