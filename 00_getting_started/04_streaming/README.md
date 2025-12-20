# Lesson 04: Streaming Responses

Stream responses in real-time for better user experience.

## Concepts Covered

- **print_response()**: Convenient streaming output
- **stream=True**: Enable streaming mode
- **Async streaming**: Using arun() for async applications
- **Event handling**: Processing stream events

## Why Streaming?

Without streaming, users wait for the entire response:
```
[waiting... waiting... waiting...]
Here's the complete response that took 5 seconds to generate.
```

With streaming, users see progress immediately:
```
Here's... the... response... appearing... word... by... word...
```

This creates a much better user experience, especially for long responses.

## How It Works

### Simple Streaming (print_response)

```python
# Easiest way - just prints to stdout with streaming
agent.print_response("Tell me a story")
```

### Manual Streaming

```python
# Get streaming response
response = agent.run("Tell me a story", stream=True)

# Process events as they arrive
for event in response:
    if hasattr(event, 'content') and event.content:
        print(event.content, end="", flush=True)
```

### Async Streaming

```python
import asyncio

async def stream_response():
    async for event in agent.arun("Tell me a story", stream=True):
        if hasattr(event, 'content') and event.content:
            print(event.content, end="", flush=True)

asyncio.run(stream_response())
```

## Run the Example

```bash
# Basic streaming
python main.py

# Custom prompt
python main.py --prompt "Write a haiku about programming"

# Compare streaming vs non-streaming
python main.py --compare

# Async mode
python main.py --async
```

## When to Use Streaming

| Scenario | Streaming? |
|----------|------------|
| Interactive chat | Yes |
| Long-form content | Yes |
| Background processing | No |
| Structured output | Usually no |
| Batch processing | No |

## Exercises

1. Time the difference between streaming and non-streaming
2. Create a "typing indicator" effect with streaming
3. Try streaming with structured output (response_model)

## Module Complete!

Congratulations! You've completed Module 0: Getting Started.

**Next Module**: [01_tools](../../01_tools/) - Give your agents superpowers with tools.
