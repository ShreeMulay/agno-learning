#!/usr/bin/env python3
"""Example: Finance Agent
Category: outskill_cohort3/tools

Get stock prices, analyst recommendations, and company news using YFinance.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "symbol": "NVDA",
    "analysis": "full",
}


def create_agent(model, analysis_type: str = "full"):
    tool_config = {
        "stock_price": True,
        "analyst_recommendations": analysis_type in ["full", "recommendations"],
        "company_info": analysis_type in ["full", "info"],
        "company_news": analysis_type in ["full", "news"],
    }
    
    return Agent(
        name="FinanceAgent",
        model=model,
        tools=[YFinanceTools(**tool_config)],
        instructions=["Use tables to display financial data clearly"],
        markdown=True,
    )


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_agent(model)


def main():
    parser = argparse.ArgumentParser(
        description="Get stock data and analyst recommendations"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--symbol",
        type=str,
        default=DEFAULT_CONFIG["symbol"],
        help="Stock symbol (e.g., NVDA, AAPL, TSLA)"
    )
    parser.add_argument(
        "--analysis",
        type=str,
        choices=["full", "price", "recommendations", "info", "news"],
        default=DEFAULT_CONFIG["analysis"],
        help="Type of analysis to perform"
    )
    
    args = parser.parse_args()
    
    print_header("Finance Agent")
    
    print_section("Request")
    print(f"  Symbol: {args.symbol}")
    print(f"  Analysis: {args.analysis}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model, args.analysis)
    
    prompts = {
        "full": f"Give me a complete analysis of {args.symbol} including price, analyst recommendations, and recent news",
        "price": f"What is the current stock price of {args.symbol}?",
        "recommendations": f"Summarize analyst recommendations for {args.symbol}",
        "info": f"Tell me about {args.symbol} - what does the company do?",
        "news": f"What's the latest news about {args.symbol}?",
    }
    
    prompt = prompts[args.analysis]
    
    print_section("Analyzing...")
    
    try:
        response = agent.run(prompt)
        
        print_section("Analysis")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
