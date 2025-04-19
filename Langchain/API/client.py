import requests
import streamlit as st 

def get_openai_response(input_text):
    try:
        response = requests.post("http://localhost:8000/essay/invoke",
                                 json={"input": {'topic': input_text}})
        response.raise_for_status()  # Check for request errors
        return response.json().get('output', {}).get('content', "Error: No content found")
    except Exception as e:
        return f"Error: {e}"


def get_ollama_response(input_text):
    try:
        response = requests.post("http://localhost:8000/poem/invoke",
                                 json={"input": {'topic': input_text}})
        response.raise_for_status()  # Check for request errors
        return response.json().get('output', {}).get('content', "Error: No content found")
    except Exception as e:
        return f"Error: {e}"


st.title("Langchain with OpenAI and Llama2")

essay_topic = st.text_input("Write an essay on:")
poem_topic = st.text_input("Write a poem on:")

# Fixing the essay part
if essay_topic:
    essay_response = get_openai_response(essay_topic)
    st.write("### Essay Output:")
    st.write(essay_response)

# Fixing the poem part
if poem_topic:
    poem_response = get_ollama_response(poem_topic)
    st.write("### Poem Output:")
    st.write(poem_response)
