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

        # Verify it returns correct type
        assert isinstance(result, WeatherResponse)

        # Verify data
        assert result.city == "Delhi"
        assert result.temperature == 32
        assert result.condition == "Sunny"

    def test_unknown_city(self):
        """Test weather for a city we don't have data for"""
        result = get_weather("Tokyo")

        assert isinstance(result, WeatherResponse)
        assert result.city == "Tokyo"
        assert result.temperature == 0
        assert result.condition == "Unknown"

    def test_case_insensitive(self):
        """Test that city lookup is case insensitive"""
        result1 = get_weather("DELHI")
        result2 = get_weather("delhi")
        result3 = get_weather("Delhi")

        assert result1.temperature == result2.temperature == result3.temperature


class TestCalculate:
    """Test the calculate tool independently"""

    def test_addition(self):
        result = calculate("2 + 2")
        assert isinstance(result, CalculationResponse)
        assert result.result == 4.0

    def test_percentage(self):
        result = calculate("100 * 0.15")
        assert result.result == 15.0

    def test_complex_expression(self):
        result = calculate("(100 + 50) * 0.2")
        assert result.result == 30.0

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
        assert result.currency == "USD"

    def test_unknown_symbol(self):
        result = get_stock_price("UNKNOWN")

        assert result.symbol == "UNKNOWN"
        assert result.price == 0.0

    def test_case_insensitive(self):
        result1 = get_stock_price("aapl")
        result2 = get_stock_price("AAPL")

        assert result1.price == result2.price


class TestStructuredOutput:
    """Test that all tools return proper Pydantic models"""

    def test_weather_response_fields(self):
        """Verify WeatherResponse has all required fields"""
        result = get_weather("Delhi")

        # These should not raise AttributeError
        _ = result.city
        _ = result.temperature
        _ = result.condition

    def test_stock_response_fields(self):
        """Verify StockResponse has all required fields"""
        result = get_stock_price("AAPL")

        _ = result.symbol
        _ = result.price
        _ = result.currency

    def test_calculation_response_fields(self):
        """Verify CalculationResponse has all required fields"""
        result = calculate("1+1")

        _ = result.expression
        _ = result.result
