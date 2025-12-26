# Image Creator Agent

This project implements an agent that generates images based on user prompts. It utilizes a root agent that delegates tasks to two sub-agents: a "prompter" and an "imager".

## Project Structure

- `image_creator_agent/`: Contains the core agent logic.
  - `agent.py`: Defines the root agent and its sub-agents.
  - `prompt.py`: Contains the prompt for the root agent.
  - `subagents/`: Contains the sub-agents.
    - `prompter/`: The prompter sub-agent, which likely refines or generates prompts.
    - `imager/`: The imager sub-agent, which likely generates the image.
- `deployment/`: Contains deployment scripts.
- `pyproject.toml`: Defines project metadata and dependencies.

## How it Works

The root agent receives a user request and uses its sub-agents to fulfill it. The `prompter` agent likely takes the initial user input and transforms it into a more detailed prompt suitable for image generation. The `imager` agent then takes this refined prompt and generates an image.

## Dependencies

The project uses the following key dependencies:

- `google-adk`
- `google-genai`
- `google-cloud`
- `pdfplumber`
- `google-cloud-aiplatform`
- `reportlab`
- `google-cloud-storage`
- `pymupdf`

## Usage

To use the agent, you would typically run the main script and provide a prompt for image generation.

_Further details on running the project would need to be added here, such as command-line examples._
