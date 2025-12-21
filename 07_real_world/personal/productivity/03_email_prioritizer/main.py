"""
Example #183: Email Prioritizer Agent
Category: personal/productivity
DESCRIPTION: Prioritizes emails by urgency, importance, and suggests response strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"role": "manager"}

class EmailItem(BaseModel):
    subject: str = Field(description="Email subject")
    priority: str = Field(description="Priority: urgent, high, medium, low")
    action: str = Field(description="respond, delegate, archive, schedule")
    time_estimate: str = Field(description="Time to handle")
    suggested_response: str = Field(description="Brief response strategy")

class EmailPrioritization(BaseModel):
    urgent_now: list[EmailItem] = Field(description="Handle immediately")
    today_queue: list[EmailItem] = Field(description="Handle today")
    this_week: list[EmailItem] = Field(description="Handle this week")
    delegate_list: list[str] = Field(description="Emails to delegate")
    archive_suggestions: list[str] = Field(description="Emails to archive/delete")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Email Prioritizer",
        instructions=[
            f"You prioritize emails for a {cfg['role']}.",
            "Apply Inbox Zero principles for email management.",
            "Identify urgent items requiring immediate attention.",
            "Suggest delegation opportunities.",
            "Recommend quick responses vs. scheduled deep replies.",
        ],
        output_schema=EmailPrioritization,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Email Prioritizer - Demo")
    print("=" * 60)
    query = """Prioritize these emails:
    1. CEO: "Urgent: Board meeting prep needed by EOD"
    2. Newsletter: "Weekly industry digest"
    3. Client: "Question about contract renewal"
    4. HR: "Benefits enrollment reminder - deadline next week"
    5. Team member: "Need approval for vacation request"
    6. Vendor: "Invoice attached"
    7. Direct report: "Stuck on project, need guidance"
    8. Marketing: "Review campaign draft when you can" """
    response = agent.run(query)
    result = response.content
    if isinstance(result, EmailPrioritization):
        print(f"\n🔴 Urgent Now:")
        for e in result.urgent_now:
            print(f"  • {e.subject} - {e.action} ({e.time_estimate})")
        print(f"\n🟡 Today's Queue:")
        for e in result.today_queue:
            print(f"  • {e.subject} - {e.action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", "-r", default=DEFAULT_CONFIG["role"])
    args = parser.parse_args()
    run_demo(get_agent(config={"role": args.role}), {"role": args.role})

if __name__ == "__main__": main()
