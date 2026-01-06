# Create First ADK Agent

## Context

I'm setting up a Google ADK (Agent Development Kit) project on my Mac mini. I have:
- Python installed
- Virtual environment at `~/adk-workshop/venv` (already activated)
- ADK installed via pip
- `GOOGLE_API_KEY` set in environment

## Role

Act as a developer assistant helping me create my first ADK agent.

## Task

Create the following file structure inside `~/adk-workshop/`:

1. Create folder: `my_agent/`
2. Create empty file: `my_agent/__init__.py`
3. Create file: `my_agent/agent.py` with this content:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
```

## Constraints

- Do not modify venv folder
- Do not install any packages
- Just create the folder and two files
- Confirm when done
