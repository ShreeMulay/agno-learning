"""
Example #129: Financial Aid Processor
Category: education/admin
DESCRIPTION: Processes financial aid applications and awards
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"aid_type": "need_based"}

class AidAward(BaseModel):
    aid_type: str = Field(description="Type of aid")
    amount: float = Field(description="Award amount")
    source: str = Field(description="Funding source")
    renewable: bool = Field(description="Renewable for future years")

class FinancialAidPackage(BaseModel):
    student_name: str = Field(description="Student name")
    efc: float = Field(description="Expected Family Contribution")
    cost_of_attendance: float = Field(description="Total COA")
    demonstrated_need: float = Field(description="Financial need")
    awards: list[AidAward] = Field(description="Aid awards")
    total_aid: float = Field(description="Total aid package")
    remaining_balance: float = Field(description="Out of pocket cost")
    next_steps: list[str] = Field(description="Required actions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Financial Aid Processor",
        instructions=["Calculate financial need", "Assemble optimal aid package", "Consider all aid sources", "Ensure compliance with regulations"],
        output_schema=FinancialAidPackage, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Financial Aid Processor - Demo\n" + "=" * 60)
    response = agent.run(f"Process {config['aid_type']} aid: FAFSA EFC $8,000, COA $45,000, GPA 3.5, eligible for Pell Grant, institutional aid available")
    result = response.content
    if isinstance(result, FinancialAidPackage):
        print(f"\nStudent: {result.student_name}")
        print(f"COA: ${result.cost_of_attendance:,.0f} | Need: ${result.demonstrated_need:,.0f}")
        print(f"\nAwards:")
        for a in result.awards:
            print(f"  {a.aid_type}: ${a.amount:,.0f} ({a.source})")
        print(f"\nTotal Aid: ${result.total_aid:,.0f} | Balance: ${result.remaining_balance:,.0f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aid-type", "-t", default=DEFAULT_CONFIG["aid_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"aid_type": args.aid_type})

if __name__ == "__main__": main()
