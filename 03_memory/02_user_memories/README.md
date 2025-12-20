# Lesson 02: User Memories

Persist user preferences and facts across sessions.

## Concepts Covered

- **enable_user_memories**: Automatic memory management
- **SqliteDb**: Database for persistence
- **user_id**: Identify users across sessions
- **Memory recall**: Automatic context retrieval

## How It Works

```python
from agno.db.sqlite import SqliteDb

agent = Agent(
    model=model,
    db=SqliteDb(db_file="agno.db"),
    enable_user_memories=True,
)

# Agent automatically remembers user info
agent.print_response("My name is Sarah", user_id="sarah")
agent.print_response("What's my name?", user_id="sarah")  # Remembers!
```

## Run the Example

```bash
python main.py
```
