# ADK Workshop

Google Agent Development Kit (ADK) learning project with tools, structured outputs, and tests.

## Prerequisites

- macOS with Homebrew
- Python 3.12+ (`brew install python@3.12`)
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)

## Setup

```bash
# Create virtual environment
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install google-adk pydantic pytest

# Set API key
export GOOGLE_API_KEY="your-key-here"
```

## Project Structure

```
adk-workshop/
├── my_agent/
│   ├── __init__.py
│   └── agent.py          # Agent with tools and Pydantic models
├── tests/
│   └── test_tools.py     # pytest tests for tools
├── blog/
│   ├── day1.md           # Learning notes
│   └── day2.md
├── prompts/              # Reusable tutorial prompts
├── notes_ref/            # Setup instructions
└── README.md
```

## Run the Agent

```bash
source venv/bin/activate

# Web UI mode (recommended)
adk web

# CLI mode
adk run my_agent
```

## Features

- **Tools**: `get_weather`, `calculate`, `get_stock_price`
- **Structured Output**: Pydantic models for type-safe responses
- **Testing**: pytest tests for all tools

## Run Tests

```bash
pytest tests/ -v
```

## Configuration

Edit `my_agent/agent.py` to customize:

```python
from google.adk.agents import Agent
from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
    city: str
    temperature: int
    condition: str

def get_weather(city: str) -> WeatherResponse:
    """Get weather for a city."""
    return WeatherResponse(city=city, temperature=32, condition="Sunny")

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant with access to tools.",
    tools=[get_weather],
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 429 quota errors | Set up billing on Google Cloud or wait for quota reset |
| API key issues | Get key from AI Studio, not Cloud Console |
| No agents found | Run `adk web` from project root, not agent folder |

See `SETUP.md` for detailed troubleshooting steps.
