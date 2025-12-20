"""
Example #047: Policy QA Bot
Category: business/hr

DESCRIPTION:
Answers employee questions about company policies by searching
the employee handbook and providing accurate, sourced responses.

PATTERNS:
- Knowledge (policy database)
- Structured Output (PolicyAnswer)
- RAG-like (search and cite)

ARGUMENTS:
- question (str): Employee's policy question
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "question": "How many sick days do I get per year? Can I use them for mental health days?",
    "handbook_excerpt": """
    EMPLOYEE HANDBOOK 2024
    
    CHAPTER 5: TIME OFF POLICIES
    
    5.1 Paid Time Off (PTO)
    - Full-time employees receive 15 days PTO in year 1-2, 20 days in years 3-5, 25 days after 5 years
    - PTO accrues monthly (1.25-2.08 days/month)
    - Maximum carryover: 5 days to next year
    - PTO requests require 2 weeks notice for 3+ days
    
    5.2 Sick Leave
    - All employees receive 10 sick days per year
    - Sick days do not roll over
    - Mental health days are included under sick leave
    - Doctor's note required for 3+ consecutive sick days
    - No advance notice required for sick days
    
    5.3 Holidays
    - Company observes 11 paid holidays
    - Floating holiday: 1 additional day of employee's choice
    
    CHAPTER 6: REMOTE WORK
    
    6.1 Eligibility
    - All employees eligible after 90-day probation
    - Manager approval required
    - Must be available during core hours (10am-3pm local time)
    
    6.2 Equipment
    - Company provides laptop and monitor
    - $500 home office stipend (one-time)
    - $50/month internet reimbursement
    """,
}


class PolicyAnswer(BaseModel):
    question_understood: str = Field(description="Rephrased question")
    direct_answer: str = Field(description="Clear, direct answer")
    policy_source: str = Field(description="Section/chapter cited")
    relevant_details: list[str] = Field(description="Additional relevant info")
    related_policies: list[str] = Field(description="Other policies they might need")
    confidence: str = Field(description="high/medium/low")
    escalate_to_hr: bool = Field(description="Should this go to HR?")
    escalation_reason: Optional[str] = Field(default=None, description="Why escalate")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    handbook = cfg.get("handbook_excerpt", DEFAULT_CONFIG["handbook_excerpt"])
    
    return Agent(
        model=model or default_model(),
        name="Policy QA Bot",
        instructions=[
            "You are a helpful HR policy assistant.",
            "Answer questions accurately based on the employee handbook.",
            "",
            "Guidelines:",
            "- Cite specific policy sections",
            "- Be clear and direct",
            "- Mention related policies proactively",
            "- Escalate complex or sensitive questions to HR",
            "- Never guess - if unsure, say so and recommend HR",
            "",
            f"HANDBOOK:\n{handbook}",
        ],
        output_schema=PolicyAnswer,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Policy QA Bot - Demo")
    print("=" * 60)
    
    question = config.get("question", DEFAULT_CONFIG["question"])
    
    response = agent.run(question)
    result = response.content
    
    if isinstance(result, PolicyAnswer):
        print(f"\n❓ Question: {result.question_understood}")
        
        print(f"\n✅ Answer:")
        print(f"   {result.direct_answer}")
        
        print(f"\n📖 Source: {result.policy_source}")
        
        if result.relevant_details:
            print(f"\n📋 Additional Details:")
            for d in result.relevant_details:
                print(f"   • {d}")
        
        if result.related_policies:
            print(f"\n🔗 Related Policies:")
            for p in result.related_policies:
                print(f"   • {p}")
        
        conf_icon = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        print(f"\n{conf_icon.get(result.confidence, '?')} Confidence: {result.confidence}")
        
        if result.escalate_to_hr:
            print(f"\n⚠️ Recommend speaking with HR: {result.escalation_reason}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Policy QA Bot")
    parser.add_argument("--question", "-q", type=str, default=DEFAULT_CONFIG["question"])
    args = parser.parse_args()
    agent = get_agent(config={"question": args.question})
    run_demo(agent, {"question": args.question})


if __name__ == "__main__":
    main()
