from google.adk.agents import LlmAgent
from pydantic import BaseModel,Field
from datetime import date

class TodoItem(BaseModel):

    task: str=Field(description="Task_name")
    due_date: date =Field(description="YYYY-MM-DD Format")
    priority:str = Field(description="low/medium/high")

# agent 
root_agent = LlmAgent(
    name="todo_agent",
    model="model/gemini-2.0-flash",
    instruction='''Generate todo items in exact JSON format,
    Make sure the format is strictly followed.
    Below is the fields you need to generate:
    1. task: Task name
    2. due_date: Due date in YYYY-MM-DD format
    3. priority: Priority of the task (low/medium/high)
    example output:
    {
        "task": "Call client",
        "due_date": "2023-10-10",
        "priority": "high"
    }
    ''',
    output_schema=TodoItem,
    output_key="todo"
)