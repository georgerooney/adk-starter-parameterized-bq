from google.adk import Agent
from google.adk.tools.google_search_tool import google_search
from .prompt import PROMPT, DESCRIPTION

search_reviewer = Agent(
    name="search_reviewer_p",
    model="gemini-2.5-flash",
    description=DESCRIPTION,
    instruction=PROMPT,
    tools=[google_search],
)
