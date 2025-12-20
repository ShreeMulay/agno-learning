#!/usr/bin/env python3
"""Example 03: Customer Support Agent - Multi-agent support system.

A team of agents that handles different types of customer inquiries.

Run with:
    python main.py
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Simulated tools for customer support
def create_ticket(title: str, priority: str, description: str) -> dict:
    """Create a support ticket."""
    ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "ticket_id": ticket_id,
        "title": title,
        "priority": priority,
        "status": "open",
        "created": datetime.now().isoformat(),
    }


def lookup_customer(email: str) -> dict:
    """Look up customer information."""
    # Simulated customer data
    customers = {
        "user@example.com": {
            "name": "John Doe",
            "plan": "Pro",
            "since": "2023-01-15",
            "tickets": 3,
        }
    }
    return customers.get(email, {"error": "Customer not found"})


def create_support_team(model):
    """Create a customer support team with specialized agents."""
    
    # FAQ/General Support Agent
    faq_agent = Agent(
        name="FAQAgent",
        role="General Support",
        model=model,
        instructions=[
            "You handle general questions and FAQs.",
            "Provide helpful, friendly responses.",
            "If you can't answer, suggest escalation.",
        ],
    )
    
    # Technical Support Agent
    tech_agent = Agent(
        name="TechAgent",
        role="Technical Support",
        model=model,
        tools=[create_ticket],
        instructions=[
            "You handle technical issues and troubleshooting.",
            "Create tickets for complex issues.",
            "Provide step-by-step solutions when possible.",
        ],
    )
    
    # Billing Support Agent
    billing_agent = Agent(
        name="BillingAgent",
        role="Billing Support",
        model=model,
        tools=[lookup_customer, create_ticket],
        instructions=[
            "You handle billing and account questions.",
            "Look up customer information when needed.",
            "Create tickets for billing disputes.",
        ],
    )
    
    # Create team with route mode
    team = Team(
        members=[faq_agent, tech_agent, billing_agent],
        name="CustomerSupport",
        instructions=[
            "Route customer inquiries to the appropriate agent:",
            "- General questions → FAQAgent",
            "- Technical issues, errors, bugs → TechAgent",
            "- Billing, payments, subscriptions → BillingAgent",
        ],
        model=model,
    )
    
    return team



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_support_team(model)


def main():
    parser = argparse.ArgumentParser(description="Customer Support Agent")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Customer Support System")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    team = create_support_team(model)
    
    print_section("Support Team")
    print("  Agents: FAQAgent, TechAgent, BillingAgent")
    print("  Mode: Route (intent-based)")
    print()
    
    print_section("Interactive Support")
    print("  Type your question. Enter 'quit' to exit.")
    print()
    print("  Example questions:")
    print("  - How do I reset my password?")
    print("  - I'm getting an error when I try to login")
    print("  - I need to update my billing information")
    print()
    
    while True:
        try:
            query = input("Customer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThank you for contacting support!")
            break
        
        if not query:
            continue
        if query.lower() == 'quit':
            print("Thank you for contacting support!")
            break
        
        response = team.run(query)
        print(f"\nSupport: {response.content}\n")


if __name__ == "__main__":
    main()
