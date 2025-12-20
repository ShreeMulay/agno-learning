# Example 07: Personal Knowledge Base

An agent that learns and remembers user information over time.

## Features

- Long-term user memories
- Session history
- Preference learning
- Context-aware responses

## Architecture

```
User Interaction → Memory Storage → Context Building → Personalized Response
```

## Key Concepts

- **Memory**: Persistent user memories
- **Database**: SQLite for storage
- **History**: Conversation continuity

## Run the Example

```bash
python main.py --user alice

# Then interact:
# "My favorite color is blue"
# "I work as a software engineer"
# "What do you know about me?"
```

## Customization Ideas

1. Add knowledge graph
2. Implement forgetting curve
3. Add relationship tracking
4. Create memory summaries
