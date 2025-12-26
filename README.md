# ADK Starter Agent - Investigator Architecture

This project implements an investigator agent architecture designed to coordinate Data Review and Policy Review tasks using the Google ADK.

## Architecture

The system consists of a hierarchical agent structure:

1.  **Root Agent**: Orchestrates requests and delegates to the appropriate Level 1 sub-agent.
2.  **Level 1 Sub-agents**:
    - **Data Review Agent**: Specializes in data analysis and weather verification.
    - **Policy Review Agent**: Specializes in policy compliance and verification.
3.  **Level 2 Sub-agents** (Each Level 1 agent possesses these):
    - **SQL Reviewer**: Uses a parameterized SQL tool (`check_weather_event`) to query BigQuery public data (NOAA GSOD) for weather events.
    - **Search Reviewer**: Uses Google Search to find information not available in the database.

## Project Structure

```
investigator_agent/
├── agent.py            # Root Agent definition
├── prompt.py           # Root prompts and testing variables
├── tools/
│   └── sql_tool.py     # Parameterized SQL tool for weather checks
└── subagents/
    ├── data_review/
    │   ├── agent.py    # Data Review Agent
    │   ├── prompt.py
    │   └── subagents/
    │       ├── sql_reviewer/    # SQL Reviewer sub-agent
    │       └── search_reviewer/ # Search Reviewer sub-agent
    └── policy_review/
        ├── agent.py    # Policy Review Agent
        ├── prompt.py
        └── subagents/
            ├── sql_reviewer/    # SQL Reviewer sub-agent
            └── search_reviewer/ # Search Reviewer sub-agent
```

## Tools

- **check_weather_event**: A custom tool that queries BigQuery to verify if a specific weather event (fog, rain, snow, hail, thunder, tornado) occurred in a given US state on a specific date. Includes debug logging to console.
- **google_search**: Built-in ADK tool for web searching.

## Testing

The `investigator_agent/prompt.py` file includes auxiliary prompts to assist with focused testing:

- `PROMPT_DATA`: Forces the agent to route all requests to the **Data Review** agent.
- `PROMPT_POLICY`: Forces the agent to route all requests to the **Policy Review** agent.

## Deployment

The project includes deployment scripts in the `deployment/` directory.
Run the deployment script to deploy the agent to Vertex AI Reasoning Engine.
