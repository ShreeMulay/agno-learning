#!/usr/bin/env python3
"""Example: Research Workflow
Category: outskill_cohort3/workflows

Two-agent workflow: Researcher gathers information, Writer creates summary.
Demonstrates manual workflow orchestration with sequential agent calls.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "topic": "electric vehicles",
}


def create_researcher(model):
    return Agent(
        name="Researcher",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=["Search for current information and gather key facts"],
        markdown=True,
    )


def create_writer(model):
    return Agent(
        name="Writer",
        model=model,
        instructions=[
            "Take research data and write a clear, engaging summary",
            "Organize information with headers and bullet points",
            "Include key statistics and quotes when available",
        ],
        markdown=True,
    )


def run_workflow(model, topic: str):
    researcher = create_researcher(model)
    writer = create_writer(model)
    
    print_section("Step 1: Research")
    print(f"  Researcher is gathering information about: {topic}")
    
    research = researcher.run(
        f"Find the latest information, trends, and key facts about: {topic}"
    )
    
    research_content = research.content if research.content else ""
    print(f"  Research complete. Found {len(research_content)} characters of data.")
    print()
    
    print_section("Step 2: Writing")
    print("  Writer is creating a summary...")
    
    summary = writer.run(
        f"Write a comprehensive but concise summary based on this research:\n\n"
        f"{research_content}\n\n"
        f"Create an engaging article about {topic}."
    )
    
    return summary


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_researcher(model)


def main():
    parser = argparse.ArgumentParser(
        description="Two-agent research and writing workflow"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--topic",
        type=str,
        default=DEFAULT_CONFIG["topic"],
        help="Topic to research and write about"
    )
    
    args = parser.parse_args()
    
    print_header("Research Workflow")
    
    print_section("Topic")
    print(f"  {args.topic}")
    print()
    
    print_section("Workflow")
    print("  1. Researcher → Gathers facts with web search")
    print("  2. Writer → Creates engaging summary")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    try:
        result = run_workflow(model, args.topic)
        
        print_section("Final Article")
        print(result.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
