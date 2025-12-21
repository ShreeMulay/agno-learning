"""
Example #180: Research Assistant Agent
Category: research/science
DESCRIPTION: General-purpose research assistant for academic work
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"task": "literature search", "field": "computer science", "deadline": "1 week"}

class ResearchTask(BaseModel):
    task_name: str = Field(description="Task name")
    status: str = Field(description="Status")
    output: str = Field(description="Task output or findings")
    next_steps: list[str] = Field(description="Suggested next steps")

class ResearchAssistance(BaseModel):
    request_summary: str = Field(description="Request summary")
    tasks_completed: list[ResearchTask] = Field(description="Completed tasks")
    key_findings: list[str] = Field(description="Key findings")
    resources_identified: list[str] = Field(description="Useful resources")
    timeline_suggestion: str = Field(description="Timeline suggestion")
    collaboration_tips: list[str] = Field(description="Collaboration tips")
    tools_recommended: list[str] = Field(description="Recommended tools")
    follow_up_actions: list[str] = Field(description="Follow-up actions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Research Assistant",
        instructions=[
            "You are an expert academic research assistant.",
            f"Assist with {cfg['task']} in {cfg['field']}",
            f"Work within {cfg['deadline']} deadline",
            "Provide thorough, accurate assistance",
            "Suggest useful tools and resources",
            "Help maintain research momentum",
        ],
        output_schema=ResearchAssistance,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Research Assistant Agent - Demo")
    print("=" * 60)
    query = f"""Assist with research:
- Task: {config['task']}
- Field: {config['field']}
- Deadline: {config['deadline']}

Provide comprehensive research assistance."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ResearchAssistance):
        print(f"\n📋 Request: {result.request_summary}")
        print(f"\n✅ Tasks Completed:")
        for task in result.tasks_completed[:2]:
            print(f"  • {task.task_name}: {task.status}")
            print(f"    Output: {task.output[:60]}...")
        print(f"\n💡 Key Findings:")
        for f in result.key_findings[:3]:
            print(f"  • {f}")
        print(f"\n🛠️ Tools: {', '.join(result.tools_recommended[:3])}")
        print(f"⏱️ Timeline: {result.timeline_suggestion}")
        print(f"\n📌 Next Steps:")
        for action in result.follow_up_actions[:3]:
            print(f"  • {action}")

def main():
    parser = argparse.ArgumentParser(description="Research Assistant Agent")
    parser.add_argument("--task", "-t", default=DEFAULT_CONFIG["task"])
    parser.add_argument("--field", "-f", default=DEFAULT_CONFIG["field"])
    parser.add_argument("--deadline", "-d", default=DEFAULT_CONFIG["deadline"])
    args = parser.parse_args()
    config = {"task": args.task, "field": args.field, "deadline": args.deadline}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
