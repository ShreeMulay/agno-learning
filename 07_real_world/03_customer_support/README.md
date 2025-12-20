# Example 03: Customer Support Agent

A multi-agent customer support system with specialized handlers.

## Features

- Intent routing to specialized agents
- FAQ knowledge base
- Ticket creation
- Escalation workflow
- Conversation memory

## Architecture

```
User Query → Router Agent → [FAQ Agent | Technical Agent | Billing Agent]
                         → Response with ticket if needed
```

## Key Concepts

- **Teams**: Route mode for intent-based routing
- **Memory**: Track customer context across sessions
- **Knowledge**: FAQ and documentation base
- **Tools**: Ticket creation, escalation

## Run the Example

```bash
python main.py

# Then interact:
# "How do I reset my password?"
# "I'm having trouble with billing"
# "My account is locked"
```

## Customization Ideas

1. Add sentiment analysis
2. Implement priority queuing
3. Add live agent handoff
4. Create ticket tracking
