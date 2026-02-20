import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph_database_backend import bot,retrieve_all_threads
from langsmith import uuid7
from langchain_openai import ChatOpenAI

st.title("Hello😎, Welcome!")


# ----------------------- UTILITIES -----------------------

# Always return thread_id as STRING
def generate_thread_id():
    return str(uuid7())


def reset_chat():
    new_thread = generate_thread_id()
    st.session_state['thread_id'] = new_thread
    add_threads(new_thread)
    st.session_state["message_history"] = []


def add_threads(thread_id: str):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id: str):
    state = bot.get_state(config={'configurable': {'thread_id': thread_id}})

    # SAFE ACCESS — prevents KeyError
    if hasattr(state, "values") and "messages" in state.values:
        return state.values["messages"]
    return []


# ----------------------- SESSION STATE -----------------------

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

# storing reaable titles as well 
if 'thread_title' not in st.session_state:
    st.session_state['thread_title']={}

add_threads(st.session_state['thread_id'])

# CONFIG MUST ALWAYS MATCH ACTIVE THREAD
def get_config():
    return {"configurable": {"thread_id": st.session_state['thread_id']}}

# ----------------------- LLM FOR AUTO TITLES -----------------------

title_llm = ChatOpenAI(model="gpt-4o-mini")

def generate_title(first_user_message):
    prompt = f"Generate a short chat title (max 6 words) for this message: {first_user_message}"
    return title_llm.invoke(prompt).content

# ----------------------- LOAD CHAT HISTORY -----------------------

for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])


# ----------------------- SIDEBAR -----------------------

st.sidebar.title("LangGraph ChatBot🐰")

if st.sidebar.button("NewChat 🐱"):
    reset_chat()

st.sidebar.header("Your Conversations 🐹")

for thread_id in st.session_state['chat_threads'][::-1]:
    title = st.session_state["thread_title"].get(thread_id, str(thread_id))
    if st.sidebar.button(title):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp.append({
                'role': role,
                'content': msg.content
            })
        st.session_state["message_history"] = temp
        st.rerun()


# ----------------------- MAIN CHAT INPUT -----------------------

user_input = st.chat_input("Type here...")

if user_input:

    # generating the title for thread_id
    if st.session_state['thread_id'] not in st.session_state["thread_title"]:
        title = generate_title(user_input)
        st.session_state["thread_title"][st.session_state['thread_id']] = title
    # Show user message
    st.session_state["message_history"].append({'role': 'user', 'content': user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.text(user_input)

    # Stream assistant response
    with st.chat_message("assistant", avatar="🤖"):
        ai_message = st.write_stream(
            chunk.content
            for chunk, meta in bot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=get_config(),
                stream_mode="messages",
            )
        )

    CONFIG = {
        "configurable":{"thread_id":st.session_state["thread_id"]},
        "metadata":{
            "thread_id":st.session_state["thread_id"]
        },
        "run_name":"chat_turn"
    }

    st.session_state["message_history"].append({'role': 'assistant', 'content': ai_message})
