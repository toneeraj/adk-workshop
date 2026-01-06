# ADK Workshop

Google Agent Development Kit (ADK) project with a basic agent.

## Prerequisites

- macOS with Homebrew
- Python 3.12+ (`brew install python@3.12`)
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup

```bash
# Create virtual environment
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate

# Install ADK
pip install google-adk

# Set API key
export GOOGLE_API_KEY="your-key-here"
```

## Project Structure

```
adk-workshop/
├── venv/                 # Virtual environment
├── my_agent/
│   ├── __init__.py
│   └── agent.py          # Agent definition
├── notes_ref/            # Setup instructions
├── README.md
└── SETUP.md              # Detailed setup guide
```

## Run the Agent

```bash
# Activate environment
source venv/bin/activate

# CLI mode
adk run my_agent

# Web UI mode
adk web my_agent
```

## Configuration

Edit `my_agent/agent.py` to customize:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",  # or gemini-2.5-pro
    instruction="You are a helpful assistant. Be concise and friendly.",
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 429 quota errors | Use `gemini-2.5-flash` instead of `gemini-2.0-flash` |
| Python version error | Use Python 3.12+ via Homebrew |
| API key issues | Get key from AI Studio, not Cloud Console |

See `SETUP.md` for detailed troubleshooting steps.
