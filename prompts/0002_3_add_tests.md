# Add Tests for ADK Tools

## Context

I'm at `~/adk-workshop` with a working ADK agent that has tools returning Pydantic models.
I want to add tests for my tools.

## Role

Act as a developer assistant helping me set up testing.

## Task

### 1. Install pytest

```bash
pip install pytest
```

### 2. Create test directory

```bash
mkdir -p tests
touch tests/__init__.py
```

### 3. Create test file `tests/test_tools.py`

```python
import pytest
from my_agent.agent import (
    get_weather,
    calculate,
    get_stock_price,
    WeatherResponse,
    CalculationResponse,
    StockResponse
)

class TestGetWeather:
    """Test the get_weather tool independently"""

    def test_known_city(self):
        """Test weather for a city we have data for"""
        result = get_weather("Delhi")
        assert isinstance(result, WeatherResponse)
        assert result.city == "Delhi"
        assert result.temperature == 32
        assert result.condition == "Sunny"

    def test_unknown_city(self):
        """Test weather for a city we don't have data for"""
        result = get_weather("Tokyo")
        assert isinstance(result, WeatherResponse)
        assert result.temperature == 0
        assert result.condition == "Unknown"

    def test_case_insensitive(self):
        """Test that city lookup is case insensitive"""
        result1 = get_weather("DELHI")
        result2 = get_weather("delhi")
        assert result1.temperature == result2.temperature


class TestCalculate:
    """Test the calculate tool independently"""

    def test_addition(self):
        result = calculate("2 + 2")
        assert isinstance(result, CalculationResponse)
        assert result.result == 4.0

    def test_percentage(self):
        result = calculate("100 * 0.15")
        assert result.result == 15.0

    def test_invalid_expression(self):
        """Invalid expressions should return 0"""
        result = calculate("not a math expression")
        assert result.result == 0.0


class TestGetStockPrice:
    """Test the get_stock_price tool independently"""

    def test_known_symbol(self):
        result = get_stock_price("AAPL")
        assert isinstance(result, StockResponse)
        assert result.symbol == "AAPL"
        assert result.price == 178.50

    def test_unknown_symbol(self):
        result = get_stock_price("UNKNOWN")
        assert result.price == 0.0

    def test_case_insensitive(self):
        result1 = get_stock_price("aapl")
        result2 = get_stock_price("AAPL")
        assert result1.price == result2.price
```

### 4. Run the tests

```bash
pytest tests/ -v
```

## Key Insight

ADK separates concerns well:

| Layer | What it is | How to test |
|-------|------------|-------------|
| Tools | Pure Python functions | Normal pytest |
| Agent | Orchestration layer | Test separately |
| LLM | External service | Mock it |

Your business logic lives in the **tools**. Test those thoroughly with normal pytest patterns. The LLM is just the "brain" that decides which tool to call.

## Why This Works

1. **Tools are just functions** - No LLM needed, no network calls
2. **Pydantic validates output** - Type errors caught automatically
3. **Fast feedback** - Tests run in milliseconds
4. **CI/CD friendly** - No API keys needed for tool tests
