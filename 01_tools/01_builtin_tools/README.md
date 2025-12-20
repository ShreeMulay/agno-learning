# Lesson 01: Built-in Tools

Agno comes with 100+ pre-built tools. Learn how to use them to extend your agent's capabilities.

## Concepts Covered

- **Tools**: Functions that agents can call to interact with the world
- **Toolkits**: Collections of related tools (DuckDuckGo, Calculator, etc.)
- **Tool selection**: How the LLM decides which tools to use

## How Tools Work

```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=model,
    tools=[DuckDuckGoTools()],  # Add tools here
    instructions="You can search the web to answer questions.",
)

# Agent will automatically use DuckDuckGo when appropriate
agent.print_response("What's the latest news about AI?")
```

## Popular Built-in Toolkits

| Toolkit | Purpose | Import |
|---------|---------|--------|
| **DuckDuckGoTools** | Web search | `agno.tools.duckduckgo` |
| **Calculator** | Math operations | `agno.tools.calculator` |
| **FileTools** | Read/write files | `agno.tools.file` |
| **ShellTools** | Run shell commands | `agno.tools.shell` |
| **PythonTools** | Execute Python code | `agno.tools.python` |
| **WebsiteTools** | Scrape websites | `agno.tools.website` |

## Tool Behavior

When you add tools to an agent:
1. The agent receives tool descriptions in its context
2. When a query needs external data, the LLM generates a tool call
3. Agno executes the tool and returns results to the LLM
4. The LLM incorporates results into its response

## Run the Example

```bash
# Web search example
python main.py --search "latest AI developments"

# Calculator example  
python main.py --calculate "What is 15% of 847?"

# Combined tools
python main.py --query "How much is $500 in euros today?"
```

## Exercises

1. Try a query that requires multiple tool calls
2. Add `show_tool_calls=True` to see which tools are used
3. Experiment with different toolkits

## Next Lesson

[02_custom_tools](../02_custom_tools/) - Create your own tools.
