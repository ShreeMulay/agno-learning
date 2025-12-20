# Lesson 01: Session State

Use session_state for in-memory storage within a conversation.

## Concepts Covered

- **session_state**: Dictionary for temporary storage
- **State initialization**: Setting initial values
- **State access**: Using state in instructions and tools
- **Stateful conversations**: Building context over time

## How It Works

```python
agent = Agent(
    model=model,
    session_state={"counter": 0, "items": []},  # Initial state
    instructions="Current counter: {counter}",   # State in prompts
)
```

## Run the Example

```bash
python main.py
```

## Next Lesson

[02_user_memories](../02_user_memories/) - Persist memories across sessions.
