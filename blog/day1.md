## Goal

Get a working ADK development environment and run a basic agent.

## What is ADK?

Google's Agent Development Kit (ADK) is an open-source framework for building AI agents in Python. Unlike simple chat interfaces, ADK agents can use tools, maintain state, and communicate with other agents.

## Environment Setup

**Prerequisites installed:**

- Xcode Command Line Tools (required for any dev work on macOS)
- Homebrew (package manager)
- Python 3.12 (ADK requires 3.10+)
- VS Code with Python extension

**Key learning:** ADK doesn't work with Python 3.9 — I hit cryptic `importlib.metadata` errors until upgrading to 3.12.

## Project Structure

ADK expects a specific layout:

```
~/adk-workshop/
├── venv/                  # Virtual environment
└── my_agent/              # Agent package
    ├── __init__.py        # Makes it a Python package
    └── agent.py           # Agent definition
```

## First Agent

The minimal agent code is surprisingly simple:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
```

Three things define an agent:

1. **name** — identifier (must match folder name)
2. **model** — which LLM powers it
3. **instruction** — system prompt shaping behavior

## Testing

ADK provides two interfaces:

**CLI:** `adk run my_agent`

- Quick testing in terminal
- Type messages, see responses

**Web UI:** `adk web`

- Visual chat interface
- Debug panel showing token counts, model responses, event details
- Session management

## Gotcha: Gemini API Quota

Hit a confusing `429 RESOURCE_EXHAUSTED` error with `limit: 0`. The API key was valid but the Generative Language API wasn't enabled in my Google Cloud project.

**Fix:** Get your API key from [AI Studio](https://aistudio.google.com/apikey) (not Google Cloud Console) for free tier access. If using `gemini-2.0-flash` has quota issues, switch to `gemini-2.5-flash`.

## Time Spent

~2 hours, mostly fighting environment issues. Once Python and API were configured correctly, the agent was running in minutes.

## Next Up

**Day 2:** Adding tools so the agent can actually *do* things, not just chat.
