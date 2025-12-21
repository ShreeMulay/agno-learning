"""
Example #124: Parent Communicator
Category: education/admin
DESCRIPTION: Generates parent communications about student progress
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"communication_type": "progress_update"}

class ParentCommunication(BaseModel):
    student_name: str = Field(description="Student name")
    parent_name: str = Field(description="Parent name")
    subject: str = Field(description="Email subject")
    message: str = Field(description="Communication message")
    tone: str = Field(description="positive, neutral, concerned")
    action_items: list[str] = Field(description="Requested parent actions")
    meeting_suggested: bool = Field(description="Meeting recommended")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Parent Communicator",
        instructions=["Write clear, professional communications", "Balance positives with concerns", "Use accessible language", "Include specific examples"],
        output_schema=ParentCommunication, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Parent Communicator - Demo\n" + "=" * 60)
    response = agent.run(f"Write {config['communication_type']}: Student Alex, Parent Ms. Johnson, Good grades in Math/Science, struggling in English (C-), missing homework assignments")
    result = response.content
    if isinstance(result, ParentCommunication):
        print(f"\nTo: {result.parent_name} | Re: {result.student_name}")
        print(f"Subject: {result.subject}")
        print(f"Tone: {result.tone} | Meeting: {result.meeting_suggested}")
        print(f"\nMessage:\n{result.message[:300]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--communication-type", "-t", default=DEFAULT_CONFIG["communication_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"communication_type": args.communication_type})

if __name__ == "__main__": main()
