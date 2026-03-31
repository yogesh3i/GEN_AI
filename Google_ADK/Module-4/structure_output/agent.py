from pydantic import BaseModel, Field

# structure validation of email content using pydantic 
class EmailContent(BaseModel):
    """Blueprint for email output."""
    subject: str = Field(description="Subject line of email, concise to 5-10 words.")
    body: str = Field(description="Formatted body with greeting, paragraph and signiture")






from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='email_agent',
    instruction="""
    Generate a professional email with:
        - clear subject line
        - Proper greeting closing
        - well-structured body
    Response MUST be in JSON format with the following keys:
    """,
    description='This agent provides an nice professional email.',
    output_schema=EmailContent,
    output_key='email'
)
