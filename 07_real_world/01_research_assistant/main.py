#!/usr/bin/env python3
"""Example 01: Research Assistant - Web search and summarization.

A practical agent that searches the web and provides researched answers.

Run with:
    python main.py "What are the latest developments in quantum computing?"
"""

import argparse
import sys
from pathlib import Path
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class ResearchResponse(BaseModel):
    """Structured research response."""
    summary: str = Field(description="Executive summary of findings")
    key_points: list[str] = Field(description="Main findings as bullet points")
    sources: list[str] = Field(description="URLs of sources used")
    follow_up_questions: list[str] = Field(description="Suggested follow-up questions")


def create_research_agent(model):
    """Create a research assistant agent."""
    
    return Agent(
        name="ResearchAssistant",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=[
            "You are a research assistant that provides well-researched answers.",
            "Always search the web for current information.",
            "Cite your sources with URLs.",
            "Provide a clear summary followed by key points.",
            "Suggest follow-up questions the user might want to explore.",
        ],
        markdown=True,
        show_tool_calls=True,
    )



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_research_agent(model)


def main():
    parser = argparse.ArgumentParser(description="Research Assistant")
    add_model_args(parser)
    parser.add_argument(
        "query", type=str, nargs="?",
        default="What are the benefits of meditation?",
        help="Research query"
    )
    parser.add_argument(
        "--structured", action="store_true",
        help="Use structured output"
    )
    args = parser.parse_args()

    print_header("Research Assistant")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_research_agent(model)
    
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    print_section("Researching...")
    
    if args.structured:
        # Structured output mode
        response = agent.run(
            args.query,
            response_model=ResearchResponse
        )
        result = response.content
        
        print_section("Summary")
        print(f"  {result.summary}")
        
        print_section("Key Points")
        for point in result.key_points:
            print(f"  • {point}")
        
        print_section("Sources")
        for source in result.sources:
            print(f"  - {source}")
        
        print_section("Follow-up Questions")
        for q in result.follow_up_questions:
            print(f"  ? {q}")
    else:
        # Free-form response
        response = agent.run(args.query)
        print(response.content)


if __name__ == "__main__":
    main()
