import datetime 
from typing import TypedDict 
from google.adk.agents import Agent,LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# 1) Define the simple function/tool 

def get_capital(country: str) -> str:

    """Return the capital of the given country"""
    capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
    return capitals.get(country.lower(), f"Sorry i dont know the capital of {country}")

# 2) Define the LLM agent 

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answer the question about capital cities.",
    instruction=(
        "You provide the capital of the country you have asked.\n"
        "When asked for capital call the get_capital(country).\n"
        "Respond concisely"
    ),
    tools=[get_capital],
)