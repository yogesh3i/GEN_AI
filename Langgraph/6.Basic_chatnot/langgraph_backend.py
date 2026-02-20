# import the necessary libraires
from langgraph.graph import StateGraph, START, END 
from typing import TypedDict, Annotated 
from langchain_openai import ChatOpenAI 
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# load the dotev file 
load_dotenv()

# define the chatstate 

class chatstate(TypedDict):

    messages: Annotated[list[BaseMessage],add_messages]

# chatbot llm 

llm = ChatOpenAI()

# define the node functino to do chat 

def chat_node(state: chatstate) -> chatstate:

    # take user message 
    message = state['messages']
    # send it to llm and get hte response 
    response = llm.invoke(message)
    # response store state
    return {'messages':message+[response]}

# define the graph 
graph = StateGraph(chatstate)

# adding node to the graph 
graph.add_node('chat_node',chat_node)

# add edges to the graph 
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# adding checkpointer 
checkpointer = InMemorySaver()
# compile the graph 
bot = graph.compile(checkpointer=checkpointer)


'''
CONFIG = {'configurable':{'thread_id':'thread-1'}}

response= bot.invoke(
    {'messages':[HumanMessage(content='Hi My name is Yogesh')]},
    config=CONFIG
)

print(bot.get_state(config=CONFIG).values['messages'])

'''