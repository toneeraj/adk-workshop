# Add Structured Outputs with Pydantic

## Context

I'm at ~/adk-workshop with an ADK agent that has tools returning strings.
I want to upgrade to structured outputs using Pydantic models.
Using Gemini model.

## Role

Act as a developer assistant helping me add structured outputs.

## Task

Replace ~/adk-workshop/my_agent/agent.py with:

```python
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Optional

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

# Tools that return structured data
def get_weather(city: str) -> WeatherResponse:
    """Get the current weather for a city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        Structured weather data with temperature and condition.
    """
    weather_data = {
        "delhi": {"temperature": 32, "condition": "Sunny"},
        "mumbai": {"temperature": 28, "condition": "Humid"},
        "bangalore": {"temperature": 24, "condition": "Cloudy"},
        "new york": {"temperature": 18, "condition": "Rainy"},
        "london": {"temperature": 12, "condition": "Foggy"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        return WeatherResponse(
            city=city,
            temperature=data["temperature"],
            condition=data["condition"]
        )
    else:
        return WeatherResponse(city=city, temperature=0, condition="Unknown")

def calculate(expression: str) -> CalculationResponse:
    """Calculate a mathematical expression.

    Args:
        expression: A math expression like "2 + 2" or "100 * 0.15"

    Returns:
        Structured result with expression and calculated value.
    """
    try:
        result = eval(expression)
        return CalculationResponse(expression=expression, result=float(result))
    except Exception:
        return CalculationResponse(expression=expression, result=0.0)

def get_stock_price(symbol: str) -> StockResponse:
    """Get the current stock price for a symbol.

    Args:
        symbol: Stock ticker symbol like AAPL, GOOGL, AMZN

    Returns:
        Structured stock data with price.
    """
    prices = {
        "AAPL": 178.50,
        "GOOGL": 141.25,
        "AMZN": 178.75,
        "MSFT": 378.90,
        "TSLA": 248.50,
    }
    symbol_upper = symbol.upper()
    price = prices.get(symbol_upper, 0.0)
    return StockResponse(symbol=symbol_upper, price=price)

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="""You are a helpful assistant with access to tools.
Use get_weather for weather questions.
Use calculate for math questions.
Use get_stock_price for stock price questions.
Present the structured data clearly to users.""",
    tools=[get_weather, calculate, get_stock_price],
)
```

Then restart the server:
```bash
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
adk web
```

## Key Concepts

1. **Pydantic BaseModel** — Define data structure with types
2. **Field(description=...)** — Help LLM understand each field
3. **Return type hint** — `-> WeatherResponse` tells ADK the output schema
4. **ADK auto-converts** — Pydantic models become JSON for the LLM

## Constraints

- Use Pydantic BaseModel for all tool outputs
- Include Field descriptions for each attribute
- Return type must match the Pydantic model
- Restart server after changes

## Test Queries

After restarting, try:
- "What's the weather in Delhi?" → Returns structured WeatherResponse
- "Calculate 100 * 0.15" → Returns structured CalculationResponse
- "MSFT stock price?" → Returns structured StockResponse
