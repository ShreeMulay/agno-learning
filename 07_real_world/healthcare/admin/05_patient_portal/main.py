"""
Example #105: Patient Portal Assistant
Category: healthcare/admin
DESCRIPTION: Handles patient portal inquiries - messages, results, appointments
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"inquiry_type": "general"}

class PortalResponse(BaseModel):
    patient_name: str = Field(description="Patient name")
    inquiry_type: str = Field(description="Type of inquiry")
    inquiry_summary: str = Field(description="Summary of patient's question")
    response: str = Field(description="Response to patient")
    action_items: list[str] = Field(description="Actions needed")
    escalate_to_provider: bool = Field(description="Needs provider review")
    urgency: str = Field(description="routine, soon, urgent")
    resources: list[str] = Field(description="Relevant patient resources")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Patient Portal Assistant",
        instructions=[
            "Respond to patient portal messages professionally and helpfully",
            "Provide accurate information within scope",
            "Identify messages requiring clinical escalation",
            "Use patient-friendly language, avoid medical jargon",
            "Include relevant educational resources"
        ],
        output_schema=PortalResponse, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Patient Portal Assistant - Demo\n" + "=" * 60)
    query = f"""Handle this {config['inquiry_type']} patient portal message:
From: Sarah Miller
Subject: Question about lab results
Message: Hi, I just saw my lab results are posted but I don't understand them. 
My potassium says 5.8 and there's a flag next to it. Should I be worried? 
Also, when is my next appointment with Dr. Chen?"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PortalResponse):
        print(f"\nPatient: {result.patient_name}")
        print(f"Inquiry: {result.inquiry_type}")
        print(f"Urgency: {result.urgency}")
        print(f"Escalate to Provider: {result.escalate_to_provider}")
        print(f"\nResponse:\n{result.response[:300]}...")
        print(f"\nAction Items: {', '.join(result.action_items)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inquiry-type", "-t", default=DEFAULT_CONFIG["inquiry_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"inquiry_type": args.inquiry_type})

if __name__ == "__main__": main()
