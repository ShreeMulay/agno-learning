#!/usr/bin/env python3
"""
Lesson 02: Custom Tools

Concepts covered:
- Creating tools from Python functions
- Writing effective docstrings for LLM understanding
- Type hints for proper parameter handling
- Returning structured data from tools

Run: python main.py --weather "New York"
     python main.py --mortgage 400000 7.0 30
     python main.py --query "What's the weather and calculate 18% tip on $65"
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# =============================================================================
# Custom Tool Definitions
# =============================================================================

def get_weather(city: str, units: str = "fahrenheit") -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city (e.g., "New York", "London", "Tokyo")
        units: Temperature units - "fahrenheit" or "celsius" (default: fahrenheit)
        
    Returns:
        A string describing current weather conditions including temperature,
        conditions, and humidity.
    """
    # Mock weather data - in real app, call a weather API
    weather_data = {
        "new york": {"temp_f": 72, "temp_c": 22, "condition": "Partly Cloudy", "humidity": 65},
        "london": {"temp_f": 59, "temp_c": 15, "condition": "Overcast", "humidity": 80},
        "tokyo": {"temp_f": 77, "temp_c": 25, "condition": "Sunny", "humidity": 55},
        "san francisco": {"temp_f": 64, "temp_c": 18, "condition": "Foggy", "humidity": 75},
        "paris": {"temp_f": 68, "temp_c": 20, "condition": "Clear", "humidity": 60},
    }
    
    city_lower = city.lower()
    data = weather_data.get(city_lower, {"temp_f": 70, "temp_c": 21, "condition": "Clear", "humidity": 50})
    
    if units.lower() == "celsius":
        temp = f"{data['temp_c']}°C"
    else:
        temp = f"{data['temp_f']}°F"
    
    return f"Weather in {city}: {temp}, {data['condition']}, Humidity: {data['humidity']}%"


def calculate_tip(bill_amount: float, tip_percentage: float = 18.0) -> dict:
    """
    Calculate tip amount and total bill.
    
    Args:
        bill_amount: The bill amount in dollars before tip
        tip_percentage: Tip percentage (default: 18.0 for 18%)
        
    Returns:
        Dictionary with tip_amount, total_bill, and per_person amounts
    """
    tip_amount = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip_amount
    
    return {
        "bill_amount": f"${bill_amount:.2f}",
        "tip_percentage": f"{tip_percentage}%",
        "tip_amount": f"${tip_amount:.2f}",
        "total_bill": f"${total:.2f}",
    }


def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int,
) -> dict:
    """
    Calculate monthly mortgage payment and total cost.
    
    Args:
        principal: Loan amount in dollars (e.g., 500000 for $500,000)
        annual_rate: Annual interest rate as percentage (e.g., 6.5 for 6.5%)
        years: Loan term in years (typically 15 or 30)
        
    Returns:
        Dictionary with monthly_payment, total_paid, and total_interest
    """
    # Convert annual rate to monthly decimal
    monthly_rate = (annual_rate / 100) / 12
    num_payments = years * 12
    
    # Calculate monthly payment using mortgage formula
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / ((1 + monthly_rate) ** num_payments - 1)
    
    total_paid = monthly_payment * num_payments
    total_interest = total_paid - principal
    
    return {
        "loan_amount": f"${principal:,.2f}",
        "interest_rate": f"{annual_rate}%",
        "term_years": years,
        "monthly_payment": f"${monthly_payment:,.2f}",
        "total_paid": f"${total_paid:,.2f}",
        "total_interest": f"${total_interest:,.2f}",
    }


def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between common units of measurement.
    
    Args:
        value: The numeric value to convert
        from_unit: Source unit (miles, km, lbs, kg, fahrenheit, celsius)
        to_unit: Target unit (must be compatible with from_unit)
        
    Returns:
        String with the converted value and units
    """
    conversions = {
        ("miles", "km"): lambda x: x * 1.60934,
        ("km", "miles"): lambda x: x / 1.60934,
        ("lbs", "kg"): lambda x: x * 0.453592,
        ("kg", "lbs"): lambda x: x / 0.453592,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("feet", "meters"): lambda x: x * 0.3048,
        ("meters", "feet"): lambda x: x / 0.3048,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    if key not in conversions:
        return f"Cannot convert from {from_unit} to {to_unit}"
    
    result = conversions[key](value)
    return f"{value} {from_unit} = {result:.2f} {to_unit}"


# =============================================================================
# Agent Creation
# =============================================================================

def create_tool_agent(model, tools: list):
    """Create an agent with specified tools."""
    return Agent(
        model=model,
        tools=tools,
        instructions=[
            "You are a helpful assistant with access to various tools.",
            "Use the appropriate tool when asked about weather, calculations, or conversions.",
            "Always show the tool results clearly.",
            "If you use a tool, explain what you found.",
        ],
        markdown=True,
    )


def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_tool_agent(model, [get_weather, calculate_tip, calculate_mortgage, convert_units])


def main():
    """Demonstrate custom tools."""
    parser = argparse.ArgumentParser(
        description="Custom tools demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--weather",
        type=str,
        help="City to get weather for",
    )
    parser.add_argument(
        "--mortgage",
        nargs=3,
        metavar=("PRINCIPAL", "RATE", "YEARS"),
        help="Calculate mortgage: principal rate years",
    )
    parser.add_argument(
        "--tip",
        nargs=2,
        metavar=("BILL", "PERCENT"),
        help="Calculate tip: bill_amount tip_percent",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="General query using all tools",
    )
    args = parser.parse_args()

    # Default to general query if nothing specified
    if not any([args.weather, args.mortgage, args.tip, args.query]):
        args.query = "What's the weather in Paris and convert 100 miles to km?"

    print_header("Lesson 02: Custom Tools")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    # Create agent with all custom tools
    all_tools = [get_weather, calculate_tip, calculate_mortgage, convert_units]
    agent = create_tool_agent(model, all_tools)

    if args.weather:
        print_section("Weather Tool")
        agent.print_response(f"What's the weather in {args.weather}?")

    if args.mortgage:
        print_section("Mortgage Calculator Tool")
        principal, rate, years = args.mortgage
        query = f"Calculate mortgage for ${principal} at {rate}% for {years} years"
        agent.print_response(query)

    if args.tip:
        print_section("Tip Calculator Tool")
        bill, percent = args.tip
        query = f"Calculate {percent}% tip on a ${bill} bill"
        agent.print_response(query)

    if args.query:
        print_section("Multi-Tool Query")
        print(f"Query: {args.query}\n")
        agent.print_response(args.query)

    print()
    print_section("Custom Tool Checklist")
    print("  [+] Clear function name that describes the action")
    print("  [+] Detailed docstring with Args and Returns")
    print("  [+] Type hints for all parameters")
    print("  [+] Sensible default values where appropriate")
    print("  [+] Return structured data (dict) for complex results")


if __name__ == "__main__":
    main()
