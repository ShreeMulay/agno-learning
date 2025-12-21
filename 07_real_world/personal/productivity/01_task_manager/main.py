"""
Example #181: Task Manager Agent
Category: personal/productivity
DESCRIPTION: Manages personal tasks with prioritization, deadlines, and progress tracking
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"context": "work"}

class Task(BaseModel):
    title: str = Field(description="Task title")
    priority: str = Field(description="Priority: high, medium, low")
    due_date: str = Field(description="Suggested due date")
    estimated_time: str = Field(description="Time estimate")
    category: str = Field(description="Task category")

class TaskManagement(BaseModel):
    tasks: list[Task] = Field(description="Organized task list")
    quick_wins: list[str] = Field(description="Tasks completable in <15 mins")
    blocked_tasks: list[str] = Field(description="Tasks needing dependencies resolved")
    today_focus: list[str] = Field(description="Top 3 tasks for today")
    weekly_goals: list[str] = Field(description="Key goals for the week")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Task Manager",
        instructions=[
            f"You are a personal task management assistant for {cfg['context']} tasks.",
            "Help organize, prioritize, and track tasks effectively.",
            "Use Eisenhower matrix principles: urgent/important classification.",
            "Identify quick wins and blocked items.",
            "Suggest realistic daily focus areas.",
        ],
        output_schema=TaskManagement,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Task Manager - Demo")
    print("=" * 60)
    query = """Organize these tasks:
    - Finish quarterly report (due Friday)
    - Reply to client emails
    - Schedule team meeting
    - Update project documentation
    - Review pull requests
    - Prepare presentation for Monday
    - Fix bug in login page
    - Order office supplies"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TaskManagement):
        print(f"\n📋 Today's Focus:")
        for t in result.today_focus:
            print(f"  • {t}")
        print(f"\n⚡ Quick Wins:")
        for q in result.quick_wins:
            print(f"  • {q}")
        print(f"\n🎯 Weekly Goals:")
        for g in result.weekly_goals:
            print(f"  • {g}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", "-c", default=DEFAULT_CONFIG["context"])
    args = parser.parse_args()
    run_demo(get_agent(config={"context": args.context}), {"context": args.context})

if __name__ == "__main__": main()
