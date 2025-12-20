"""
Example #008: Territory Planner
Category: business/sales

DESCRIPTION:
Optimizes sales territory assignments by analyzing account potential,
geographic distribution, and rep capacity to create balanced territories.

PATTERNS:
- Structured Output (TerritoryPlan schema)
- Tools (for market data lookup)

ARGUMENTS:
- num_reps (int): Number of sales reps. Default: 5
- region (str): Geographic region. Default: "West Coast"
- account_type (str): Account segment. Default: "enterprise"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "num_reps": 5,
    "region": "West Coast",
    "account_type": "enterprise",
    "total_accounts": 150,
    "total_arr": 15000000,
}


class TerritoryAssignment(BaseModel):
    """Single territory assignment."""
    rep_name: str = Field(description="Representative name/ID")
    territory_name: str = Field(description="Territory identifier")
    states_cities: list[str] = Field(description="Geographic coverage")
    account_count: int = Field(description="Number of accounts")
    total_potential: int = Field(description="ARR potential in USD")
    key_accounts: list[str] = Field(description="Top accounts in territory")


class TerritoryPlan(BaseModel):
    """Complete territory plan."""
    
    plan_name: str = Field(description="Plan identifier")
    region: str = Field(description="Region covered")
    
    assignments: list[TerritoryAssignment] = Field(description="Territory assignments")
    
    # Balance metrics
    avg_accounts_per_rep: float = Field(description="Average accounts per rep")
    avg_potential_per_rep: int = Field(description="Average ARR per rep")
    balance_score: int = Field(ge=0, le=100, description="How balanced 0-100")
    
    # Analysis
    coverage_gaps: list[str] = Field(description="Geographic gaps")
    overlap_risks: list[str] = Field(description="Potential conflicts")
    recommendations: list[str] = Field(description="Optimization suggestions")
    
    implementation_notes: str = Field(description="Rollout guidance")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Territory Planner agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Territory Planner",
        instructions=[
            "You are a sales operations expert who designs balanced territories.",
            f"Region: {cfg['region']}",
            f"Reps: {cfg['num_reps']}",
            f"Account Type: {cfg['account_type']}",
            f"Total Accounts: {cfg['total_accounts']}",
            f"Total ARR Potential: ${cfg['total_arr']:,}",
            "",
            "Territory Planning Principles:",
            "- Balance account count and revenue potential",
            "- Minimize travel time within territories",
            "- Consider account complexity and rep experience",
            "- Avoid splitting key accounts across territories",
            "",
            "Create named territories with clear boundaries.",
        ],
        output_schema=TerritoryPlan,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    """Generate a territory plan demo."""
    print("\n" + "=" * 60)
    print("  Territory Planner - Demo")
    print("=" * 60)
    
    query = f"""
    Create a territory plan for:
    - Region: {config['region']}
    - Reps: {config['num_reps']}
    - Account Type: {config['account_type']}
    - Total Accounts: {config['total_accounts']}
    - Total Potential: ${config['total_arr']:,}
    
    Design balanced territories with named assignments.
    """
    
    print(f"\nPlanning territories for {config['region']}...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, TerritoryPlan):
        print(f"\n{'='*60}")
        print(f"  {result.plan_name}")
        print(f"  Balance Score: {result.balance_score}/100")
        print(f"{'='*60}")
        
        print(f"\n📊 ASSIGNMENTS")
        for t in result.assignments:
            print(f"\n  {t.territory_name} - {t.rep_name}")
            print(f"    Coverage: {', '.join(t.states_cities[:3])}")
            print(f"    Accounts: {t.account_count} | Potential: ${t.total_potential:,}")
            print(f"    Key: {', '.join(t.key_accounts[:2])}")
        
        print(f"\n📈 METRICS")
        print(f"  Avg Accounts/Rep: {result.avg_accounts_per_rep:.1f}")
        print(f"  Avg Potential/Rep: ${result.avg_potential_per_rep:,}")
        
        if result.coverage_gaps:
            print(f"\n⚠️ GAPS: {', '.join(result.coverage_gaps)}")
        
        print(f"\n💡 RECOMMENDATIONS")
        for r in result.recommendations:
            print(f"  • {r}")
        
        print(f"\n📋 IMPLEMENTATION\n{result.implementation_notes}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Territory Planner")
    parser.add_argument("--reps", type=int, default=DEFAULT_CONFIG["num_reps"])
    parser.add_argument("--region", type=str, default=DEFAULT_CONFIG["region"])
    parser.add_argument("--type", type=str, default=DEFAULT_CONFIG["account_type"])
    args = parser.parse_args()
    
    config = {**DEFAULT_CONFIG, "num_reps": args.reps, "region": args.region, "account_type": args.type}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
