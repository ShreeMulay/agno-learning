"""
Example #140: Closing Coordinator Agent
Category: industry/real_estate
DESCRIPTION: Manages real estate closing process and documentation
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"closing_date": "2024-03-15", "transaction_type": "purchase", "party": "buyer"}

class ClosingTask(BaseModel):
    task: str = Field(description="Task description")
    due_date: str = Field(description="Due date")
    responsible_party: str = Field(description="Who is responsible")
    status: str = Field(description="pending/in_progress/complete")
    documents_needed: list[str] = Field(description="Required documents")

class ClosingCoordination(BaseModel):
    transaction_summary: str = Field(description="Transaction summary")
    closing_date: str = Field(description="Scheduled closing date")
    days_until_closing: int = Field(description="Days remaining")
    tasks: list[ClosingTask] = Field(description="Closing tasks and timeline")
    documents_checklist: list[str] = Field(description="All required documents")
    estimated_closing_costs: dict = Field(description="Closing cost estimates")
    final_walkthrough_notes: list[str] = Field(description="Final walkthrough items")
    wire_instructions_reminder: str = Field(description="Wire fraud warning")
    contingencies_status: dict = Field(description="Status of contingencies")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Closing Coordinator",
        instructions=[
            "You are an expert real estate closing coordinator.",
            f"Manage {cfg['transaction_type']} closings for {cfg['party']}s",
            f"Coordinate all tasks leading to closing on {cfg['closing_date']}",
            "Track all required documents and deadlines",
            "Provide clear timeline with responsible parties",
            "Include wire fraud warnings - critical for buyer safety",
        ],
        output_schema=ClosingCoordination,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Closing Coordinator Agent - Demo")
    print("=" * 60)
    query = f"""Coordinate the closing process:
- Closing Date: {config['closing_date']}
- Transaction Type: {config['transaction_type']}
- Party: {config['party']}

Provide complete task list, timeline, and document checklist."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ClosingCoordination):
        print(f"\n📋 {result.transaction_summary}")
        print(f"📅 Closing: {result.closing_date} ({result.days_until_closing} days)")
        print(f"\n✅ Key Tasks:")
        for t in result.tasks[:4]:
            print(f"  [{t.status}] {t.task}")
            print(f"    Due: {t.due_date} | By: {t.responsible_party}")
        print(f"\n📄 Documents Needed: {len(result.documents_checklist)} items")
        for doc in result.documents_checklist[:4]:
            print(f"  • {doc}")
        print(f"\n⚠️ WIRE FRAUD WARNING:")
        print(f"  {result.wire_instructions_reminder}")

def main():
    parser = argparse.ArgumentParser(description="Closing Coordinator Agent")
    parser.add_argument("--date", "-d", default=DEFAULT_CONFIG["closing_date"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["transaction_type"])
    parser.add_argument("--party", "-p", default=DEFAULT_CONFIG["party"])
    args = parser.parse_args()
    config = {"closing_date": args.date, "transaction_type": args.type, "party": args.party}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
