"""
Example #174: Data Analyzer Agent
Category: research/science
DESCRIPTION: Analyzes research data and interprets statistical results
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"data_type": "experimental", "analysis_goal": "hypothesis testing", "sample_size": 100}

class StatisticalResult(BaseModel):
    test_name: str = Field(description="Statistical test used")
    test_statistic: str = Field(description="Test statistic value")
    p_value: str = Field(description="P-value")
    effect_size: str = Field(description="Effect size")
    interpretation: str = Field(description="Plain language interpretation")

class DataAnalysis(BaseModel):
    data_summary: str = Field(description="Data summary")
    descriptive_stats: dict = Field(description="Descriptive statistics")
    normality_check: str = Field(description="Normality assessment")
    tests_performed: list[StatisticalResult] = Field(description="Statistical tests")
    key_findings: list[str] = Field(description="Key findings")
    assumptions_met: list[str] = Field(description="Assumptions checked")
    limitations: list[str] = Field(description="Analysis limitations")
    recommendations: list[str] = Field(description="Recommendations")
    visualizations_suggested: list[str] = Field(description="Suggested visualizations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Data Analyzer",
        instructions=[
            "You are an expert research data analyst.",
            f"Analyze {cfg['data_type']} data",
            f"Focus on {cfg['analysis_goal']}",
            "Choose appropriate statistical tests",
            "Check assumptions and limitations",
            "Provide clear interpretations",
        ],
        output_schema=DataAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Data Analyzer Agent - Demo")
    print("=" * 60)
    query = f"""Analyze research data:
- Data Type: {config['data_type']}
- Goal: {config['analysis_goal']}
- Sample Size: {config['sample_size']}
- Context: Comparing treatment vs control group outcomes

Provide comprehensive statistical analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DataAnalysis):
        print(f"\n📊 {result.data_summary}")
        print(f"📈 Normality: {result.normality_check}")
        print(f"\n🔬 Statistical Tests:")
        for test in result.tests_performed[:2]:
            print(f"  • {test.test_name}: {test.test_statistic}, p={test.p_value}")
            print(f"    Effect: {test.effect_size}")
            print(f"    → {test.interpretation}")
        print(f"\n💡 Key Findings:")
        for f in result.key_findings[:3]:
            print(f"  • {f}")
        print(f"\n📉 Visualize: {', '.join(result.visualizations_suggested[:3])}")

def main():
    parser = argparse.ArgumentParser(description="Data Analyzer Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["data_type"])
    parser.add_argument("--goal", "-g", default=DEFAULT_CONFIG["analysis_goal"])
    parser.add_argument("--n", type=int, default=DEFAULT_CONFIG["sample_size"])
    args = parser.parse_args()
    config = {"data_type": args.type, "analysis_goal": args.goal, "sample_size": args.n}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
