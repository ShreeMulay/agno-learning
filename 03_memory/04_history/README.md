# Lesson 04: Conversation History

Maintain context across multiple turns in a conversation.

## Concepts Covered

- **add_history_to_context**: Include previous messages
- **Session continuity**: Multi-turn conversations
- **History management**: Controlling context window

## How It Works

```python
agent = Agent(
    model=model,
    db=SqliteDb(db_file="agno.db"),
    add_history_to_context=True,
    num_history_runs=5,  # Include last 5 turns
)
```

## Run the Example

```bash
python main.py
```
