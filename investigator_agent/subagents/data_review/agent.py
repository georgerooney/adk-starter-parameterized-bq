from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import PROMPT
from .subagents.sql_reviewer import sql_reviewer
from .subagents.search_reviewer import search_reviewer

data_review = Agent(
    name="data_review",
    model="gemini-2.5-flash",
    description="You are an expert in Data Review.",
    instruction=PROMPT,
    tools=[
        AgentTool(agent=sql_reviewer),
        AgentTool(agent=search_reviewer),
    ],
)
