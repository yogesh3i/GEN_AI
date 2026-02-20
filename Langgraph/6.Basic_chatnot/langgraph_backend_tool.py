from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests

# ------------------------
# 1. Loading env variables
# ------------------------
load_dotenv()

# ------------------------
# 2. Load the LLM 
# ------------------------
llm = ChatOpenAI()
# ------------------------
# 3. Tools 
# ------------------------
# tool-1 
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool 
def calculator(first_num:float, second_num:float, operator: str) ->dict:

    """
    Perform the basic arithmatic operations on the given two numbers. 
    Supported operations: add, sub, multi, div
    """

    try:
        if operator=="add":
            result = first_num+second_num
        elif operator=="sub":
            result = first_num-second_num 
        elif operator=="multi":
            result = first_num*second_num 
        elif operator=="div":
            if second_num==0:
                return {"error":"Division by zero is not allowed"}
            else:
                result = first_num/second_num 

        return {"first_num":first_num, "second_num":second_num,"operator":operator,"result":result}

    except Exception as e:
        return {"error":str(e)}
    
# tool-2 
@tool 
def get_stock_price(symbol) -> dict:

    """
    Fetch the latest price of the given symbol (eg.'APPL','TSLA')
    Using alpha vintage with API key in the url.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    res = requests.get(url)
    return res.json()

# ------------------------
# 4. Bind the tool 
# ------------------------
tools = [search_tool,calculator,get_stock_price]
llm_with_tool = llm.bind_tools(tools)
# ------------------------
# 5. State of the graph 
# ------------------------
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
# ------------------------
# 6. Nodes
# ------------------------
# node-1
def chat_node(state:ChatState):
    """LLM node that may answer the question or request a tool call."""
    messages = state['messages']
    response = llm_with_tool.invoke(messages)
    return {"messages":[response]}
#node-2
tool_node = ToolNode(tools)

# ------------------------
# 7. Checkpointer
# ------------------------
conn = sqlite3.connect(database="botdb.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# ------------------------
# 8. State the graph and add the nodes
# ------------------------
graph = StateGraph(ChatState)
# ------------------------
# 9. Add nodes
# ------------------------
graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node)
# ------------------------
# 10. adding edges to the graph
# ------------------------
graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")
# ------------------------
# 11. compile the graph
# ------------------------
chatbot = graph.compile(checkpointer=checkpointer)

# ------------------------
# 12. Helper function to retrieve all the threads
# ------------------------

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)