# Add Tools to ADK Agent

## Context

I'm at ~/adk-workshop with a basic ADK agent.
Current agent has no tools - just responds to chat.
I want to add multiple tools so the agent can perform actions.

## Role

Act as a developer assistant helping me add tools to my agent.

## Task

Replace ~/adk-workshop/my_agent/agent.py with:

```python
from google.adk.agents import Agent

def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        A string describing the weather.
    """
    weather_data = {
        "delhi": "32°C, Sunny",
        "mumbai": "28°C, Humid",
        "bangalore": "24°C, Cloudy",
        "new york": "18°C, Rainy",
        "london": "12°C, Foggy",
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return f"Weather in {city}: {weather_data[city_lower]}"
    else:
        return f"Weather data not available for {city}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: A math expression like "2 + 2" or "100 * 0.15"

    Returns:
        The result of the calculation.
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating: {e}"

def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a symbol.

    Args:
        symbol: Stock ticker symbol like AAPL, GOOGL, AMZN

    Returns:
        The current stock price.
    """
    prices = {
        "AAPL": 178.50,
        "GOOGL": 141.25,
        "AMZN": 178.75,
        "MSFT": 378.90,
        "TSLA": 248.50,
    }
    symbol_upper = symbol.upper()
    if symbol_upper in prices:
        return f"{symbol_upper} is currently trading at ${prices[symbol_upper]}"
    else:
        return f"Stock price not available for {symbol}"

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="""You are a helpful assistant with access to tools.
Use get_weather for weather questions.
Use calculate for math questions.
Use get_stock_price for stock price questions.""",
    tools=[get_weather, calculate, get_stock_price],
)
```

Then restart the server:
```bash
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
adk web
```

## Constraints

- Use gemini-2.0-flash model
- Include all three tools: get_weather, calculate, get_stock_price
- Each tool must have type hints and docstrings (ADK uses these)
- Show the file after saving

## Test Queries

After restarting, try:
- "What's the weather in Delhi?"
- "Calculate 25 * 4 + 10"
- "What's Apple's stock price?"
