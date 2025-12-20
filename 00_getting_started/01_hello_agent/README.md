# Lesson 01: Hello Agent

Your first Agno agent! This lesson introduces the core concepts you'll use throughout the course.

## Concepts Covered

- **Agent**: The main class that wraps an LLM with instructions and capabilities
- **Model**: The LLM provider (OpenRouter, OpenAI, Anthropic, etc.)
- **run()**: Execute the agent with a prompt
- **print_response()**: Convenient method for displaying responses

## How It Works

```python
from agno.agent import Agent
from agno.models.openrouter import OpenRouter

# 1. Create a model (the LLM)
model = OpenRouter(id="anthropic/claude-3.5-sonnet")

# 2. Create an agent with instructions
agent = Agent(
    model=model,
    instructions="You are a helpful assistant.",
)

# 3. Run the agent
response = agent.run("Hello!")
print(response.content)
```

## Key Points

1. **Agents are stateless by default** - Each `run()` is independent
2. **Instructions guide behavior** - Think of them as the agent's personality
3. **Models are swappable** - Change providers without changing agent code

## Run the Example

```bash
# Default (OpenRouter)
python main.py

# Different provider
python main.py --provider openai
python main.py --provider anthropic

# Custom message
python main.py --message "Tell me a joke"
```

## Exercises

1. Change the instructions to make the agent speak like a pirate
2. Try different models via `--model` flag
3. Add a second `agent.run()` call - what do you notice about context?

## Next Lesson

[02_multi_provider](../02_multi_provider/) - Learn to switch between LLM providers easily.
