"""
Example #043: Onboarding Assistant
Category: business/hr

DESCRIPTION:
Guides new hires through onboarding, answers common questions,
and tracks task completion for first 30/60/90 days.

PATTERNS:
- Knowledge (company policies, procedures)
- Structured Output (OnboardingStatus)

ARGUMENTS:
- employee_name (str): New hire name
- start_date (str): Start date
- question (str): Question from new hire
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "employee_name": "Alex Rivera",
    "role": "Software Engineer",
    "start_date": "December 16, 2024",
    "department": "Engineering",
    "manager": "Sarah Chen",
    "question": "What do I need to complete in my first week? Also, how do I set up my development environment?",
}


class OnboardingTask(BaseModel):
    task: str = Field(description="Task description")
    category: str = Field(description="admin/technical/social/training")
    due_by: str = Field(description="Day 1/Week 1/Month 1/etc")
    priority: str = Field(description="required/recommended/optional")
    status: str = Field(description="pending/in_progress/completed")


class OnboardingStatus(BaseModel):
    employee_name: str = Field(description="Employee name")
    days_since_start: int = Field(description="Days since start date")
    current_phase: str = Field(description="Week 1/Month 1/Month 2/Month 3")
    answer_to_question: str = Field(description="Answer to the employee's question")
    relevant_tasks: list[OnboardingTask] = Field(description="Tasks relevant to question")
    upcoming_deadlines: list[str] = Field(description="Tasks due soon")
    helpful_resources: list[str] = Field(description="Links/docs to share")
    suggested_next_steps: list[str] = Field(description="What to do next")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Onboarding Assistant",
        instructions=[
            "You are a friendly onboarding assistant for new employees.",
            f"Employee: {cfg['employee_name']}, Role: {cfg['role']}",
            f"Start Date: {cfg['start_date']}, Manager: {cfg['manager']}",
            "",
            "Standard Onboarding Tasks:",
            "Day 1: ID badge, laptop setup, email/Slack, meet manager",
            "Week 1: HR paperwork, benefits enrollment, team introductions",
            "Month 1: Complete training modules, 1:1 with skip-level, first project",
            "Month 2: Performance goals, cross-team meetings",
            "Month 3: 90-day review, full project ownership",
            "",
            "For Engineering roles, also include:",
            "- Dev environment setup (IDE, Git, CI/CD access)",
            "- Code review training",
            "- Architecture overview session",
            "- Pair programming with buddy",
            "",
            "Be welcoming, helpful, and proactive with suggestions.",
        ],
        output_schema=OnboardingStatus,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Onboarding Assistant - Demo")
    print("=" * 60)
    
    question = config.get("question", DEFAULT_CONFIG["question"])
    
    response = agent.run(question)
    result = response.content
    
    if isinstance(result, OnboardingStatus):
        print(f"\n👋 Welcome, {result.employee_name}!")
        print(f"📅 Day {result.days_since_start} | {result.current_phase}")
        
        print(f"\n💬 Answer:")
        print(f"  {result.answer_to_question}")
        
        print(f"\n📋 Relevant Tasks:")
        for task in result.relevant_tasks:
            icon = {"required": "🔴", "recommended": "🟡", "optional": "🟢"}
            print(f"  {icon.get(task.priority, '⚪')} {task.task}")
            print(f"    Due: {task.due_by} | {task.category}")
        
        if result.upcoming_deadlines:
            print(f"\n⏰ Upcoming Deadlines:")
            for d in result.upcoming_deadlines:
                print(f"  • {d}")
        
        print(f"\n📚 Resources:")
        for r in result.helpful_resources:
            print(f"  • {r}")
        
        print(f"\n➡️ Next Steps:")
        for s in result.suggested_next_steps:
            print(f"  • {s}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Onboarding Assistant")
    parser.add_argument("--name", "-n", type=str, default=DEFAULT_CONFIG["employee_name"])
    parser.add_argument("--question", "-q", type=str, default=DEFAULT_CONFIG["question"])
    args = parser.parse_args()
    config = {**DEFAULT_CONFIG, "employee_name": args.name, "question": args.question}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
