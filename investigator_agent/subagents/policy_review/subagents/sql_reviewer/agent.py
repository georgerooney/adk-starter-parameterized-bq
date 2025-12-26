from google.adk import Agent
from investigator_agent.tools.sql_tool import check_weather_event
from .prompt import PROMPT, DESCRIPTION

sql_reviewer = Agent(
    name="sql_reviewer_p",
    model="gemini-2.5-flash",
    description=DESCRIPTION,
    instruction=PROMPT,
    tools=[check_weather_event],
)
