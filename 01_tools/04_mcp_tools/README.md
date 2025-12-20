# Lesson 04: MCP Tools

Use external tool servers with the Model Context Protocol (MCP).

## Concepts Covered

- **MCP**: Model Context Protocol for external tools
- **MCPTools**: Agno's MCP integration
- **Transport types**: stdio, streamable-http
- **External tool servers**: Using third-party MCP servers

## What is MCP?

MCP (Model Context Protocol) is an open protocol for connecting LLMs to external tools and data sources. It allows:

- Running tools in separate processes
- Using tools written in any language
- Connecting to remote tool servers
- Standardized tool interfaces

## How It Works

```python
from agno.tools.mcp import MCPTools

# Connect to an MCP server
mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://example.com/mcp",
)

agent = Agent(
    model=model,
    tools=[mcp_tools],
)
```

## Transport Types

| Transport | Use Case | Example |
|-----------|----------|---------|
| `stdio` | Local process | `npx @anthropic/mcp-server-*` |
| `streamable-http` | Remote server | HTTPS endpoints |

## Common MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| **mcp-server-fetch** | Web scraping | `npx @anthropic/mcp-server-fetch` |
| **mcp-server-filesystem** | File access | `npx @anthropic/mcp-server-filesystem` |
| **mcp-server-github** | GitHub API | `npx @anthropic/mcp-server-github` |
| **mcp-server-memory** | Key-value store | `npx @anthropic/mcp-server-memory` |

## Run the Example

```bash
# Connect to the Agno docs MCP server
python main.py --agno-docs

# Use a local MCP server (requires npx)
python main.py --local "fetch"
```

## Setting Up Local MCP Servers

```bash
# Install an MCP server
npm install -g @anthropic/mcp-server-fetch

# Use with stdio transport
mcp_tools = MCPTools(
    command=["npx", "@anthropic/mcp-server-fetch"],
    transport="stdio",
)
```

## Exercises

1. Connect to the Agno docs MCP server and ask questions
2. Set up a local filesystem MCP server
3. Create your own simple MCP server

## Module Complete!

Congratulations! You've completed Module 1: Tools.

**Next Module**: [02_knowledge](../../02_knowledge/) - Build agents with domain knowledge.
