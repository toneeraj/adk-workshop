## Goal

Add tools to the agent, experiment with local LLMs, and implement structured outputs with Pydantic.

## What Are Tools?

Tools are Python functions that an agent can call to perform actions. Instead of just generating text, an agent with tools can fetch data, call APIs, or interact with systems.

ADK uses the function's type hints and docstring to tell the LLM what the tool does and what parameters it accepts.

## Adding Multiple Tools

Started with simple string-returning tools:

```python
from google.adk.agents import Agent

def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Returns: "Weather in Delhi: 32°C, Sunny"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    # Returns: "2 + 2 = 4"

def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a symbol."""
    # Returns: "AAPL is currently trading at $178.50"

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant with access to tools.",
    tools=[get_weather, calculate, get_stock_price],
)
```

## Structured Outputs with Pydantic

Instead of returning strings, tools can return **Pydantic models** for structured data:

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR CODE                                │
│  1. Define Pydantic models (WeatherResponse, etc.)              │
│  2. Tools return these models instead of strings                │
│  3. Register tools with agent                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          ADK                                    │
│  4. Reads your Pydantic models                                  │
│  5. Tells LLM "this tool returns {city, temperature, condition}"│
│  6. Validates tool output matches the model                     │
│  7. Converts to JSON for transport                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          LLM                                    │
│  8. Receives structured data from tool                          │
│  9. Formats it into natural language for user                   │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
from google.adk.agents import Agent
from pydantic import BaseModel, Field

# Define structured output models
class WeatherResponse(BaseModel):
    """Structured weather data"""
    city: str = Field(description="Name of the city")
    temperature: int = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition like Sunny, Rainy, etc.")

class StockResponse(BaseModel):
    """Structured stock data"""
    symbol: str = Field(description="Stock ticker symbol")
    price: float = Field(description="Current stock price in USD")
    currency: str = Field(default="USD", description="Currency")

class CalculationResponse(BaseModel):
    """Structured calculation result"""
    expression: str = Field(description="The math expression")
    result: float = Field(description="The calculated result")

