#!/usr/bin/env python3
"""
Lesson 04: MCP Tools

Concepts covered:
- Model Context Protocol (MCP) for external tools
- MCPTools integration in Agno
- Connecting to remote MCP servers
- Using stdio transport for local servers

Run: python main.py --agno-docs
     python main.py --query "How do I create an agent with tools?"

Note: This example connects to the Agno documentation MCP server.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.tools.mcp import MCPTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_mcp_agent(model, mcp_url: str):
    """
    Create an agent with MCP tools.
    
    Args:
        model: The LLM model to use
        mcp_url: URL of the MCP server
    """
    # Create MCP tools connection
    mcp_tools = MCPTools(
        transport="streamable-http",
        url=mcp_url,
    )
    
    return Agent(
        model=model,
        tools=[mcp_tools],
        instructions=[
            "You are a helpful assistant with access to external tools via MCP.",
            "Use the available tools to answer questions.",
            "Be thorough and cite sources when possible.",
        ],
        
        markdown=True,
    )


def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        name="MCPAgent",
        model=model,
        # Instructions for the agent on how to use the MCP tool
        instructions=[
            "You are an agent with access to an MCP tool server.",
            "Choose the appropriate tool based on the user's request.",
            "If you're not sure which tool to use, ask for clarification.",
        ],
        
        markdown=True,
    )


def main():
    """Demonstrate MCP tools integration."""
    parser = argparse.ArgumentParser(
        description="MCP Tools demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--agno-docs",
        action="store_true",
        help="Connect to Agno documentation MCP server",
    )
    parser.add_argument(
        "--mcp-url",
        type=str,
        help="Custom MCP server URL",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What is Agno and how do I create an agent?",
        help="Query to send to the agent",
    )
    args = parser.parse_args()

    # Default to Agno docs if nothing specified
    if not args.agno_docs and not args.mcp_url:
        args.agno_docs = True

    print_header("Lesson 04: MCP Tools")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    # Determine MCP URL
    if args.agno_docs:
        mcp_url = "https://docs.agno.com/mcp"
        print(f"MCP Server: Agno Documentation ({mcp_url})")
    else:
        mcp_url = args.mcp_url
        print(f"MCP Server: {mcp_url}")

    print_section("Connecting to MCP Server")
    print("Setting up MCP tools connection...")
    
    try:
        agent = create_mcp_agent(model, mcp_url)
        print("Connection established!")
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        print("\nMake sure the MCP server is accessible.")
        sys.exit(1)

    print_section("Query")
    print(f"Question: {args.query}\n")
    
    print("Response:")
    print("-" * 60)
    
    try:
        agent.print_response(args.query)
    except Exception as e:
        print(f"Error: {e}")
        print("\nThe MCP server may be unavailable or the query failed.")
        print("Try a simpler query or check the server status.")

    print("-" * 60)

    print_section("About MCP")
    print("""
    Model Context Protocol (MCP) enables:
    
    1. External Tool Servers
       - Tools can run in separate processes
       - Written in any language (Python, Node.js, Rust, etc.)
       - Communicate via standardized protocol
    
    2. Transport Types
       - streamable-http: Remote servers over HTTPS
       - stdio: Local processes via stdin/stdout
    
    3. Use Cases
       - Documentation search (like this example)
       - Database access
       - API integrations
       - File system operations
       - Custom enterprise tools
    
    Popular MCP Servers:
       - mcp-server-fetch: Web scraping
       - mcp-server-filesystem: File access
       - mcp-server-github: GitHub integration
       - mcp-server-memory: Key-value storage
    """)


if __name__ == "__main__":
    main()
