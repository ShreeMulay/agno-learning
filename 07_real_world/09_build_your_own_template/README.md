# Example 09: Build Your Own

A blank template for creating your own Agno application.

## Features

This template includes:
- Basic project structure
- Model configuration
- Argument parsing
- Placeholder for your logic

## Getting Started

1. Copy this directory
2. Edit `main.py` with your logic
3. Update this README

## Template Structure

```python
# 1. Configure your agent
agent = Agent(
    name="YourAgent",
    model=model,
    instructions=["Your instructions here"],
    tools=[YourTools()],
)

# 2. Add your logic
response = agent.run(user_input)

# 3. Process the response
print(response.content)
```

## Ideas for Projects

- Email assistant
- Meeting summarizer
- Task prioritizer
- Learning companion
- Writing coach
- Interview prep bot
- Recipe generator
- Travel planner
- Study buddy
- Habit tracker

## Resources

- [Agno Documentation](https://docs.agno.com)
- [Agno GitHub](https://github.com/agno-agi/agno)
- [OpenRouter Models](https://openrouter.ai/models)
