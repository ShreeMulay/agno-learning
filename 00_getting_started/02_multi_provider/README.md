# Lesson 02: Multi-Provider Support

Learn to switch between different LLM providers without changing your agent code.

## Concepts Covered

- **Provider abstraction**: Same agent code, different LLMs
- **Model configuration**: Centralized provider management
- **OpenRouter**: Access multiple models through one API

## Supported Providers

| Provider | Models | Best For |
|----------|--------|----------|
| **OpenRouter** | Claude, GPT, Llama, etc. | Flexibility, cost optimization |
| **OpenAI** | GPT-4o, GPT-4o-mini | Reliability, ecosystem |
| **Anthropic** | Claude 3.5 Sonnet | Reasoning, long context |
| **Google** | Gemini 2.0 | Speed, multimodal |
| **Groq** | Llama 3.3 70B | Fastest inference |
| **Ollama** | Local models | Privacy, offline |

## How It Works

```python
from shared.model_config import get_model

# Switch providers with one line
model = get_model("openrouter")   # Default: Claude 3.5 Sonnet
model = get_model("openai")       # Default: GPT-4o
model = get_model("anthropic")    # Default: Claude Sonnet 4.5

# Override default model
model = get_model("openrouter", "deepseek/deepseek-chat-v3")
model = get_model("openai", "gpt-4o-mini")

# Same agent code works with any provider
agent = Agent(model=model, instructions="...")
```

## Run the Example

```bash
# Compare providers
python main.py --provider openrouter
python main.py --provider openai
python main.py --provider anthropic

# Check which providers are configured
python -m shared.model_config
```

## Provider Selection Tips

| Use Case | Recommended Provider |
|----------|---------------------|
| Development/Testing | Groq (fast) or OpenRouter (flexible) |
| Production | OpenAI or Anthropic (reliable) |
| Cost-sensitive | OpenRouter with DeepSeek or Llama |
| Privacy/Offline | Ollama |
| Complex reasoning | Anthropic Claude |

## Exercises

1. Run the example with each provider you have configured
2. Compare response quality and speed between providers
3. Try the same prompt with different models via OpenRouter

## Next Lesson

[03_structured_output](../03_structured_output/) - Get type-safe responses with Pydantic.
