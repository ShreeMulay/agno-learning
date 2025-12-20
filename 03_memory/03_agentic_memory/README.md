# Lesson 03: Agentic Memory

Let the agent control when to create, update, or delete memories.

## Concepts Covered

- **enable_agentic_memory**: Agent-controlled memory
- **Memory tools**: Create, update, delete memories
- **Strategic memory**: Agent decides what to remember

## How It Works

```python
agent = Agent(
    model=model,
    db=SqliteDb(db_file="agno.db"),
    enable_agentic_memory=True,  # Agent controls memory
)
```

## Run the Example

```bash
python main.py
```
