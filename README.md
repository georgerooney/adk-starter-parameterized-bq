# ADK Starter Agent - Investigator Architecture

This project implements an investigator agent architecture designed to coordinate Data Review and Policy Review tasks using the Google ADK.

## Prerequisites

Ensure the Vertex AI Agent Engine service account has the necessary permissions to access BigQuery. Run the following command (replacing placeholders with your project details):

```bash
gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="serviceAccount:service-<PROJECT_NUMBER>@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="roles/bigquery.user"
```

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

The Investigator Agent can be deployed to Vertex AI Agent Engine using the following commands:

```bash
uv run --extra deployment deployment/deploy.py --create
```

When the deployment finishes, it will print a line like this:

```
Created remote agent: projects/<PROJECT_NUMBER>/locations/<PROJECT_LOCATION>/reasoningEngines/<AGENT_ENGINE_ID>
```

If you forgot the `AGENT_ENGINE_ID`, you can list existing agents using:

```bash
uv run --extra deployment deployment/deploy.py --list
```

The output will be like:

```
All remote agents:

123456789 ("root_agent")
- Create time: 2025-05-12 12:35:34.245431+00:00
- Update time: 2025-05-12 12:36:01.421432+00:00
```

You may interact with the deployed agent using the `test_deployment.py` script:

```bash
export USER_ID=<any string>
export AGENT_ENGINE_ID=<AGENT_ENGINE_ID>
uv run --extra deployment deployment/test_deployment.py --resource_id=${AGENT_ENGINE_ID} --user_id=${USER_ID}
```

The output will be like:

```
Found agent with resource ID: ...
Created session for user ID: ...
Type 'quit' to exit.
Input: Hello, what can you do for me?
Response: Hello! I'm a root investigator agent. I can help you coordinate reviews...
```

To delete the deployed agent, you may run the following command:

```bash
uv run --extra deployment deployment/deploy.py --delete --resource_id=${AGENT_ENGINE_ID}
```
