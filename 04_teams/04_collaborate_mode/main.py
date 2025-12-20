#!/usr/bin/env python3
"""Lesson 04: Collaborate Mode - Parallel execution.

Collaborate mode (delegate_to_all_members=True) sends the task to ALL members
simultaneously and combines their responses. Useful for reviews, brainstorming,
or getting multiple perspectives.

Run: python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def get_agent(model=None):
    """Create a collaborative team for the API."""
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    
    # Create specialized reviewers
    tech = Agent(
        name="Tech",
        role="Technical reviewer",
        model=model,
        instructions=[
            "Review from a technical perspective.",
            "Focus on feasibility, architecture, and implementation.",
            "Identify technical risks and requirements.",
        ],
    )
    
    legal = Agent(
        name="Legal",
        role="Legal reviewer",
        model=model,
        instructions=[
            "Review from a legal perspective.",
            "Focus on compliance, liability, and contractual terms.",
            "Identify legal risks and required protections.",
        ],
    )
    
    finance = Agent(
        name="Finance",
        role="Financial reviewer",
        model=model,
        instructions=[
            "Review from a financial perspective.",
            "Focus on costs, ROI, and budget implications.",
            "Identify financial risks and opportunities.",
        ],
    )
    
    return Team(
        name="Review Team",
        members=[tech, legal, finance],
        model=model,
        # Collaborate mode - all members receive the task simultaneously
        delegate_to_all_members=True,
        instructions=[
            "Coordinate a comprehensive multi-perspective review.",
            "Synthesize all reviewers' feedback into actionable recommendations.",
            "Highlight areas of agreement and any conflicting concerns.",
        ],
        markdown=True,
    )


SAMPLE_CONTRACT = """
CONTRACT PROPOSAL: Cloud Infrastructure Migration

Parties: TechCorp Inc. (Client) and CloudVendor Ltd. (Provider)

Scope:
- Migrate 50 legacy servers to cloud infrastructure
- 12-month implementation timeline
- 24/7 support with 99.9% uptime SLA

Pricing:
- Initial migration: $150,000
- Monthly hosting: $25,000/month
- Support tier: Premium ($5,000/month)

Terms:
- 3-year minimum commitment
- Early termination: 50% of remaining contract value
- Data sovereignty: All data stored in US regions
- IP ownership: Client retains all IP rights

Liability:
- Provider liability capped at 12 months of fees
- No liability for indirect/consequential damages
"""


def main():
    parser = argparse.ArgumentParser(description="Collaborate Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 04: Collaborate Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    team = get_agent(model)

    print_section("Sample Contract")
    print(SAMPLE_CONTRACT)

    print_section("Parallel Review")
    query = f"Review this contract proposal from all perspectives:\n{SAMPLE_CONTRACT}"
    team.print_response(query)


if __name__ == "__main__":
    main()