# Tools return Pydantic models
def get_weather(city: str) -> WeatherResponse:
    """Get the current weather for a city."""
    weather_data = {
        "delhi": {"temperature": 32, "condition": "Sunny"},
        "mumbai": {"temperature": 28, "condition": "Humid"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        return WeatherResponse(
            city=city,
            temperature=data["temperature"],
            condition=data["condition"]
        )
    return WeatherResponse(city=city, temperature=0, condition="Unknown")

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="Present the structured data clearly to users.",
    tools=[get_weather, calculate, get_stock_price],
)
```

### Benefits of Structured Outputs

1. **Type safety** — Pydantic validates data at runtime
2. **Self-documenting** — Field descriptions help the LLM understand data
3. **Consistent format** — Always get the same fields back
4. **Easy to extend** — Add new fields without breaking existing code

### ADK Web UI: Tool Calling in Action

The ADK web UI (`adk web`) shows the complete flow:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGENT GRAPH                         │  CHAT INTERFACE                      │
│                                      │                                      │
│       ┌──────────────┐               │  USER: "25 * 4"                      │
│       │ get_weather  │               │    ⚡ calculate                       │
│       └──────┬───────┘               │    ✓ calculate                       │
│              │                       │  AGENT: "25 * 4 is 100."             │
│              ▼                       │                                      │
│  ┌───────────────────┐               │  USER: "AAPL stock price"            │
│  │    my_agent       │───────────┐   │    ⚡ get_stock_price                 │
│  └───────────────────┘           │   │    ✓ get_stock_price                 │
│              │                   │   │  AGENT: "The stock price for AAPL    │
│              ▼                   │   │          is 178.5 USD."              │
│       ┌──────────────┐           │   │                                      │
│       │  calculate   │           │   │  USER: "What's the weather in Mumbai"│
│       └──────────────┘           │   │    ⚡ get_weather                     │
│              │                   │   │    ✓ get_weather                     │
│              ▼                   │   │  AGENT: "The weather in Mumbai is    │
│     ┌────────────────┐           │   │          Humid with a temperature    │
│     │get_stock_price │◄──────────┘   │          of 28 degrees."             │
│     └────────────────┘               │                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Event Panel** shows the structured response:

```
functionResponse:
  name: "get_weather"
  response:
    result:
      city: "Mumbai"
      temperature: 28
      condition: "Humid"
```

The LLM receives this structured JSON and converts it to natural language:
> "The weather in Mumbai is Humid with a temperature of 28 degrees."

## The Ollama Experiment

### Why Ollama?

Hit `429 RESOURCE_EXHAUSTED` errors with Gemini free tier. Tried running models locally.

### Model Comparison

| Model | Size | Tools Support | Result |
|-------|------|---------------|--------|
| gemma3:4b | 3.3GB | ❌ No | Infinite loops |
| mistral | 4.4GB | ✅ Yes | Hallucinated responses |
| llama3.1:8b | 4.9GB | ✅ Yes | Unreliable tool calls |

### Verdict

Local models struggled with reliable tool calling — fine for chat, unreliable for function calling.

## Back to Gemini

Set up billing on Google Cloud to remove quota limits. Gemini handles tools natively and reliably.

## Gotcha: API Key Issues

1. **Test your key:**
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hi"}]}]}'
```

2. **Check environment vs config:**
```bash
echo $GOOGLE_API_KEY        # Current session
grep GOOGLE_API_KEY ~/.zshrc # Config file
```

3. **Restart server after changing key** — ADK caches the key at startup.

## Time Spent

~4 hours. Tools, Ollama experiments, structured outputs, API debugging, testing setup.

## Lessons Learned

1. **Gemini is best for ADK** — Native tool support, reliable, well-integrated
2. **Use Pydantic for structured outputs** — Type safety and self-documenting
3. **Local LLMs aren't ready for tools** — Fine for chat, unreliable for function calling
4. **Environment matters** — Restart servers after changing API keys

## Testing ADK Agents

### The Key Insight

ADK separates concerns well:

```
┌─────────────────────────────────────────────────────────────────┐
│  Tools         = Pure Python functions    → Easy to test       │
│  Agent         = Orchestration layer      → Test separately    │
│  LLM           = External service         → Mock it            │
└─────────────────────────────────────────────────────────────────┘
```

Your business logic lives in the **tools**. Test those thoroughly with normal pytest patterns. The LLM is just the "brain" that decides which tool to call.

### Testing Tools Directly

```python
# test_tools.py
from my_agent.agent import get_weather, calculate, get_stock_price
from my_agent.agent import WeatherResponse, CalculationResponse, StockResponse

def test_get_weather_known_city():
    result = get_weather("Mumbai")
    assert isinstance(result, WeatherResponse)
    assert result.city == "Mumbai"
    assert result.temperature == 28
    assert result.condition == "Humid"

def test_get_weather_unknown_city():
    result = get_weather("Unknown City")
    assert result.temperature == 0
    assert result.condition == "Unknown"

def test_calculate_simple():
    result = calculate("2 + 2")
    assert isinstance(result, CalculationResponse)
    assert result.result == 4.0

def test_calculate_invalid():
    result = calculate("invalid")
    assert result.result == 0.0

def test_get_stock_price():
    result = get_stock_price("AAPL")
    assert isinstance(result, StockResponse)
    assert result.symbol == "AAPL"
    assert result.price == 178.50
```

### Why This Works

1. **Tools are just functions** — No LLM needed, no network calls
2. **Pydantic validates output** — Type errors caught automatically
3. **Fast feedback** — Tests run in milliseconds
4. **CI/CD friendly** — No API keys needed for tool tests

### VS Code Test Setup

To run tests from VS Code's Testing panel, configure `.vscode/settings.json`:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
}
```

**Gotcha:** pytest uses `test_*.py` naming convention, unittest uses `*test.py`. Make sure you enable the right framework.

After saving, reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window") to discover tests.

## Next Up

**Day 3:** Explore sub-agents and agent-to-agent communication.
