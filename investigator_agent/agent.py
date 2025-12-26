from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.agent_tool import AgentTool

from .subagents.policy_review import policy_review
from .subagents.data_review import data_review
from .prompt import PROMPT, DESCRIPTION, PROMPT_DATA, PROMPT_POLICY

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description=DESCRIPTION,
    instruction=PROMPT_DATA,
    generate_content_config=types.GenerateContentConfig(temperature=0.1),
    tools=[
        AgentTool(agent=policy_review),
        AgentTool(agent=data_review),
    ],
)
