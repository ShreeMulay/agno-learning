# Lesson 03: Tool Context

Access agent state and session data from within your tools using RunContext.

## Concepts Covered

- **RunContext**: Access to agent state within tools
- **session_state**: Persistent data across tool calls
- **Agent reference**: Access the agent itself from tools
- **State management**: Building stateful tools

## Why Tool Context?

Sometimes tools need more than just their parameters:
- Access previous results
- Store data for later use
- Track conversation state
- Count API calls or manage quotas

```python
from agno.run import RunContext

def add_to_cart(run_context: RunContext, item: str, quantity: int = 1) -> str:
    """Add an item to the shopping cart."""
    # Access session state
    if "cart" not in run_context.session_state:
        run_context.session_state["cart"] = []
    
    run_context.session_state["cart"].append({
        "item": item,
        "quantity": quantity
    })
    
    return f"Added {quantity}x {item} to cart"
```

## How It Works

1. Add `run_context: RunContext` as first parameter
2. Agno automatically injects the context
3. Access `session_state` dict for persistent storage
4. The LLM doesn't see this parameter - it's internal

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `session_state` | dict | Persistent storage across tool calls |
| `agent` | Agent | Reference to the agent |
| `messages` | list | Conversation history |
| `run_id` | str | Unique ID for this run |

## Run the Example

```bash
# Shopping cart example
python main.py --shop

# Note-taking example
python main.py --notes

# Counter/quota example
python main.py --counter
```

## Exercises

1. Build a todo list tool with add/remove/list operations
2. Create a tool that limits API calls (e.g., max 5 per session)
3. Make a tool that tracks conversation topics

## Next Lesson

[04_mcp_tools](../04_mcp_tools/) - Use external tool servers with MCP.
