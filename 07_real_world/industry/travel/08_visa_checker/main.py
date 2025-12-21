"""
Example #158: Visa Checker Agent
Category: industry/travel
DESCRIPTION: Checks visa requirements and provides application guidance
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"passport_country": "United States", "destination": "Vietnam", "trip_purpose": "tourism"}

class VisaRequirement(BaseModel):
    visa_required: bool = Field(description="Is visa required")
    visa_type: str = Field(description="Type of visa needed")
    duration_allowed: str = Field(description="Maximum stay allowed")
    cost: str = Field(description="Visa cost")
    processing_time: str = Field(description="Processing time")
    application_method: str = Field(description="How to apply")

class VisaCheck(BaseModel):
    passport_country: str = Field(description="Passport country")
    destination: str = Field(description="Destination country")
    requirement: VisaRequirement = Field(description="Visa requirements")
    required_documents: list[str] = Field(description="Documents needed")
    application_steps: list[str] = Field(description="Application steps")
    tips: list[str] = Field(description="Application tips")
    common_mistakes: list[str] = Field(description="Common mistakes to avoid")
    alternatives: list[str] = Field(description="Alternative entry options")
    disclaimer: str = Field(description="Important disclaimer")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Visa Checker",
        instructions=[
            "You are an expert visa and immigration advisor.",
            f"Check requirements for {cfg['passport_country']} passport holders",
            f"Traveling to {cfg['destination']} for {cfg['trip_purpose']}",
            "Provide accurate visa information and documentation requirements",
            "Include application tips and common pitfalls",
            "Always include disclaimer about verifying with official sources",
        ],
        output_schema=VisaCheck,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Visa Checker Agent - Demo")
    print("=" * 60)
    query = f"""Check visa requirements:
- Passport: {config['passport_country']}
- Destination: {config['destination']}
- Purpose: {config['trip_purpose']}

Provide visa requirements and application guidance."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, VisaCheck):
        print(f"\n🛂 {result.passport_country} → {result.destination}")
        req = result.requirement
        status = "✅ No Visa Required" if not req.visa_required else f"📋 {req.visa_type} Required"
        print(f"\n{status}")
        print(f"⏱️ Stay: {req.duration_allowed} | Cost: {req.cost}")
        print(f"📝 Processing: {req.processing_time}")
        print(f"🖥️ Apply: {req.application_method}")
        print(f"\n📄 Documents:")
        for doc in result.required_documents[:4]:
            print(f"  • {doc}")
        print(f"\n⚠️ {result.disclaimer}")

def main():
    parser = argparse.ArgumentParser(description="Visa Checker Agent")
    parser.add_argument("--passport", "-p", default=DEFAULT_CONFIG["passport_country"])
    parser.add_argument("--dest", "-d", default=DEFAULT_CONFIG["destination"])
    parser.add_argument("--purpose", default=DEFAULT_CONFIG["trip_purpose"])
    args = parser.parse_args()
    config = {"passport_country": args.passport, "destination": args.dest, "trip_purpose": args.purpose}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
