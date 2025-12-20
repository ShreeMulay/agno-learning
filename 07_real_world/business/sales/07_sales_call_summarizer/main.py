"""
Example #007: Sales Call Summarizer
Category: business/sales

DESCRIPTION:
Processes sales call transcripts to extract key information, action items,
next steps, and updates for CRM. Works with transcripts from Gong, Chorus,
or manual notes.

PATTERNS:
- Structured Output (CallSummary schema)
- Workflows (multi-step processing)

ARGUMENTS:
- transcript (str): Call transcript text. Default: sample transcript
- deal_stage (str): Current pipeline stage. Default: "discovery"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "deal_stage": "discovery",
    "transcript": """
    Rep: Hi Sarah, thanks for taking the time today. I wanted to learn more about your current challenges with your CRM.
    
    Sarah: Sure, we're using Salesforce but honestly it's become a nightmare. Our reps spend more time updating records than selling.
    
    Rep: That's a common pain point. How much time would you say reps spend on admin work?
    
    Sarah: At least 2 hours a day. And the data quality is still terrible because they rush through it.
    
    Rep: What would it mean if you could cut that to 15 minutes?
    
    Sarah: That would be huge. We could probably add another 10% to quota attainment just from the extra selling time.
    
    Rep: Interesting. Who else would need to be involved in evaluating a solution?
    
    Sarah: My VP of Sales, Tom, and probably someone from IT for the integration piece.
    
    Rep: Great. What's your timeline for making a decision?
    
    Sarah: We're looking to have something in place by Q2. Budget is already approved for this initiative.
    
    Rep: Perfect. Let me send over some materials and schedule a demo with your team next week. Does Tuesday work?
    
    Sarah: Tuesday afternoon would be great. Thanks!
    """,
}


class ActionItem(BaseModel):
    """Action item from the call."""
    owner: str = Field(description="Who owns this action: rep/prospect/other")
    action: str = Field(description="What needs to be done")
    due: str = Field(description="When it's due")
    priority: str = Field(description="high/medium/low")


class Stakeholder(BaseModel):
    """Identified stakeholder."""
    name: str = Field(description="Person's name")
    role: str = Field(description="Their role/title")
    sentiment: str = Field(description="positive/neutral/negative/unknown")


class CallSummary(BaseModel):
    """Complete call summary for CRM."""
    
    call_type: str = Field(description="discovery/demo/negotiation/closing/check-in")
    duration_estimate: str = Field(description="Estimated call length")
    
    executive_summary: str = Field(description="2-3 sentence summary")
    
    # Pain & Value
    pain_points: list[str] = Field(description="Identified customer pain points")
    value_drivers: list[str] = Field(description="What value matters to them")
    
    # People
    stakeholders: list[Stakeholder] = Field(description="People mentioned")
    decision_maker: str = Field(description="Who makes the decision")
    
    # Deal Info
    budget_status: str = Field(description="Budget situation")
    timeline: str = Field(description="Decision timeline")
    competition: list[str] = Field(description="Competitors mentioned")
    
    # Next Steps
    action_items: list[ActionItem] = Field(description="Follow-up actions")
    next_meeting: str = Field(description="Next scheduled meeting")
    
    # Analysis
    deal_momentum: str = Field(description="positive/neutral/negative")
    risk_factors: list[str] = Field(description="Deal risks identified")
    coaching_notes: list[str] = Field(description="Suggestions for rep")
    
    crm_update: str = Field(description="Summary for CRM notes field")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Sales Call Summarizer agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Call Summarizer",
        instructions=[
            "You are a sales operations analyst who summarizes sales calls.",
            f"Current deal stage: {cfg['deal_stage']}",
            "",
            "Extract all relevant information from the transcript:",
            "- Pain points and value drivers",
            "- All stakeholders mentioned",
            "- Budget, timeline, and competition info",
            "- Specific action items with owners and deadlines",
            "",
            "Also provide:",
            "- Coaching notes for the rep",
            "- Risk factors to watch",
            "- A CRM-ready summary",
        ],
        output_schema=CallSummary,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    """Process a sample call."""
    print("\n" + "=" * 60)
    print("  Sales Call Summarizer - Demo")
    print("=" * 60)
    
    query = f"Summarize this sales call transcript:\n\n{config['transcript']}"
    
    print("\nProcessing call transcript...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, CallSummary):
        print(f"\n{'='*60}")
        print(f"  CALL SUMMARY: {result.call_type.upper()}")
        print(f"  Momentum: {result.deal_momentum.upper()}")
        print(f"{'='*60}")
        
        print(f"\n📋 SUMMARY\n{result.executive_summary}")
        
        print(f"\n😣 PAIN POINTS")
        for p in result.pain_points:
            print(f"  • {p}")
        
        print(f"\n💎 VALUE DRIVERS")
        for v in result.value_drivers:
            print(f"  • {v}")
        
        print(f"\n👥 STAKEHOLDERS")
        for s in result.stakeholders:
            print(f"  • {s.name} ({s.role}) - {s.sentiment}")
        print(f"  Decision Maker: {result.decision_maker}")
        
        print(f"\n💰 DEAL INFO")
        print(f"  Budget: {result.budget_status}")
        print(f"  Timeline: {result.timeline}")
        if result.competition:
            print(f"  Competition: {', '.join(result.competition)}")
        
        print(f"\n✅ ACTION ITEMS")
        for a in result.action_items:
            icon = "🔴" if a.priority == "high" else "🟡" if a.priority == "medium" else "🟢"
            print(f"  {icon} [{a.owner}] {a.action} (Due: {a.due})")
        
        print(f"\n📅 Next Meeting: {result.next_meeting}")
        
        if result.risk_factors:
            print(f"\n⚠️ RISKS")
            for r in result.risk_factors:
                print(f"  • {r}")
        
        print(f"\n💡 COACHING NOTES")
        for c in result.coaching_notes:
            print(f"  • {c}")
        
        print(f"\n📝 CRM UPDATE:\n{result.crm_update}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Sales Call Summarizer")
    parser.add_argument("--stage", type=str, default=DEFAULT_CONFIG["deal_stage"])
    parser.add_argument("--transcript", type=str, default=None)
    args = parser.parse_args()
    
    config = {**DEFAULT_CONFIG, "deal_stage": args.stage}
    if args.transcript:
        config["transcript"] = args.transcript
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
