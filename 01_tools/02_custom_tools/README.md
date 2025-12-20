# Lesson 02: Custom Tools

Create your own tools to give agents any capability you need.

## Concepts Covered

- **Function tools**: Turn any Python function into a tool
- **Docstrings**: How LLMs understand your tool
- **Type hints**: Proper parameter handling
- **Return values**: What to send back to the agent

## How Custom Tools Work

Any Python function can become a tool. The LLM uses:
1. **Function name**: To identify the tool
2. **Docstring**: To understand what it does
3. **Parameter types**: To know what arguments to pass
4. **Return value**: To incorporate results

```python
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city (e.g., "New York", "London")
        
    Returns:
        A string describing the current weather conditions.
    """
    # Your implementation here
    return f"Weather in {city}: Sunny, 72°F"

# Add it to an agent
agent = Agent(
    model=model,
    tools=[get_weather],  # Just pass the function!
)
```

## Best Practices

### Good Docstrings
```python
def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int,
) -> dict:
    """
    Calculate monthly mortgage payment and total cost.
    
    Args:
        principal: Loan amount in dollars
        annual_rate: Annual interest rate as percentage (e.g., 6.5 for 6.5%)
        years: Loan term in years
        
    Returns:
        Dictionary with monthly_payment and total_cost
    """
```

### Type Hints Matter
```python
# Good - LLM knows exactly what to pass
def search_users(query: str, limit: int = 10) -> list[dict]:

# Bad - LLM has to guess
def search_users(query, limit=10):
```

## Run the Example

```bash
# Weather tool example
python main.py --weather "San Francisco"

# Custom calculation
python main.py --mortgage 500000 6.5 30

# Multiple custom tools
python main.py --query "What's the weather in Tokyo and calculate 20% tip on $85"
```

## Exercises

1. Create a tool that converts between units (miles to km, etc.)
2. Build a tool that looks up stock prices (mock data is fine)
3. Make a tool with optional parameters

## Next Lesson

[03_tool_context](../03_tool_context/) - Access agent state from within tools.
