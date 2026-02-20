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

    # below is the code to print the response of the llm 
     
    with st.chat_message("user",avatar="🧑"):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in bot.stream(
                {"messages":[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
        
    st.session_state["message_history"].append({'role':'assistant','content':ai_message})

