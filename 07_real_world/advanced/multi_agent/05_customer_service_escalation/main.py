"""
Example #215: Customer Service Escalation Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Tiered support system with frontline, specialist, and supervisor agents
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"company": "TechCorp"}

class Resolution(BaseModel):
    issue_summary: str = Field(description="Summary of customer issue")
    tier_handled: str = Field(description="Which tier resolved: frontline, specialist, supervisor")
    resolution: str = Field(description="How issue was resolved")
    customer_satisfaction_risk: str = Field(description="low, medium, high")
    follow_up_needed: bool = Field(description="Whether follow-up is required")
    compensation_offered: str = Field(description="Any compensation provided")
    process_improvements: list[str] = Field(description="Suggested process improvements")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_frontline_agent(model=None, company: str = "TechCorp") -> Agent:
    return Agent(
        model=model or default_model(),
        name="Frontline Support",
        instructions=[
            f"You are frontline support for {company}.",
            "Handle common issues with standard solutions.",
            "Escalate complex issues to specialists.",
            "Be empathetic and solution-focused.",
        ],
        markdown=True,
    )

def get_specialist_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Technical Specialist",
        instructions=[
            "You handle escalated technical issues.",
            "Have deep product knowledge.",
            "Can authorize moderate compensations.",
            "Escalate policy exceptions to supervisor.",
        ],
        markdown=True,
    )

def get_supervisor_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Support Supervisor",
        instructions=[
            "You handle final escalations and exceptions.",
            "Can authorize significant compensations.",
            "Make policy exception decisions.",
            "Identify systemic issues for improvement.",
        ],
        output_schema=Resolution,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_supervisor_agent(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Customer Service Escalation - Demo")
    print("=" * 60)
    
    issue = """Customer complaint: "I've been a loyal customer for 5 years. 
    Your software crashed and I lost 3 hours of work. This is the third time 
    this month. I want a refund and compensation for my lost time. 
    Your frontline support just keeps apologizing but nothing changes." """
    
    frontline = get_frontline_agent(company=config.get("company", "TechCorp"))
    specialist = get_specialist_agent()
    supervisor = agent
    
    print(f"\n😤 Customer Issue: {issue[:100]}...")
    print("\n🔄 Processing through support tiers...")
    
    tier1 = frontline.run(f"Handle this customer issue:\n{issue}")
    tier2 = specialist.run(f"Escalated issue. Frontline notes: {tier1.content}\nOriginal issue: {issue}")
    
    final_prompt = f"""
    Escalated customer issue requiring supervisor decision:
    
    Original Issue: {issue}
    Frontline Response: {tier1.content}
    Specialist Analysis: {tier2.content}
    
    Make final resolution decision."""
    
    result = supervisor.run(final_prompt)
    
    if isinstance(result.content, Resolution):
        r = result.content
        print(f"\n📋 Issue: {r.issue_summary}")
        print(f"🎯 Resolved at: {r.tier_handled.upper()} tier")
        print(f"⚠️ Satisfaction Risk: {r.customer_satisfaction_risk}")
        print(f"\n✅ Resolution: {r.resolution}")
        if r.compensation_offered:
            print(f"💰 Compensation: {r.compensation_offered}")
        print(f"\n🔧 Process Improvements Suggested:")
        for imp in r.process_improvements:
            print(f"  • {imp}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", "-c", default=DEFAULT_CONFIG["company"])
    args = parser.parse_args()
    run_demo(get_agent(), {"company": args.company})

if __name__ == "__main__": main()
