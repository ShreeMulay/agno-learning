"""
Example #009: Commission Calculator
Category: business/sales

DESCRIPTION:
Calculates sales commissions based on complex compensation plans including
accelerators, SPIFFs, team bonuses, and what-if scenarios.

PATTERNS:
- Structured Output (CommissionReport schema)
- Tools (for plan rules lookup)

ARGUMENTS:
- rep_name (str): Sales rep name. Default: "Alex Johnson"
- closed_revenue (int): Revenue closed. Default: 500000
- quota (int): Quota amount. Default: 400000
- base_rate (float): Base commission rate. Default: 0.10
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "rep_name": "Alex Johnson",
    "closed_revenue": 500000,
    "quota": 400000,
    "base_rate": 0.10,
    "accelerator_threshold": 1.0,
    "accelerator_rate": 0.15,
}


class CommissionComponent(BaseModel):
    """Individual commission component."""
    component: str = Field(description="Name of commission component")
    revenue_applied: int = Field(description="Revenue this applies to")
    rate: float = Field(description="Commission rate")
    amount: int = Field(description="Commission amount")
    notes: str = Field(default="", description="Calculation notes")


class WhatIfScenario(BaseModel):
    """What-if analysis scenario."""
    scenario: str = Field(description="Scenario description")
    additional_revenue: int = Field(description="Additional revenue needed")
    additional_commission: int = Field(description="Additional commission earned")


class CommissionReport(BaseModel):
    """Complete commission calculation."""
    
    rep_name: str = Field(description="Rep name")
    period: str = Field(description="Commission period")
    
    # Performance
    quota: int = Field(description="Quota amount")
    closed_revenue: int = Field(description="Revenue closed")
    attainment_percent: float = Field(description="Quota attainment %")
    
    # Commission breakdown
    components: list[CommissionComponent] = Field(description="Commission components")
    total_commission: int = Field(description="Total commission earned")
    
    # Comparison
    on_target_earnings: int = Field(description="OTE if at 100%")
    vs_ote_percent: float = Field(description="Actual vs OTE %")
    
    # What-if scenarios
    scenarios: list[WhatIfScenario] = Field(description="What-if analyses")
    
    # Summary
    payout_date: str = Field(description="Expected payout date")
    notes: list[str] = Field(description="Additional notes")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Commission Calculator agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Commission Calculator",
        instructions=[
            "You are a sales compensation analyst who calculates commissions.",
            "",
            "Compensation Plan Rules:",
            f"- Base Rate: {cfg['base_rate']*100:.0f}% on all revenue",
            f"- Accelerator: {cfg['accelerator_rate']*100:.0f}% on revenue above {cfg['accelerator_threshold']*100:.0f}% of quota",
            "- Q4 SPIFF: Extra 2% on new logo deals",
            "- Team Bonus: $5,000 if team hits 110%",
            "",
            "Calculate:",
            "1. Base commission on all revenue",
            "2. Accelerator on overachievement",
            "3. Any applicable SPIFFs",
            "4. What-if scenarios for next milestone",
        ],
        output_schema=CommissionReport,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    """Calculate commission demo."""
    print("\n" + "=" * 60)
    print("  Commission Calculator - Demo")
    print("=" * 60)
    
    query = f"""
    Calculate commission for:
    - Rep: {config['rep_name']}
    - Closed Revenue: ${config['closed_revenue']:,}
    - Quota: ${config['quota']:,}
    - Base Rate: {config['base_rate']*100:.0f}%
    
    Show breakdown and what-if scenarios.
    """
    
    print(f"\nCalculating for {config['rep_name']}...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, CommissionReport):
        attain_emoji = "🏆" if result.attainment_percent >= 100 else "📊"
        
        print(f"\n{'='*60}")
        print(f"  {attain_emoji} COMMISSION REPORT: {result.rep_name}")
        print(f"  Period: {result.period}")
        print(f"{'='*60}")
        
        print(f"\n📈 PERFORMANCE")
        print(f"  Quota: ${result.quota:,}")
        print(f"  Closed: ${result.closed_revenue:,}")
        print(f"  Attainment: {result.attainment_percent:.1f}%")
        
        print(f"\n💰 COMMISSION BREAKDOWN")
        for c in result.components:
            print(f"  {c.component}")
            print(f"    ${c.revenue_applied:,} × {c.rate*100:.1f}% = ${c.amount:,}")
        
        print(f"\n  {'─'*40}")
        print(f"  TOTAL: ${result.total_commission:,}")
        print(f"  vs OTE: {result.vs_ote_percent:.1f}%")
        
        print(f"\n🎯 WHAT-IF SCENARIOS")
        for s in result.scenarios:
            print(f"  • {s.scenario}")
            print(f"    +${s.additional_revenue:,} → +${s.additional_commission:,}")
        
        print(f"\n📅 Payout: {result.payout_date}")
        
        if result.notes:
            print(f"\n📝 NOTES")
            for n in result.notes:
                print(f"  • {n}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Commission Calculator")
    parser.add_argument("--rep", type=str, default=DEFAULT_CONFIG["rep_name"])
    parser.add_argument("--revenue", type=int, default=DEFAULT_CONFIG["closed_revenue"])
    parser.add_argument("--quota", type=int, default=DEFAULT_CONFIG["quota"])
    args = parser.parse_args()
    
    config = {**DEFAULT_CONFIG, "rep_name": args.rep, "closed_revenue": args.revenue, "quota": args.quota}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
