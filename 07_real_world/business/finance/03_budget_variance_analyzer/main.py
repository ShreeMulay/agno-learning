"""
Example #033: Budget Variance Analyzer
Category: business/finance

DESCRIPTION:
Analyzes actual vs budget performance, identifies significant variances,
and provides explanations with corrective action recommendations.

PATTERNS:
- Structured Output (VarianceReport)
- Knowledge (financial analysis)
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "budget_data": """
    Q4 2024 Budget vs Actual (in thousands):
    
    Revenue:
    - Product Sales: Budget $500K, Actual $485K
    - Services: Budget $200K, Actual $245K
    - Subscriptions: Budget $150K, Actual $162K
    
    Expenses:
    - Salaries: Budget $350K, Actual $365K
    - Marketing: Budget $80K, Actual $112K
    - Infrastructure: Budget $60K, Actual $55K
    - Travel: Budget $40K, Actual $28K
    - Software: Budget $25K, Actual $32K
    
    Notes:
    - Hired 2 new engineers mid-quarter
    - Launched major marketing campaign in November
    - Travel reduced due to remote work policy
    """,
}


class VarianceItem(BaseModel):
    category: str = Field(description="Budget category")
    budget: float = Field(description="Budgeted amount")
    actual: float = Field(description="Actual amount")
    variance: float = Field(description="Variance (actual - budget)")
    variance_pct: float = Field(description="Variance percentage")
    favorable: bool = Field(description="Is variance favorable")
    significance: str = Field(description="high/medium/low")
    explanation: str = Field(description="Likely cause")


class VarianceReport(BaseModel):
    period: str = Field(description="Reporting period")
    total_budget: float = Field(description="Total budget")
    total_actual: float = Field(description="Total actual")
    net_variance: float = Field(description="Net variance")
    revenue_variances: list[VarianceItem] = Field(description="Revenue variances")
    expense_variances: list[VarianceItem] = Field(description="Expense variances")
    key_insights: list[str] = Field(description="Key takeaways")
    action_items: list[str] = Field(description="Recommended actions")
    forecast_impact: str = Field(description="Impact on annual forecast")
    executive_summary: str = Field(description="Summary for leadership")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Budget Variance Analyzer",
        instructions=[
            "You are a financial analyst specializing in budget analysis.",
            "Analyze variances and provide actionable insights.",
            "",
            "Variance Thresholds:",
            "- High: >15% or >$50K variance",
            "- Medium: 5-15% or $10-50K",
            "- Low: <5% and <$10K",
            "",
            "For expenses: Under budget = favorable",
            "For revenue: Over budget = favorable",
            "",
            "Provide specific explanations and corrective actions.",
        ],
        output_schema=VarianceReport,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Budget Variance Analyzer - Demo")
    print("=" * 60)
    
    data = config.get("budget_data", DEFAULT_CONFIG["budget_data"])
    response = agent.run(f"Analyze budget variances:\n\n{data}")
    result = response.content
    
    if isinstance(result, VarianceReport):
        print(f"\n📊 {result.period}")
        print(f"Budget: ${result.total_budget:,.0f}K | Actual: ${result.total_actual:,.0f}K")
        print(f"Net Variance: ${result.net_variance:,.0f}K")
        
        print(f"\n📈 Revenue Variances:")
        for v in result.revenue_variances:
            icon = "🟢" if v.favorable else "🔴"
            print(f"  {icon} {v.category}: {v.variance_pct:+.1f}% (${v.variance:+,.0f}K)")
            print(f"      {v.explanation}")
        
        print(f"\n📉 Expense Variances:")
        for v in result.expense_variances:
            icon = "🟢" if v.favorable else "🔴"
            print(f"  {icon} {v.category}: {v.variance_pct:+.1f}% (${v.variance:+,.0f}K)")
            print(f"      {v.explanation}")
        
        print(f"\n💡 Key Insights:")
        for insight in result.key_insights[:3]:
            print(f"  • {insight}")
        
        print(f"\n🎯 Action Items:")
        for action in result.action_items[:3]:
            print(f"  • {action}")
        
        print(f"\n📋 Executive Summary: {result.executive_summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Budget Variance Analyzer")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["budget_data"])
    args = parser.parse_args()
    agent = get_agent(config={"budget_data": args.data})
    run_demo(agent, {"budget_data": args.data})


if __name__ == "__main__":
    main()
