#!/usr/bin/env python3
"""Example: Agent Team
Category: outskill_cohort3/teams

Combine multiple specialized agents to handle complex queries.
A web search agent and finance agent work together.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "query": "What's the latest news about NVDA and summarize analyst recommendations?",
}


def create_team(model):
    web_agent = Agent(
        name="WebAgent",
        role="Search the web for current news and information",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=["Always include source links"],
        markdown=True,
    )
    
    finance_agent = Agent(
        name="FinanceAgent",
        role="Get financial data and analyst recommendations",
        model=model,
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
        )],
        instructions=["Use tables for financial data"],
        markdown=True,
    )
    
    team = Team(
        name="ResearchTeam",
        members=[web_agent, finance_agent],
        model=model,
        instructions=[
            "Coordinate between team members to answer queries",
            "Use WebAgent for news and current events",
            "Use FinanceAgent for stock data and recommendations",
            "Include sources from web searches",
            "Display financial data in tables",
        ],
        markdown=True,
    )
    
    return team


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_team(model)


def main():
    parser = argparse.ArgumentParser(
        description="Multi-agent team for research queries"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_CONFIG["query"],
        help="Query for the agent team"
    )
    
    args = parser.parse_args()
    
    print_header("Agent Team")
    
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    print_section("Team Members")
    print("  1. WebAgent - Web search with DuckDuckGo")
    print("  2. FinanceAgent - Financial data with YFinance")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    team = create_team(model)
    
    print_section("Processing...")
    
    try:
        response = team.run(args.query)
        
        print_section("Team Response")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
