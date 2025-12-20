"""
Example #025: Onboarding Checklist Tracker
Category: business/customer_success

DESCRIPTION:
Guides new customers through onboarding with personalized checklists.
Tracks progress, identifies stuck points, and provides proactive
assistance to ensure successful product adoption.

PATTERNS:
- Memory (track progress across sessions)
- Workflows (step-by-step onboarding)
- Structured Output (OnboardingStatus)

ARGUMENTS:
- customer_name (str): Customer name. Default: "Acme Corp"
- plan (str): Subscription plan. Default: "professional"
- completed_steps (str): Already completed steps. Default: sample
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "customer_name": "Acme Corp",
    "plan": "professional",
    "completed_steps": "account_created,team_invited",
    "days_since_signup": 5,
    "use_case": "project management for software teams",
}


# =============================================================================
# Output Schema
# =============================================================================

class OnboardingStep(BaseModel):
    """Individual onboarding step."""
    
    step_id: str = Field(description="Step identifier")
    name: str = Field(description="Step name")
    status: str = Field(description="completed/in_progress/pending/blocked")
    priority: str = Field(description="critical/high/medium/low")
    time_estimate: str = Field(description="Estimated time to complete")
    description: str = Field(description="What this step involves")
    resources: list[str] = Field(description="Helpful resources")
    blockers: list[str] = Field(default_factory=list, description="What might be blocking")


class ProgressMetrics(BaseModel):
    """Onboarding progress metrics."""
    
    completion_percentage: int = Field(description="Overall progress %")
    steps_completed: int = Field(description="Steps done")
    steps_remaining: int = Field(description="Steps left")
    estimated_completion: str = Field(description="Estimated completion date")
    health_status: str = Field(description="on_track/at_risk/delayed")
    days_in_onboarding: int = Field(description="Days since signup")


class Recommendation(BaseModel):
    """Proactive recommendation."""
    
    type: str = Field(description="next_step/tip/warning/celebration")
    title: str = Field(description="Recommendation title")
    message: str = Field(description="Detailed message")
    action: str = Field(description="What to do")
    urgency: str = Field(description="now/soon/later")


class OnboardingStatus(BaseModel):
    """Complete onboarding status."""
    
    customer: str = Field(description="Customer name")
    plan: str = Field(description="Subscription plan")
    progress: ProgressMetrics = Field(description="Progress metrics")
    steps: list[OnboardingStep] = Field(description="All onboarding steps")
    next_step: OnboardingStep = Field(description="Immediate next step")
    recommendations: list[Recommendation] = Field(description="Proactive recommendations")
    stuck_points: list[str] = Field(description="Identified friction points")
    success_milestones: list[str] = Field(description="Completed milestones")
    personalized_tips: list[str] = Field(description="Tips based on use case")
    csm_notes: str = Field(description="Notes for customer success manager")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Onboarding Checklist Tracker agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for onboarding tracking
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Onboarding Tracker",
        instructions=[
            "You are a customer onboarding specialist.",
            "Guide customers through product setup and adoption.",
            "",
            f"Customer: {cfg['customer_name']}",
            f"Plan: {cfg['plan']}",
            f"Use Case: {cfg['use_case']}",
            f"Days Since Signup: {cfg['days_since_signup']}",
            "",
            "Standard Onboarding Steps:",
            "1. account_created - Create account (auto-complete)",
            "2. team_invited - Invite team members",
            "3. profile_setup - Complete company profile",
            "4. first_project - Create first project",
            "5. integrations - Connect integrations",
            "6. workflow_setup - Set up workflows",
            "7. training_complete - Watch training videos",
            "8. first_milestone - Achieve first success metric",
            "",
            "Health Status Rules:",
            "- On Track: Completing ~1 step per day",
            "- At Risk: Stuck on same step for 3+ days",
            "- Delayed: Less than 50% complete after 7 days",
            "",
            "Personalization:",
            "- Adapt recommendations to their use case",
            "- Prioritize steps that deliver quick value",
            "- Flag blockers that need CSM intervention",
        ],
        output_schema=OnboardingStatus,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of onboarding tracking."""
    print("\n" + "=" * 60)
    print("  Onboarding Checklist Tracker - Demo")
    print("=" * 60)
    
    customer = config.get("customer_name", DEFAULT_CONFIG["customer_name"])
    plan = config.get("plan", DEFAULT_CONFIG["plan"])
    completed = config.get("completed_steps", DEFAULT_CONFIG["completed_steps"])
    days = config.get("days_since_signup", DEFAULT_CONFIG["days_since_signup"])
    use_case = config.get("use_case", DEFAULT_CONFIG["use_case"])
    
    query = f"""
    Generate onboarding status for:
    
    Customer: {customer}
    Plan: {plan}
    Use Case: {use_case}
    Days Since Signup: {days}
    Completed Steps: {completed}
    
    Provide current status, next steps, and proactive recommendations.
    """
    
    print(f"\nCustomer: {customer} ({plan})")
    print(f"Days in Onboarding: {days}")
    print("-" * 40)
    print("Analyzing onboarding progress...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, OnboardingStatus):
        health_emoji = {"on_track": "🟢", "at_risk": "🟡", "delayed": "🔴"}
        
        print(f"\n{'='*50}")
        print(f"ONBOARDING: {result.customer}")
        print(f"{'='*50}")
        
        p = result.progress
        print(f"\n{health_emoji.get(p.health_status, '⚪')} Status: {p.health_status.upper()}")
        print(f"📊 Progress: {p.completion_percentage}% ({p.steps_completed}/{p.steps_completed + p.steps_remaining} steps)")
        print(f"📅 Est. Completion: {p.estimated_completion}")
        print(f"⏱️  Days in Onboarding: {p.days_in_onboarding}")
        
        print(f"\n✅ Completed Milestones:")
        for milestone in result.success_milestones:
            print(f"  ✓ {milestone}")
        
        print(f"\n📋 Checklist:")
        for step in result.steps:
            icon = "✅" if step.status == "completed" else "🔄" if step.status == "in_progress" else "⬜" if step.status == "pending" else "🚫"
            print(f"  {icon} {step.name} ({step.status})")
            if step.status != "completed" and step.blockers:
                print(f"      ⚠️ Blockers: {', '.join(step.blockers)}")
        
        ns = result.next_step
        print(f"\n🎯 Next Step: {ns.name}")
        print(f"   {ns.description}")
        print(f"   Time: {ns.time_estimate} | Priority: {ns.priority}")
        if ns.resources:
            print(f"   Resources: {', '.join(ns.resources[:2])}")
        
        print(f"\n💡 Recommendations:")
        for rec in result.recommendations[:3]:
            emoji = "🎯" if rec.type == "next_step" else "💡" if rec.type == "tip" else "⚠️" if rec.type == "warning" else "🎉"
            print(f"  {emoji} [{rec.urgency.upper()}] {rec.title}")
            print(f"     {rec.message}")
        
        if result.stuck_points:
            print(f"\n⚠️ Friction Points:")
            for point in result.stuck_points:
                print(f"  • {point}")
        
        print(f"\n🎓 Tips for Your Use Case:")
        for tip in result.personalized_tips[:3]:
            print(f"  • {tip}")
        
        print(f"\n📝 CSM Notes:")
        print(f"  {result.csm_notes}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Onboarding Checklist Tracker - Guide customer adoption"
    )
    
    parser.add_argument(
        "--customer", "-c",
        type=str,
        default=DEFAULT_CONFIG["customer_name"],
        help="Customer name"
    )
    parser.add_argument(
        "--plan", "-p",
        type=str,
        default=DEFAULT_CONFIG["plan"],
        help="Subscription plan"
    )
    parser.add_argument(
        "--completed",
        type=str,
        default=DEFAULT_CONFIG["completed_steps"],
        help="Comma-separated completed steps"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=DEFAULT_CONFIG["days_since_signup"],
        help="Days since signup"
    )
    
    args = parser.parse_args()
    
    config = {
        "customer_name": args.customer,
        "plan": args.plan,
        "completed_steps": args.completed,
        "days_since_signup": args.days,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
